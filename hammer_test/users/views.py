import random
import time
import uuid

from django.contrib.auth.models import User
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.db import transaction
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from .serializers import PhoneNumberSerializer, UserProfileSerializer
from .models import UserProfile


def verification_phone_view(request):
    return render(request, 'verification_form.html')


def verification_code_view(request):
    return render(request, "verify_code.html")


class ProfileHtmlView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            user_profile = get_object_or_404(UserProfile, user=user)
            serializer = UserProfileSerializer(user_profile)
            return render(request, 'profile.html', {'profile': serializer.data})
        else:
            HttpResponse({'message': 'Unauthorized'}, status=401)


class RequestPhoneVerificationAPIView(APIView):
    serializer_class = PhoneNumberSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        phone_number = serializer.validated_data['phone_number']
        verification_code = ''.join(random.choices('0123456789', k=4))
        request.session['verification_code'] = verification_code
        request.session['phone_number'] = phone_number
        time.sleep(random.uniform(1, 2))
        print("Verification code:", verification_code)
        return Response({"data": serializer.data, "code": verification_code})


class VerifyPhoneAPIView(APIView):
    serializer_class = None

    def post(self, request):
        verification_code = request.data.get("code")
        saved_verification_code = request.session.get('verification_code')

        if verification_code == saved_verification_code:
            phone_number = request.session.get('phone_number')

            with transaction.atomic():
                user, created = User.objects.select_for_update().get_or_create(
                    username=phone_number)

                if created:
                    invite_code = str(uuid.uuid4()).replace('-', '').upper()[:6]
                    UserProfile.objects.create(
                        user=user,
                        phone_number=phone_number,
                        invite_code=invite_code
                    )
            login(request, user)
            return Response({'message': "Success login"})
        else:
            return Response({'message': 'Invalid verification code.'},
                            status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(APIView):
    serializer_class = UserProfileSerializer

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            user_profile = get_object_or_404(UserProfile, user=user)
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data)
        else:
            return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        user = request.user
        entered_invite_code = request.data.get('entered_invite_code')

        if user.is_authenticated and entered_invite_code:
            with transaction.atomic():
                user_profile = get_object_or_404(
                    UserProfile.objects.select_for_update(), user=user)

                if (user_profile.invite_code != entered_invite_code
                        and not user_profile.entered_invite_code):
                    other_user_profile = get_object_or_404(
                        UserProfile, invite_code=entered_invite_code)

                    if (other_user_profile.entered_invite_code
                            != user_profile.invite_code):
                        user_profile.entered_invite_code = other_user_profile.invite_code
                        user_profile.invited_by = other_user_profile
                        user_profile.save()
                    else:
                        return Response({"message": "The user has already "
                                                    "activated your"
                                                    " invite code"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    return Response({'message': 'Entered another user\'s'
                                                ' invite code successfully'})
                else:
                    return Response({'message': 'You cannot activate'
                                                ' your invite code'
                                                ' or invite code exists'},
                                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'message': 'Unauthorized or not entered invite code'},
                status=status.HTTP_401_UNAUTHORIZED)
