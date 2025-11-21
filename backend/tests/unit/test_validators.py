import pytest
from app.utils.validators import (
    is_valid_email,
    is_strong_password,
    is_valid_username,
    is_valid_category,
    is_valid_difficulty
)


class TestIsValidEmail:
    """Testes para is_valid_email"""
    
    def test_should_return_true_for_valid_email(self):
        assert is_valid_email("test@example.com") is True
        assert is_valid_email("user.name@domain.co.uk") is True
        assert is_valid_email("user+tag@example.org") is True
    
    def test_should_return_false_for_invalid_email(self):
        assert is_valid_email("invalid") is False
        assert is_valid_email("invalid@") is False
        assert is_valid_email("@domain.com") is False
        assert is_valid_email("user@") is False
        assert is_valid_email("") is False


class TestIsStrongPassword:
    """Testes para is_strong_password"""
    
    def test_should_return_true_for_valid_password(self):
        is_valid, error = is_strong_password("senha123")
        assert is_valid is True
        assert error is None
    
    def test_should_return_false_for_short_password(self):
        is_valid, error = is_strong_password("12345")
        assert is_valid is False
        assert "mínimo 6" in error.lower()
    
    def test_should_return_true_for_long_password(self):
        is_valid, error = is_strong_password("senha_muito_longa_123")
        assert is_valid is True
        assert error is None


class TestIsValidUsername:
    """Testes para is_valid_username"""
    
    def test_should_return_true_for_valid_username(self):
        is_valid, error = is_valid_username("user123")
        assert is_valid is True
        assert error is None
    
    def test_should_return_false_for_short_username(self):
        is_valid, error = is_valid_username("ab")
        assert is_valid is False
        assert "mínimo 3" in error.lower()
    
    def test_should_return_false_for_long_username(self):
        is_valid, error = is_valid_username("a" * 51)
        assert is_valid is False
        assert "máximo 50" in error.lower()
    
    def test_should_return_false_for_username_with_special_chars(self):
        is_valid, error = is_valid_username("user@name")
        assert is_valid is False
        assert "letras, números e underscore" in error.lower()


class TestIsValidCategory:
    """Testes para is_valid_category"""
    
    def test_should_return_true_for_valid_categories(self):
        assert is_valid_category("geografia") is True
        assert is_valid_category("historia") is True
        assert is_valid_category("ciencias") is True
        assert is_valid_category("esportes") is True
        assert is_valid_category("geral") is True
        assert is_valid_category(None) is True
    
    def test_should_return_false_for_invalid_category(self):
        assert is_valid_category("invalida") is False
        assert is_valid_category("") is False


class TestIsValidDifficulty:
    """Testes para is_valid_difficulty"""
    
    def test_should_return_true_for_valid_difficulties(self):
        assert is_valid_difficulty("facil") is True
        assert is_valid_difficulty("medio") is True
        assert is_valid_difficulty("dificil") is True
        assert is_valid_difficulty(None) is True
    
    def test_should_return_false_for_invalid_difficulty(self):
        assert is_valid_difficulty("invalida") is False
        assert is_valid_difficulty("") is False

