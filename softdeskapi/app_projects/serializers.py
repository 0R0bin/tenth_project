import app_projects.models as projectsModels
import accounts.models as accModels
import accounts.serializers as accSerializers

from django.db import transaction
from rest_framework import serializers

# Classe pour créer un user
class ProjectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = projectsModels.Projects
        fields = ['id', 'title', 'description', 'type']
        extra_kwargs = {
            'id': {'read_only': True},
            'description': {'write_only': True},
        }
    
    @transaction.atomic
    def create(self, validated_data):

        project = projectsModels.Projects.objects.create(**validated_data)
        project.save()

        contributor_obj = {
            'project': project,
            'user': self.context['request'].user,
            'permission': 'AUT',
            'role': 'Author',
        }

        contributor = projectsModels.Contributors.objects.create(**contributor_obj)
        contributor.save()

        return project

class ProjectDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = projectsModels.Projects
        fields = ['id', 'title', 'description', 'type', 'created_time']


class ContributorListSerializer(serializers.ModelSerializer):

    class Meta:
        model = projectsModels.Contributors
        fields = ['id', 'user', 'role', 'permission']
        extra_kwargs = {
            'id': {'read_only': True},
        }


    def create(self, validated_data):

        # On vérifie que l'utilisateur soit bien Auteur pour avoir le droit d'ajouter des contributeurs au projet
        path = self.context['request'].META['PATH_INFO']
        project_id = (path.split('/'))[2]
        user_contributor = projectsModels.Contributors.objects.filter(project_id=project_id).get(user=self.context['request'].user)

        # Si le user log est bien l'auteur
        if user_contributor.permission == 'AUT':
            # Création Objet Contributor
            contributor_obj = {
                'project_id': project_id,
                'user': validated_data.pop('user', None),
                'permission': validated_data.pop('permission', None),
                'role': validated_data.pop('role', None),
            }

            contributor_created = projectsModels.Contributors.objects.create(**contributor_obj)
            contributor_created.save()
            return contributor_created
        # Sinon
        else:
            raise serializers.ValidationError({"Erreur": "Vous n'êtes pas auteur de ce projet"})
            


class ContributorDetailsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = projectsModels.Contributors
        fields = ['id', 'user', 'role']

    def get_user(self, instance):

        queryset = accModels.CustomUser.objects.get(pk=instance.user.pk)
        serializer = accSerializers.LittleUserSerializer(queryset)
        return serializer.data