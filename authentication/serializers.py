from rest_framework import serializers

from authentication.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = super().create(validated_data)  # сохраняем пользователя со всеми проверками
        user.set_password(user.password)   # встроенный метод set_password - хешируем пароль

        user.save()  # сохраняем пользователя
        return user  # возвращаем пользователя - как если бы мы были родительским методом

