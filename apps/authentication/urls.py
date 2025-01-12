from django.urls import path
from .views import (
    AccountView,
    AccountVerificationView,
    LoginView, SignUpView, LogoutView)

urlpatterns = [
    path('account', AccountView.as_view()),
    path('account_verifications', AccountVerificationView.as_view()),
    path('login', LoginView.as_view()),
    path('signup', SignUpView.as_view()),
    path('logout', LogoutView.as_view()),
]