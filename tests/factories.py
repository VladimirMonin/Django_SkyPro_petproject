import factory.django

from authentication.models import User
from vacancies.models import Vacancy


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = 'test'
    password = 'testtest'


class VacancyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vacancy

    slug = 'test'
    text = 'test text'
    status = "draft"
    user = factory.SubFactory(UserFactory)