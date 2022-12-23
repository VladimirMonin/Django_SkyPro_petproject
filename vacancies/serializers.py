from rest_framework import serializers  # импорт подтягивается плохо - можно делать вручную

from vacancies.models import Vacancy


class VacancySerializer(serializers.ModelSerializer):
    username = serializers.CharField()  # username в модели нет - но мы можем добавить в сериализатор (а данные добавляются во вьюшке)
    class Meta:
        model = Vacancy  # Модель которую будем прогонять
        fields = ['id', 'text', 'slug', 'status', 'created', 'username']  # Поля (тут можно сделать исключения, или просто указать __all__


