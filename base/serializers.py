from rest_framework.serializers import ModelSerializer

from .models import *

class PhishSessionSerializer(ModelSerializer):
    class Meta:
        model = PhishSession
        exclude = ['id', "user"]

class TriesSerializer(ModelSerializer):
    class Meta:
        model = Tries
        exclude = ['id', "session"]

