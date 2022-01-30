from dj_rest_auth.serializers import UserDetailsSerializer, PasswordResetSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework import permissions, status, exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from authentication.models import CustomUser

UserModel = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.status == 'B':
            raise exceptions.AuthenticationFailed(
                'You account is blocked',
                'account_blocked',
            )
        if self.user.status == 'P':
            raise exceptions.AuthenticationFailed(
                'You account is pending',
                'account_pending',
            )
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        # token['name'] = user.get_full_name()
        # token['is_superuser'] = user.is_superuser
        # token['is_staff'] = user.is_staff
        token['role'] = user.role

        return token


class CustomUserDetailsSerializer(UserDetailsSerializer):
    def validate_username(self, username):
        username = super().validate_username(username)
        return username

    class Meta:
        extra_fields = []
        if hasattr(UserModel, "USERNAME_FIELD"):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, "EMAIL_FIELD"):
            extra_fields.append(UserModel.EMAIL_FIELD)

        model = UserModel
        fields = ('pk', *extra_fields, 'first_name', 'last_name')
        read_only_fields = ('email',)


class CustomPasswordResetSerializer(PasswordResetSerializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def get_email_options(self):
        return {
            'email_template_name': 'email/password_reset_email.txt',
            # 'html_email_template_name': 'email/password_reset_email.html',
        }
