from django.urls import path

from .views import (
    RequestPhoneVerificationAPIView,
    verification_phone_view,
    verification_code_view,
    VerifyPhoneAPIView,
    ProfileAPIView,
    ProfileHtmlView
)


urlpatterns = [
    path('request-verification/', RequestPhoneVerificationAPIView.as_view(), name='request_verification'),
    path("enter-code/", VerifyPhoneAPIView.as_view(), name="enter_code"),
    path('verification-phone/', verification_phone_view, name='verification_phone_view'),
    path('verify/', verification_code_view, name='verify_phone'),
    path('api-profile/', ProfileAPIView.as_view(), name='profile'),
    path("profile/", ProfileHtmlView.as_view(), name="profile_html")
]
