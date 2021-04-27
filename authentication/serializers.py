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
        if self.user.status is 'B':
            raise exceptions.AuthenticationFailed(
                'You account is blocked',
                'account_blocked',
            )
        if self.user.status is 'P':
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
    def get_email_options(self):
        return {
            'from_email': 'admin@admin.com',
            'email_template_name': 'email/password_reset_email.txt'
        }
    # email = serializers.EmailField()
    # password_reset_form_class = PasswordResetForm
    #
    # def validate_email(self, value):
    #     self.reset_form = self.password_reset_form_class(data=self.initial_data)
    #     if not self.reset_form.is_valid():
    #         raise serializers.ValidationError(_('Error'))
    #
    #     if not CustomUser.objects.filter(email=value).exists():
    #         raise serializers.ValidationError(_('Invalid e-mail address'))
    #     return value
    #
    # def save(self):
    #     request = self.context.get('request')
    #     opts = {
    #         'use_https': request.is_secure(),
    #         'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
    #         'email_template_name': 'email/password_reset_email.txt',
    #         'request': request,
    #     }
    #     self.reset_form.save(**opts)
