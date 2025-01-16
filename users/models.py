from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .user_manager import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "username"
    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = "custom_user"
        verbose_name = "custo_muser"
        verbose_name_plural = "custom_users"
        ordering = ("-id",)
