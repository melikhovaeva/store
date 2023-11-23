from django.db import models
from django.contrib.auth.models import AbstractUser
from simple_history.models import HistoricalRecords


class User(AbstractUser):
  image = models.ImageField(upload_to='users_images', null=True, blank=True)
  history = HistoricalRecords()