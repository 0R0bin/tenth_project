import app_projects.serializers as pSerializers
import app_projects.models as pModels
from rest_framework.viewsets import ModelViewSet
from itertools import chain


class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()
    

class ProjectsViewSet(MultipleSerializerMixin, ModelViewSet):
    """
    Vue User des projets
    On renvoie les projets de l'utilisateur (table Contributors) + Création / PUT / DEL des réservation
    """

    serializer_class = pSerializers.ProjectListSerializer
    detail_serializer_class = pSerializers.ProjectDetailsSerializer

    def get_queryset(self):
        queryset_contributors = pModels.Contributors.objects.filter(author_user_id=self.request.user)
        final_queryset = pModels.Projects.objects.filter(id__in = queryset_contributors.values('project_id'))
            
        return final_queryset