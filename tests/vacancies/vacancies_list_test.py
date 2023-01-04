from datetime import date

import pytest

from vacancies.models import Vacancy


@pytest.mark.django_db  # Проверит все миграции. Создаст объект в базе а потом откатит её в исходное состояние!
def test_vacancy_list(client):
    vacancy = Vacancy.objects.create(
        slug='123',
        text='123'
    )

    expected_response = {
        'count': 1,
        'next': None,
        'previous': None,
        'results': [{
            'id': vacancy.id,
            'text': '123',
            'slug': '123',
            'status': 'draft',
            'created': date.today().strftime('%Y-%m-%d'),
            'likes': 0,
            'min_experience': None,
            'updated_at': None,
            'username': None,
            'user': None,
            'skills': []
        }]
    }
    response = client.get('/vacancy/')

    assert response.status_code == 200
    assert response.json() == expected_response
