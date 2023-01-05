from datetime import date

import pytest

from vacancies.models import Vacancy


@pytest.mark.django_db  # Проверит все миграции. Создаст объект в базе а потом откатит её в исходное состояние!
def test_vacancy_list(client, vacancy):


    expected_response = {
        'count': 1,
        'next': None,
        'previous': None,
        'results': [{
            "id": vacancy.pk,
            "created": date.today().strftime('%Y-%m-%d'),
            "skills": [],
            'slug': 'test',
            'text': 'test text',
            'status': "draft",
            "min_experience": None,
            "likes": 0,
            "updated_at": None,
            "user": vacancy.user.pk,
            "username": vacancy.user.username
        }]
    }
    response = client.get('/vacancy/')

    assert response.status_code == 200
    assert response.json() == expected_response
