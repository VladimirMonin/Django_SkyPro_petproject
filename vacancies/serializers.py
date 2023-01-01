from rest_framework import serializers  # импорт подтягивается плохо - можно делать вручную

from vacancies.models import Vacancy, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class VacancySerializer(serializers.ModelSerializer):
    #  тут мы можем как добавить новое поле, так и переопределить поле модели
    username = serializers.CharField()  # username в модели нет - но мы можем добавить в сериализатор (а данные
    # добавляются во вьюшке)
    skills = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'  # На какое поле модели skills мы будем ссылаться
    )

    class Meta:
        model = Vacancy  # Модель, которую будем прогонять
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
    id = serializers.IntegerField(
        required=False)  # Добавили поле ID (объявления) - т.к. оно не передается при создании - указали что
    # required=False
    skills = serializers.SlugRelatedField(  # Показали что работаем и со скилами
        required=False,
        many=True,
        queryset=Skill.objects.all(),  # Когда мы перестаем использовать только для чтения - нужно давать queryset
        slug_field='name'
    )

    class Meta:
        model = Vacancy
        fields = '__all__'  # Исключили эти поля - они не идут на вход при создании вакансии

    # Когда мы передадим скилл которого нет в базе, проверка попытается достать это
    # В квери сете, и упадет. Чтобы этого не случилось прячем их от валидатора, чтобы пройтись по ним самим
    def is_valid(self, raise_exception=False):
        self._skills = self.initial_data.pop('skills', [])  # Вытащили по ключу skills всё что прислал юзер
        return super().is_valid(raise_exception=raise_exception)  # Вернули поведение "по умолчанию"

    # Переопределяем метод create - он принимает валидированные данные
    def create(self, validated_data):
        vacancy = Vacancy.objects.create(**validated_data)
        # Проходимся самостоятельно по скиллам - вытаскиваем или создаем
        for skill in self._skills:
            skill_object, _ = Skill.objects.get_or_create(name=skill)
            vacancy.skills.add(skill_object)

        vacancy.save()
        return vacancy


class VacancyUpdateSerializer(VacancyCreateSerializer):  # важный момент - ограничить перезапись IP
    id = serializers.IntegerField(read_only=True)
    created = serializers.DateField(read_only=True)
    user = serializers.CharField(read_only=True)

    def save(self):
        vacancy = super().save()
        for skill in self._skills:
            skill_object, _ = Skill.objects.get_or_create(name=skill)
            vacancy.skills.add(skill_object)

        vacancy.save()
        return vacancy


class VacancyDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ['id']
