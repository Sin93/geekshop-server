from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings


def send_verify_email(user):
    verify_link = settings.DOMAIN_NAME + reverse('auth:verify', args=[user.id, user.activation_key])

    title = f'Подтверждение регистрации {user.email}'
    message = f'Для завершения регистрации, перейдите по ссылке: {verify_link}'

    return send_mail(
        title,
        message,
        settings.EMAIL_HOST_USER,
        [user.email, ],
        fail_silently=False,
    )
