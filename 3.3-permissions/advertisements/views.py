from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter, FavoriteFilter
from advertisements.models import Advertisement, Favorite
from advertisements.permissions import IsOwnerOrReadOnly, IsNotOwner
from advertisements.serializers import AdvertisementSerializer, FavoriteSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'delete']:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []


class FavoriteViewSet(ModelViewSet):
    """ViewSet для избранного."""
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, IsNotOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FavoriteFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsNotOwner()]
        return []