from django.contrib.auth.models import AbstractUser
from django.db import models
from media.models import Media


class CustomUser(AbstractUser):
    class Meta:
        db_table = 'auth_users'

    PENDING = 'P'
    ACTIVE = 'A'
    BLOCKED = 'B'
    STATUS_CHOICES = (
        (PENDING, 'pending'),
        (ACTIVE, 'active'),
        (BLOCKED, 'blocked'),
    )

    EDITOR = 'E'
    ADMIN = 'A'
    SUPERADMIN = 'S'
    ROLE_CHOICES = (
        (EDITOR, 'editor'),
        (ADMIN, 'admin'),
        (SUPERADMIN, 'superadmin'),
    )

    email = models.EmailField('email', max_length=200, unique=True)
    REQUIRED_FIELDS = ['email', 'password']

    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default=EDITOR)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    avatar = models.ForeignKey(Media, blank=True, on_delete=models.SET_NULL, null=True)

    def get_verbose_status(self):
        return self.get_status_display()
