from django.urls import path
from .views import (
    AccountView,
    AccountVerificationView,
    ShippingAddressListView,
    ShippingAddressCreateView,
    ShippingAddressView,
    LoginView, SignUpView, LogoutView)

urlpatterns = [
    path('account', AccountView.as_view()),
    path('account_verifications', AccountVerificationView.as_view()),
    path('account/address', ShippingAddressListView.as_view()),
    path('account/address/create', ShippingAddressCreateView.as_view()),
    path('account/address/<uuid:id>/', ShippingAddressView.as_view()),
    path('login', LoginView.as_view()),
    path('signup', SignUpView.as_view()),
    path('logout', LogoutView.as_view()),
]