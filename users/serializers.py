from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # status = serializers.ChoiceField(choices=User.STATUS_CHOICES)

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email', 'username', 'is_staff', 'is_superuser', 'status', 'role', 'password'
        )

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        print(validated_data)
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = {
            'id': instance.id,
            # 'full_name': instance.get_full_name(),
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'username': instance.username,
            'email': instance.email,
            'is_staff': instance.is_staff,
            'is_superuser': instance.is_superuser,
            # 'role': instance.get_role_display(),
            # 'status': instance.get_status_display(),
            'role': instance.role,
            'status': instance.status,
        }
        return representation


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer = UserSerializer()
