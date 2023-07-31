import tickets.models as tModels
import tickets.serializers as tSerializers
import app_projects.models as appPModels

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions


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

        if appPModels.Contributors.objects.filter(project_id=project_id_sent).filter(user=user_log).exists():
            queryset = tModels.Issues.objects.filter(project_id=project_id_sent)
            return queryset
        else:
            res = exceptions.ValidationError({'Erreur': "Vous n'êtes affilié à ce projet"})
            res.status_code = 401
            raise res

class CommentViewSet(MultipleSerializerMixin,  ModelViewSet):
    """
    Vue des commentaires d'un projet
    On renvoie les commentaires de l'issue (table Comments)
    Full CRUD
    """

    serializer_class = tSerializers.CommentsListSerializer
    detail_serializer_class = tSerializers.CommentsDetailsSerializer

    def get_queryset(self):
        issue_id_sent = self.kwargs['issue_id']
        queryset = tModels.Comments.objects.filter(issue_id=issue_id_sent)
        
        return queryset
