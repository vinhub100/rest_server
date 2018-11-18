from django.db import models
from django.contrib.auth.models import User
# Create your models here.

Roles = (("Player", "Player"),
        ("Author", "Author"),)


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    role = models.CharField(max_length=8, choices=Roles)

    class Meta:
        verbose_name = "UserProfile"

    def __str__(self):
        return self.user.username + self.role

