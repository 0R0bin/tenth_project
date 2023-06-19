import app_projects.models as projectsModels
from rest_framework import serializers

# Classe pour créer un user
class ProjectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = projectsModels.Projects
        fields = ['title', 'description', 'type']
        extra_kwargs = {
            'description': {'write_only': True},
        }

class ProjectDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = projectsModels.Projects
        fields = ['title', 'description', 'type', 'created_time']