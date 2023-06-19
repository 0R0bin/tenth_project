import accounts.serializers as accSerializers
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()
    

# Classe pour créer un user
class CreateUserViewSet(MultipleSerializerMixin, ModelViewSet):

    serializer_class = accSerializers.CustomUserSerializer

    def get_queryset(self):
        return None
