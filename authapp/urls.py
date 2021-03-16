from django.urls import path

import authapp.views as auth

app_name = 'auth'

urlpatterns = [
        path('login/', auth.LoginView.as_view(), name='login'),
        path('logout/', auth.LogoutView.as_view(), name='logout'),
        path('register/', auth.RegisterView.as_view(), name='register'),
        path('edit/', auth.UserEditView.as_view(), name='edit'),
        path('verify/<int:user_id>/<hash>', auth.VerifyView.as_view(), name='verify')
    ]
