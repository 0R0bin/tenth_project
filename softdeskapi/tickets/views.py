import accounts.models as accModels
import app_projects.models as appPModels
import tickets.models as tModels
import tickets.serializers as tSerializers

from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class IssuesViewSet(MultipleSerializerMixin,  ModelViewSet):
    """
    Vue des problèmes d'un projet
    On renvoie les problèmes du projet (table Issues)
    Full CRUD
    """

    permission_classes = [IsAuthenticated]

    serializer_class = tSerializers.IssuesListSerializer
    detail_serializer_class = tSerializers.IssuesDetailsSerializer

    def get_queryset(self):
        project_id_sent = self.kwargs['project_id']
        user_log = self.request.user

        if not appPModels.Contributors.objects.filter(
                project_id=project_id_sent).filter(user=user_log).exists():
            raise exceptions.AuthenticationFailed(
                detail={'Erreur': "Vous n'êtes pas affilié à ce projet"})

        queryset = tModels.Issues.objects.filter(project_id=project_id_sent)
        return queryset

    def update(self, request, *args, **kwargs):
        issue = self.get_object()

        if not (issue.author_user == self.request.user or issue.assignee_user == self.request.user):
            raise exceptions.AuthenticationFailed(
                detail={'Erreur': 'Vous n\'êtes ni l\'auteur de cette issue, ni assigné dessus'})

        request.data._mutable = True

        if request.data['assignee_user'] == "":
            request.data['assignee_user'] = None
        else:
            project_id = self.kwargs['project_id']
            assignee_user_id = request.data['assignee_user']
            if not appPModels.Contributors.objects.filter(
                    project_id=project_id).filter(user_id=assignee_user_id).exists():
                raise exceptions.AuthenticationFailed(
                    detail={'Erreur': "assignee_user n'est pas assigné à ce projet"})
            request.data['assignee_user'] = accModels.CustomUser.objects.get(pk=assignee_user_id)

        request.data._mutable = False

        data = request.data

        for key, value in data.items():
            setattr(issue, key, value)
        issue.save()
        return Response({'Accept': 'L\'issue a bien été mise à jour'})

    def destroy(self, request, *args, **kwargs):
        issue = self.get_object()

        if issue.author_user != self.request.user:
            raise exceptions.AuthenticationFailed(
                detail={'Erreur': 'Vous n\'êtes pas l\'auteur de cette issue'})

        issue.delete()

        return Response({'Accept': 'L\'issue a bien été supprimée'})


class CommentViewSet(MultipleSerializerMixin,  ModelViewSet):
    """
    Vue des commentaires d'un projet
    On renvoie les commentaires de l'issue (table Comments)
    Full CRUD
    """

    permission_classes = [IsAuthenticated]

    serializer_class = tSerializers.CommentsListSerializer
    detail_serializer_class = tSerializers.CommentsDetailsSerializer

    def get_queryset(self):
        issue_id_sent = self.kwargs['issue_id']
        user_log = self.request.user

        # Vérification
        if not tModels.Issues.objects.filter(pk=issue_id_sent).exists():
            raise exceptions.NotFound(
                detail={'error': 'Aucun objet Issue trouvé avec cet identifiant.'})

        issue = tModels.Issues.objects.get(pk=issue_id_sent)

        if not appPModels.Contributors.objects.filter(
                project_id=issue.project_id).filter(user=user_log).exists():
            raise exceptions.AuthenticationFailed(
                detail={'error': 'Vous n\'êtes pas assigné à ce projet.'})

        queryset = tModels.Comments.objects.filter(issue_id=issue_id_sent)

        return queryset

    def update(self, request, *args, **kwargs):
        comment = self.get_object()

        if not comment.author_user == self.request.user:
            raise exceptions.AuthenticationFailed(
                detail={'Erreur': 'Vous n\'êtes pas l\'auteur de ce commentaire'})

        data = request.data

        for key, value in data.items():
            setattr(comment, key, value)
        comment.save()
        return Response({'Accept': 'Le commentaire a bien été mis à jour'})

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()

        if comment.author_user != self.request.user:
            raise exceptions.AuthenticationFailed(
                detail={'Erreur': 'Vous n\'êtes pas l\'auteur de ce commentaire'})

        comment.delete()

        return Response({'Accept': 'Le commentaire a bien été supprimé'})
