import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_user_login():
    user = User.objects.create_user(
        username="testlogin",
        email="login@example.com",
        password="securepassword"
    )

    client = APIClient()
    response = client.post("/api/users/token/", {
        "username": "testlogin",
        "password": "securepassword"
    })

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data
