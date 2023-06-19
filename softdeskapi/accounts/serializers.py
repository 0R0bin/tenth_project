import accounts.models as accModels
from rest_framework import serializers

# Classe pour créer un user
class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = accModels.CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_pic']
        extra_kwargs = {
            'username': {'write_only': True},
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'email': {'write_only': True},
            'profile_pic': {'write_only': True},
        }