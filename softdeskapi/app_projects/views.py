import app_projects.serializers as pSerializers
import app_projects.models as pModels

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions


class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectsViewSet(MultipleSerializerMixin, ModelViewSet):
    """
    Vue User des projets
    On renvoie les projets de l'utilisateur (table Contributors)
    Création / PUT / DEL des réservation
    """

    permission_classes = [IsAuthenticated]

    serializer_class = pSerializers.ProjectListSerializer
    detail_serializer_class = pSerializers.ProjectDetailsSerializer

    def get_queryset(self):
        queryset_contributors = pModels.Contributors.objects.filter(user=self.request.user)
        final_queryset = pModels.Projects.objects.filter(
            id__in=queryset_contributors.values('project_id'))
        return final_queryset

    def update(self, request, *args, **kwargs):
        project = self.get_object()
        user_contributors = pModels.Contributors.objects.filter(project=project)
        user_contributor = user_contributors.get(user=self.request.user)

        if not user_contributor.permission == 'AUT':
            raise exceptions.AuthenticationFailed({'Erreur': "Vous n'êtes pas auteur de ce projet"})

        data = request.data
        for key, value in data.items():
            setattr(project, key, value)
        project.save()
        return Response({'Accept': 'Le projet a bien été mis à jour'})

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        user_contributors = pModels.Contributors.objects.filter(project=project)
        user_contributor = user_contributors.get(user=self.request.user)

        if not user_contributor.permission == 'AUT':
            raise exceptions.AuthenticationFailed({'Erreur': "Vous n'êtes pas auteur de ce projet"})

        project.delete()

        return Response({'Accept': 'Le projet a bien été supprimé'})


class ContributorsViewSet(MultipleSerializerMixin, mixins.RetrieveModelMixin,
                          mixins.CreateModelMixin, mixins.ListModelMixin,
                          mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    Vue User des contributeurs
    On renvoie les utilisateurs contributeurs du projet (table Contributors)
    Ajout d'un contributeur / DEL d'un contributeur
    """

    permission_classes = [IsAuthenticated]

    serializer_class = pSerializers.ContributorListSerializer
    detail_serializer_class = pSerializers.ContributorDetailsSerializer

    def get_queryset(self):
        project_id_sent = self.kwargs['project_id']
        queryset = pModels.Contributors.objects.filter(project_id=project_id_sent)

        return queryset

    def destroy(self, request, *args, **kwargs):
        project_id = kwargs['project_id']
        user_contributors = pModels.Contributors.objects.filter(project_id=project_id)
        user_contributor = user_contributors.get(user=self.request.user)

        if user_contributor.permission == 'AUT':
            contributor_to_delete = self.get_object()
            contributor_to_delete.delete()
        else:
            res = exceptions.ValidationError({'Erreur': "Vous n'êtes pas auteur de ce projet"})
            res.status_code = 401
            raise res

        return Response({'Accept': 'Le contributeur a bien été supprimé'})
