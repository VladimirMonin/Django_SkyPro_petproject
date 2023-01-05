from datetime import date
import pytest

from tests.factories import VacancyFactory
from vacancies.serializers import VacancySerializer

@pytest.mark.django_db  # Проверит все миграции. Создаст объект в базе а потом откатит её в исходное состояние!
def test_vacancy_list(client):
    vacancies = VacancyFactory.create_batch(5)  # создаем список объектов вакансий
    expected_response = {
        'count': 5,
        'next': None,
        'previous': None,
        'results': VacancySerializer(vacancies, many=True).data  # Используем сериалайзер для проверки данных
    }
    response = client.get('/vacancy/')

    assert response.status_code == 200
    assert response.json() == expected_response
