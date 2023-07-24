import app_projects.models as projectsModels
import accounts.models as accModels
import accounts.serializers as accSerializers

from rest_framework import serializers

# Classe pour créer un user
class ProjectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = projectsModels.Projects
        fields = ['id', 'title', 'description', 'type']
        extra_kwargs = {
            'description': {'write_only': True},
        }

class ProjectDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = projectsModels.Projects
        fields = ['id', 'title', 'description', 'type', 'created_time']


class ContributorListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = projectsModels.Contributors
        fields = ['id', 'user', 'role']
    
    def get_user(self, instance):

        queryset = accModels.CustomUser.objects.get(pk=instance.user.pk)
        serializer = accSerializers.LittleUserSerializer(queryset)
        return serializer.data


class ContributorDetailsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = projectsModels.Contributors
        fields = ['id', 'user', 'role']

    def get_user(self, instance):

        queryset = accModels.CustomUser.objects.get(pk=instance.user.pk)
        serializer = accSerializers.LittleUserSerializer(queryset)
        return serializer.data