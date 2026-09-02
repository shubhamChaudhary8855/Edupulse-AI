from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_register_and_login():
    email = 'test-user@example.com'
    password = 'StrongPassword123!'

    register = client.post('/api/v1/auth/register', json={'email': email, 'password': password})
    assert register.status_code in (200, 409)

    login = client.post('/api/v1/auth/login', json={'email': email, 'password': password})
    assert login.status_code == 200
    assert login.json()['access_token']


def test_protected_document_endpoint():
    response = client.post('/api/v1/documents', json={'title': 'Test', 'content': 'Library is open Monday to Saturday.'})
    assert response.status_code == 401
