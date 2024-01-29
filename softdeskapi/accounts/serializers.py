import accounts.models as accModels

from rest_framework import serializers

# Classe pour créer un user
class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = accModels.CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'birthday', 'can_be_contacted', 'sharing_data', 'profile_pic']
        # extra_kwargs = {
        #     'username': {'write_only': True},
        #     'first_name': {'write_only': True},
        #     'last_name': {'write_only': True},
        #     'email': {'write_only': True},
        #     'birthday': {'write_only': True},
        #     'can_be_contacted': {'write_only': True},
        #     'sharing_data': {'write_only': True},
        #     'profile_pic': {'write_only': True},
        # }
    
    def create(self, validated_data):

        user = accModels.CustomUser.objects.create(**validated_data)
        user.save()

        return user

class LittleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = accModels.CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'profile_pic']



#######################################################
#               Serializers pour Comptes              #
#######################################################
class UserFullSerializer(serializers.ModelSerializer):

    class Meta:
        model = accModels.CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'age', 'can_be_contacted', 'sharing_data', 'profile_pic']