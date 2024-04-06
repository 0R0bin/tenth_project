import app_projects.models as appModels
import tickets.models as tModels

from rest_framework import exceptions, serializers


class IssuesListSerializer(serializers.ModelSerializer):

    class Meta:
        model = tModels.Issues
        fields = ['id', 'title', 'description', 'tag', 'priority', 'status', 'assignee_user']

        extra_kwargs = {
            'description': {'write_only': True},
            'tag': {'write_only': True},
            'priority': {'write_only': True},
            'status': {'write_only': True},
            'assignee_user': {'write_only': True},
        }

    def create(self, validated_data):
        # Récupération des informations nécessaires
        path = self.context['request'].META['PATH_INFO']
        project_id = (path.split('/'))[3]
        project = appModels.Projects.objects.get(pk=project_id)
        user = self.context['request'].user
        assignee_user = validated_data.pop('assignee_user', None)

        if assignee_user is not None:
            if not appModels.Contributors.objects.filter(
                    project=project).filter(user=assignee_user).exists():
                raise exceptions.AuthenticationFailed(
                    detail={'Erreur': "assignee_user n'est pas assigné à ce projet"})

        obj_to_save = {
            'title': validated_data.pop('title', None),
            'description': validated_data.pop('description', None),
            'tag': validated_data.pop('tag', None),
            'priority': validated_data.pop('priority', None),
            'status': validated_data.pop('status', None),
            'project': project,
            'author_user': user,
            'assignee_user': assignee_user,
        }

        issue = tModels.Issues.objects.create(**obj_to_save)
        issue.save()

        return issue


class IssuesDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = tModels.Issues
        fields = ['id', 'title', 'description', 'tag', 'priority', 'status', 'assignee_user']


class CommentsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = tModels.Comments
        fields = ['id', 'description', 'uuid']
        extra_kwargs = {
            'uuid': {'read_only': True},
        }

    def create(self, validated_data):
        # Récupération des informations nécessaires
        path = self.context['request'].META['PATH_INFO']
        issue_id = (path.split('/'))[5]
        user = self.context['request'].user

        # Vérification de l'existence de l'issue et de l'appartenance de l'utilisateur
        if not tModels.Issues.objects.filter(pk=issue_id).exists():
            raise exceptions.NotFound(detail={'error': 'Cette issue n\'existe pas'})

        issue = tModels.Issues.objects.get(pk=issue_id)

        if not appModels.Contributors.objects.filter(
                project_id=issue.project.pk).filter(user=user).exists():
            raise exceptions.AuthenticationFailed(
                detail={'Erreur': "Vous ne faites pas parti de ce projet"})

        # Création de l'objet
        obj_to_save = {
            'description': validated_data.pop('description', None),
            'author_user': user,
            'issue': issue,
        }

        offer = tModels.Comments.objects.create(**obj_to_save)
        offer.save()

        return offer


class CommentsDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = tModels.Comments
        fields = ['id', 'description', 'created_time']
