from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from authentication.models import User


def check_date_not_past(value: date):
    if value < date.today():
        raise ValidationError(f'{value} is in the past.')


class Skill(models.Model):
    name = models.CharField(max_length=25)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    def __str__(self):
        return self.name  # То что будет отображаться в заголовках админки


class Vacancy(models.Model):
    STATUS = [  # Константа со списком вариантов поля статус. Это список картежей.
        # Первое значение для базы, второе - человеко читаемое (пользователю АДМИНКИ)
        ('draft', 'Черновик'),
        ('open', 'Открыта'),
        ('closed', 'Закрыта'),
    ]

    slug = models.SlugField(max_length=100)
    text = models.CharField(max_length=2000)
    status = models.CharField(max_length=6, choices=STATUS,
                              default='draft')  # Тут может быть 3 значения. Они называются енамами (т.е.
    # Перечислениям) указываются как константа сверху. Второй аргумент - выбор вариантов, третий, значение по
    # умолчанию
    # created = models.DateField(default=datetime.date.now()) # Оно будет работать. Но есть более элегантный метод
    created = models.DateField(auto_now_add=True)  # Поставь текущее время на момент создания ;)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                             blank=True)  # ОДИН КО МНОГИМ. Внешний ключ принимает название модели с которой
    # Связываемся.
    # Обязательный атрибут on_delete - если удаляем пользователя вероятно хотим удалить все его вакансии. Так же мы
    # не прописали ID - они будут созданы за нас. Поле может быть null
    skills = models.ManyToManyField(
        Skill)  # Добавили связь МНОГИЕ КО МНОГИМ. Джанго сделает всё сам. Кстати, это не поле а связь

    likes = models.IntegerField(default=0)
    min_experience = models.IntegerField(null=True, validators=[MinValueValidator(0)])  # null - для того, чтобы не
    # постарадали имеющиеся данные, валидатор не позволит указать отрицательный опыт
    updated_at = models.DateField(null=True, validators=[check_date_not_past])  # Функция написана выше, райзит
    # ValidationError если добавляют время в прошлом - добавлено в список без вызова(!)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        # ordering = ['id']  # в списке колонки для сортировки

    def __str__(self):
        return self.text  # То что будет отображаться в заголовках админки

    #  Добавляем username через модель. Будет его возвращать, иначе None
    @property  # чтобы сделать его атрибутом модели
    def username(self):
        return self.user.username if self.user else None
