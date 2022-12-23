from rest_framework import serializers  # импорт подтягивается плохо - можно делать вручную

from vacancies.models import Vacancy, Skill


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


class VacancyCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)  # Добавили поле ID (объявления) - т.к. оно не передается при создании - указали что required=False
    skills = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Skill.objects.all(),  # Когда мы перестаем использовать только для чтения - нужно давать queryset
        slug_field='name'
    )
    class Meta:
        model = Vacancy
        fields = '__all__'  # Исключили эти поля - они не идут на вход при создании вакансии

    def is_valid(self, raise_exeption=False):
        self._skills = self.initial_data.pop('skills')
        return super().is_valid(raise_exeption=raise_exeption)