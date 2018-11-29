from django.db import models
from django.contrib.auth.models import User


class PlayerScore(models.Model):
    user = models.OneToOneField(User)
    score = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Player Score"

    def __str__(self):
        return self.user.username
