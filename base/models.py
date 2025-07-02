from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PhishSession(models.Model):
    session_id = models.CharField(max_length = 20)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    gen_type = models.CharField(max_length = 10)
    is_online = models.BooleanField(default = False)
    redirect = models.TextField()

    def __str__(self):
        return self.session_id


class Tries(models.Model):
    session = models.ForeignKey(PhishSession, on_delete = models.CASCADE)
    try_id = models.CharField(max_length = 30)
    username = models.CharField(max_length = 200)
    password = models.CharField(max_length = 200)
    time = models.DateTimeField(auto_now_add = True)
    valid = models.BooleanField()

    def __str__(self):
        return self.try_id