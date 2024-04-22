import re
from rest_framework import serializers
from .models import UserProfile


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

    def validate_phone_number(self, value):

        if not re.match(r'^\+7\d{10}$', value):
            raise serializers.ValidationError(
                "Неверный формат номера телефона. Пожалуйста, используйте формат +7XXXXXXXXXX, где X - цифра.")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    invited_users = serializers.SerializerMethodField()

    def get_invited_users(self, obj):
        invited_users = obj.invited_users.all()
        user_data = [{'phone_number': user.phone_number} for user in
                     invited_users]
        return user_data

    class Meta:
        model = UserProfile
        fields = ["phone_number", "invite_code", "entered_invite_code", "invited_users"]
