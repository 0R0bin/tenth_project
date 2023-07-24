import app_projects.serializers as pSerializers
import app_projects.models as pModels

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets, mixins


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
        if self.request.user.is_authenticated:
            queryset_contributors = pModels.Contributors.objects.filter(user=self.request.user)
            final_queryset = pModels.Projects.objects.filter(id__in = queryset_contributors.values('project_id'))
            return final_queryset
        else:
            return None
        
        

class ContributorsViewSet(MultipleSerializerMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    Vue User des contributeurs
    On renvoie les utilisateurs contributeurs du projet (table Contributors) + Ajout d'un contributeur / DEL d'un contributeur
    """

    serializer_class = pSerializers.ContributorListSerializer
    detail_serializer_class = pSerializers.ContributorDetailsSerializer

    def get_queryset(self):
        project_id_sent = self.kwargs['project_id']
        queryset = pModels.Contributors.objects.filter(project_id=project_id_sent)
        
        return queryset
