import accounts.models as accModels
import accounts.serializers as accSerializers

from softdeskapi.mixin_serializer import MultipleSerializerMixin
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


# Classe pour info son user
class UserViewSet(MultipleSerializerMixin, ModelViewSet):

    serializer_class = accSerializers.UserFullSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = accModels.CustomUser.objects.filter(pk=self.request.user.pk)
        return queryset


# Classe pour créer un user
class CreateUserViewSet(MultipleSerializerMixin, mixins.CreateModelMixin,
                        mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = accSerializers.CustomUserSerializer
    create_serializer_class = accSerializers.CustomUserSerializer

    def get_queryset(self):
        return None
