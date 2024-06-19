from django.db import models
from django.contrib.auth.models import User


class VisitLog(models.Model):
    user = models.CharField(max_length=64, null=True)
    date = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    get_params = models.TextField()
    post_params = models.TextField()
    user_agent = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.user} - {self.date}"
