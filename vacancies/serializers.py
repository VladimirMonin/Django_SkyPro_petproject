from rest_framework import serializers  # импорт подтягивается плохо - можно делать вручную

from vacancies.models import Vacancy


class VacancySerializer(serializers.ModelSerializer):
    #  тут мы можем как добавить новое поле, так и переопределить поле модели
    username = serializers.CharField()  # username в модели нет - но мы можем добавить в сериализатор (а данные добавляются во вьюшке)
    skills = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'  # На какое поле модели skills мы будем ссылаться
    )

    class Meta:
        model = Vacancy  # Модель которую будем прогонять
        fields = ['id', 'text', 'slug', 'status', 'created',
                  'username', 'skills']  # Поля (тут можно сделать исключения, или просто указать __all__


class VacancyDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField()  # если добавить сюда эту строку - будет подтягиваться Юзернейм!!!
    skills = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'  # На какое поле модели skills мы будем ссылаться
    )

    class Meta:
        model = Vacancy  # Модель которую будем прогонять
        fields = '__all__'
