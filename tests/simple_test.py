def test_root_not_found(client):  # встроенная фикстура client умеет делать запросы
    response = client.get('/')
    assert response.status_code == 404
