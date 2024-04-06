import accounts.models as accModels
import datetime

from rest_framework import exceptions, serializers


# Classe pour créer un user
class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = accModels.CustomUser
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email',
                  'birthday', 'can_be_contacted', 'sharing_data', 'profile_pic']
        extra_kwargs = {
            'username': {'write_only': True},
            'password': {'write_only': True},
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'email': {'write_only': True},
            'birthday': {'write_only': True},
            'can_be_contacted': {'write_only': True},
            'sharing_data': {'write_only': True},
            'profile_pic': {'write_only': True},
        }

    def create(self, validated_data):

        bday_send = validated_data['birthday']
        today = datetime.date.today()

        age = today.year - bday_send.year - ((today.month, today.day) <
                                             (bday_send.month, bday_send.day))

        if age <= 15:
            raise exceptions.ValidationError(
                detail={'error': 'Vous devez être âgé de plus de 15 ans pour utiliser ce service'})

        password = validated_data.pop('password')
        user = accModels.CustomUser.objects.create(**validated_data)
        user.set_password(password)
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
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'birthday',
                  'can_be_contacted', 'sharing_data', 'profile_pic']
