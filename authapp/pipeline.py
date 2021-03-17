# Django
from django.utils import timezone
# Project
from authapp.models import ShopUserProfile
# Other
from datetime import datetime
from social_core.exceptions import AuthForbidden

import requests

API_VERSION = '5.92'
USER_FIELDS = ['bdate', 'sex', 'about', 'personal', 'domain']


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    token = response['access_token']
    fields = ','.join(USER_FIELDS)
    api_url = f'https://api.vk.com/method/users.get?fields={fields}&access_token={token}&v={API_VERSION}'
    resp = requests.get(api_url)

    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    if data['sex']:
        user.profile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE

    if data['about']:
        user.profile.aboutMe = data['about']

    if data['bdate']:
        date_of_birth = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
        # проверка был ли уже день рождения в этом году (True/False)
        was_birth = (timezone.now().date().month, timezone.now().date().day) < (date_of_birth.month, date_of_birth.day)
        # Явное лучше чем не явное, по этому явно приведу was_birth к 0 или 1
        was_birth = 1 if was_birth else 0
        # Вычисление полных лет
        age = timezone.now().date().year - date_of_birth.year - was_birth

        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        else:
            user.age = age

    try:
        user.profile.language = data['personal']['langs'][0]
    except KeyError:
        pass

    try:
        user.profile.vk_url = 'https://vk.com/' + data['domain']
    except KeyError:
        pass

    user.save()
