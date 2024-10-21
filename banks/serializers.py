from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from .models import Banks

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banks
        fields = '__all__'