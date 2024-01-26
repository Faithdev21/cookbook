from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class ListCreateRetrieveDestroy(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.DestroyModelMixin,
                                GenericViewSet):
    """Класс, включающий в себя list, create, destroy,retrieve методы."""
