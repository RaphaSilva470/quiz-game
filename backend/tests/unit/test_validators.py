import pytest
from app.utils.validators import (
    is_valid_email,
    is_strong_password,
    is_valid_username,
    is_valid_category,
    is_valid_difficulty
)

class TestEmailValidator:
    """Testes para validação de email"""
    
    def test_valid_email_standard(self):
        """Teste: Email válido padrão"""
        assert is_valid_email("user@example.com") == True
    
    def test_valid_email_with_subdomain(self):
        """Teste: Email válido com subdomínio"""
        assert is_valid_email("user@mail.example.com") == True
    
    def test_valid_email_with_plus(self):
        """Teste: Email válido com sinal de mais"""
        assert is_valid_email("user+tag@example.com") == True
    
    def test_invalid_email_no_at(self):
        """Teste: Email inválido sem @"""
        assert is_valid_email("userexample.com") == False
    
    def test_invalid_email_no_domain(self):
        """Teste: Email inválido sem domínio"""
        assert is_valid_email("user@") == False
    
    def test_invalid_email_no_tld(self):
        """Teste: Email inválido sem TLD"""
        assert is_valid_email("user@example") == False

class TestPasswordValidator:
    """Testes para validação de senha"""
    
    def test_strong_password_minimum_length(self):
        """Teste: Senha forte com tamanho mínimo"""
        is_valid, error = is_strong_password("123456")
        assert is_valid == True
        assert error is None
    
    def test_strong_password_long(self):
        """Teste: Senha forte longa"""
        is_valid, error = is_strong_password("senha123456789")
        assert is_valid == True
        assert error is None
    
    def test_weak_password_too_short(self):
        """Teste: Senha fraca muito curta"""
        is_valid, error = is_strong_password("12345")
        assert is_valid == False
        assert "mínimo 6" in error.lower()

class TestUsernameValidator:
    """Testes para validação de username"""
    
    def test_valid_username_minimum(self):
        """Teste: Username válido tamanho mínimo"""
        is_valid, error = is_valid_username("abc")
        assert is_valid == True
        assert error is None
    
    def test_valid_username_with_numbers(self):
        """Teste: Username válido com números"""
        is_valid, error = is_valid_username("user123")
        assert is_valid == True
        assert error is None
    
    def test_valid_username_with_underscore(self):
        """Teste: Username válido com underscore"""
        is_valid, error = is_valid_username("user_name")
        assert is_valid == True
        assert error is None
    
    def test_invalid_username_too_short(self):
        """Teste: Username inválido muito curto"""
        is_valid, error = is_valid_username("ab")
        assert is_valid == False
        assert "mínimo 3" in error.lower()
    
    def test_invalid_username_too_long(self):
        """Teste: Username inválido muito longo"""
        long_username = "a" * 51
        is_valid, error = is_valid_username(long_username)
        assert is_valid == False
        assert "máximo 50" in error.lower()
    
    def test_invalid_username_special_chars(self):
        """Teste: Username inválido com caracteres especiais"""
        is_valid, error = is_valid_username("user-name")
        assert is_valid == False
        assert "letras, números e underscore" in error.lower()

class TestCategoryValidator:
    """Testes para validação de categoria"""
    
    def test_valid_category_geografia(self):
        """Teste: Categoria válida geografia"""
        assert is_valid_category("geografia") == True
    
    def test_valid_category_historia(self):
        """Teste: Categoria válida historia"""
        assert is_valid_category("historia") == True
    
    def test_valid_category_none(self):
        """Teste: Categoria None é válida"""
        assert is_valid_category(None) == True
    
    def test_invalid_category(self):
        """Teste: Categoria inválida"""
        assert is_valid_category("invalid") == False

class TestDifficultyValidator:
    """Testes para validação de dificuldade"""
    
    def test_valid_difficulty_facil(self):
        """Teste: Dificuldade válida facil"""
        assert is_valid_difficulty("facil") == True
    
    def test_valid_difficulty_medio(self):
        """Teste: Dificuldade válida medio"""
        assert is_valid_difficulty("medio") == True
    
    def test_valid_difficulty_dificil(self):
        """Teste: Dificuldade válida dificil"""
        assert is_valid_difficulty("dificil") == True
    
    def test_valid_difficulty_none(self):
        """Teste: Dificuldade None é válida"""
        assert is_valid_difficulty(None) == True
    
    def test_invalid_difficulty(self):
        """Teste: Dificuldade inválida"""
        assert is_valid_difficulty("muito_facil") == False

