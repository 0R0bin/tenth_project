class MultipleSerializerMixin:

    detail_serializer_class = None
    create_serializer_class = None
    put_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        if self.action == 'create' and self.create_serializer_class is not None:
            return self.create_serializer_class
        if (self.action == 'update' or self.action == 'partial_update') and self.put_serializer_class is not None:
            return self.put_serializer_class
        return super().get_serializer_class()