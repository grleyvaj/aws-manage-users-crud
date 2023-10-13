import pytest
from pydantic import ValidationError

from my_cognito_lambda.models.user_create import UserCreate


def test_create_valid_user():
    user_data = {
        "name": "Gloria",
        "last_name": "Leyva",
        "charge": "Developer",
        "email": "glorialj@example.com"
    }
    user = UserCreate(**user_data)
    assert user.name == "Gloria"
    assert user.last_name == "Leyva"
    assert user.charge == "Developer"
    assert user.email == "glorialj@example.com"


# Prueba de longitud mínima no cumplida
def test_name_too_short():
    user_data = {
        "name": "G",
        "last_name": "Leyva",
        "charge": "Developer",
        "email": "glorialj@example.com"
    }
    with pytest.raises(ValidationError):
        UserCreate(**user_data)


def test_name_too_long():
    user_data = {
        "name": "Gloria" * 10,  # Esto excederá el límite máximo de 30 caracteres
        "last_name": "Leyva",
        "charge": "Developer",
        "email": "glorialj@example.com"
    }
    with pytest.raises(ValidationError):
        UserCreate(**user_data)


def test_invalid_email():
    user_data = {
        "name": "Gloria",
        "last_name": "Leyva",
        "charge": "Developer",
        "email": "glorialj"  # Esto no es una dirección de correo electrónico válida
    }
    with pytest.raises(ValidationError):
        UserCreate(**user_data)
