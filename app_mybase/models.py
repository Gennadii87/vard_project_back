from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import User


class UserDataBaseProfile(models.Model):
    DATABASE_CHOICES = [
        ('mysql', 'MySQL'),
        ('postgresql', 'PostgreSQL'),
    ]

    objects = None
    name_profile = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    db_host = models.CharField(max_length=255, blank=True, null=True)
    db_port = models.IntegerField()
    db_username = models.CharField(max_length=255, blank=True, null=True)
    db_password = models.CharField(max_length=255, blank=True, null=True)
    db_type = models.CharField(max_length=10, choices=DATABASE_CHOICES, default='mysql')

    def __str__(self):
        return f'{self.pk} : {self.user} : {self.db_type}: {self.name_profile}'
