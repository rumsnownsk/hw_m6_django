import os.path

from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import get_user_avatar_path

# Create your models here.
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(
        upload_to=get_user_avatar_path,
        blank=True,
        null=True
    )
    email = models.EmailField('Ваш Email', unique=True, null=True)
    country = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    def __str__(self):
        return self.username or self.email or f"Пользователь #{self.id}"

    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         try:
    #             old_instance = CustomUser.objects.get(pk=self.pk)
    #             if(old_instance.avatar and self.avatar and old_instance.avatar.name != self.avatar.name):
    #                 if os.path.isfile(old_instance.avatar.path):
    #                     os.remove(old_instance.avatar.path)
    #             elif old_instance.avatar and not self.avatar:
    #                 old_path = old_instance.avatar.path
    #                 if os.path.exists(old_path):
    #                     os.remove(old_path)
    #         except CustomUser.DoesNotExist:
    #             pass
    #     super().save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     if self.avatar:
    #         if os.path.isfile(self.avatar.path):
    #             os.remove(self.avatar.path)
    #     super().delete(*args, **kwargs)