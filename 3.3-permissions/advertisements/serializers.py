from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, Favorite


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        # TODO: добавьте требуемую валидацию
        creator = self.context['request'].user
        # if not self.instance:
        if not self.instance or data.get('status') == 'OPEN':
            if Advertisement.objects.filter(creator=creator).count() > 9:
                raise serializers.ValidationError(f'Превышено число открытых объявлений')
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    person = UserSerializer(
        read_only=True,
    )
    advertisement = AdvertisementSerializer(
        read_only=True
    )

    class Meta:
        model = Favorite
        fields = ('person', 'advertisement', )

    def create(self, validated_data):
        """Метод для создания"""
        validated_data['person'] = self.context['request'].user
        validated_data['advertisement'] = self.context['request']['advertisement']
        return super().create(validated_data)