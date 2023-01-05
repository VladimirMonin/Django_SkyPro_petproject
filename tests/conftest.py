from pytest_factoryboy import register

from tests.factories import VacancyFactory, UserFactory

pytest_plugins = 'tests.fixtures'  # Если фикстуры лежат отдельным файлом, это надо указать тут
register(VacancyFactory)
register(UserFactory)
