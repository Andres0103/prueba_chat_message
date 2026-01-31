#Test para content_filter.py en domain services
import pytest
from src.Domain.services.content_filter import ContentFilterService

#test cases para ContentFilterService para contenido inapropiado y sanitización
class TestContentFilterServiceDetection:

    #Debe detectar palabras inapropiadas en el contenido
    def test_contains_inappropriate_content_with_spam(self):
        content = "Esto es contenido spam"
        assert ContentFilterService.contains_inappropriate_content(content) is True

    #Debe detectar 'malware' en el contenido
    def test_contains_inappropriate_content_with_malware(self):
        content = "Peligro: malware detectado"
        assert ContentFilterService.contains_inappropriate_content(content) is True

    #Debe detectar 'hack' en el contenido
    def test_contains_inappropriate_content_with_hack(self):
        content = "No haga un hack al sistema"
        assert ContentFilterService.contains_inappropriate_content(content) is True

    #Debe detectar 'scam' en el contenido
    def test_contains_inappropriate_content_with_scam(self):
        content = "Esto es un scam"
        assert ContentFilterService.contains_inappropriate_content(content) is True

    #Debe detectar palabras inapropiadas sin importar mayúsculas/minúsculas
    def test_contains_inappropriate_content_case_insensitive(self):
        contents = [
            "Esto es Contenido SPAM",
            "Esto es Spam",
            "Esto es spaM",
            "Esto es MALWARE",
            "Esto es HACK",
            "Esto es SCAM",
        ]
        for content in contents:
            assert ContentFilterService.contains_inappropriate_content(content) is True

    #No debe detectar contenido limpio como inapropiado
    def test_contains_inappropriate_content_with_clean_content(self):
        content = "Esto es un mensaje limpio"
        assert ContentFilterService.contains_inappropriate_content(content) is False

    #Debe manejar cadena vacía correctamente
    def test_contains_inappropriate_content_with_empty_string(self):
        content = ""
        assert ContentFilterService.contains_inappropriate_content(content) is False

#Tests para la sanitización de contenido
class TestContentFilterServiceSanitization:

    #Debe eliminar espacios en blanco al inicio
    def test_sanitize_content_removes_leading_whitespace(self):
        content = "   hello world"
        sanitized = ContentFilterService.sanitize_content(content)
        assert sanitized == "hello world"

    #Debe eliminar espacios en blanco al final
    def test_sanitize_content_removes_trailing_whitespace(self):
        content = "hello world   "
        sanitized = ContentFilterService.sanitize_content(content)
        assert sanitized == "hello world"

    #Debe eliminar espacios en blanco en ambos extremos
    def test_sanitize_content_removes_both_ends_whitespace(self):
        content = "   hello world   "
        sanitized = ContentFilterService.sanitize_content(content)
        assert sanitized == "hello world"

#Tests para el método principal filter()
class TestContentFilterServiceFilter:

    #Debe retornar contenido limpio sin cambios
    def test_filter_clean_content_returns_content(self):
        content = "Hello world"
        result = ContentFilterService().filter(content)
        assert result == "Hello world"

    #Debe sanitizar el contenido antes de verificar palabras inapropiadas
    def test_filter_sanitizes_content_before_checking(self):
        content = "   Hello world   "
        result = ContentFilterService().filter(content)
        assert result == "Hello world"

    #Debe lanzar ValueError si se detecta 'spam'
    def test_filter_raises_error_for_spam(self):
        content = "Compra este spam ahora"
        with pytest.raises(ValueError, match="El mensaje contiene palabras inapropiadas"):
            ContentFilterService().filter(content)

    #Debe lanzar ValueError si se detecta 'malware'
    def test_filter_raises_error_for_malware(self):
        content = "Este es malware"
        with pytest.raises(ValueError, match="El mensaje contiene palabras inapropiadas"):
            ContentFilterService().filter(content)
    
    #Debe lanzar ValueError si se detecta 'hack'
    def test_filter_raises_error_for_hack(self):
        content = "No hagas un hack al sistema"
        with pytest.raises(ValueError, match="El mensaje contiene palabras inapropiadas"):
            ContentFilterService().filter(content)
    
    #Debe lanzar ValueError si se detecta 'scam'
    def test_filter_raises_error_for_scam(self):
        with pytest.raises(ValueError, match="El mensaje contiene palabras inapropiadas"):
            ContentFilterService().filter("SCAM detectado")

    #Debe detectar múltiples palabras inapropiadas
    def test_filter_with_multiple_inappropriate_words(self):
        with pytest.raises(ValueError):
            ContentFilterService().filter("spam y malware y hack y scam")

#Tests para el método estático legacy filter_content()
class TestContentFilterServiceFilterContent:

    #Debe retornar (True, '') para contenido limpio
    def test_filter_content_returns_true_for_clean_content(self):
        content = "Hola, cómo puedo ayudarte?"
        is_valid, error = ContentFilterService.filter_content(content)

        assert is_valid is True
        assert error == ""

    #Debe retornar (False, error_msg) para contenido inapropiado
    def test_filter_content_returns_false_for_inappropriate(self):
        content = "Compra este malware ahora!"
        is_valid, error = ContentFilterService.filter_content(content)

        assert is_valid is False
        assert error == "El mensaje contiene palabras inapropiadas"

    #Debe detectar spam en el contenido
    def test_filter_content_with_spam(self):
        content = "Este es un mensaje spam"
        is_valid, error = ContentFilterService.filter_content(content)

        assert is_valid is False

    #Debe detectar hack en el contenido
    def test_filter_content_with_hack(self):
        content = "Aprende a hacer un hack al sistema"
        is_valid, error = ContentFilterService.filter_content(content)

        assert is_valid is False

    #Debe sanitizar antes de verificar contenido inapropiado
    def test_filter_content_sanitizes_before_checking(self):
        content = "   mensaje limpio   "
        is_valid, error = ContentFilterService.filter_content(content)

        assert is_valid is True
        assert error == ""

    #Debe eliminar espacios extra en la sanitización
    def test_sanitize_content_removes_extra_spaces(self):
        content = "  Hello world  "
        sanitized = ContentFilterService.sanitize_content(content)

        assert sanitized == "Hello world"

    #Debe detectar contenido inapropiado sin importar mayúsculas/minúsculas
    def test_case_insensitive_filtering(self):
        content = "Esto es SPAM"
        assert ContentFilterService.contains_inappropriate_content(content) is True

    #Debe manejar cadena vacía correctamente
    def test_empty_content_is_valid(self):
        is_valid, error = ContentFilterService.filter_content("")
        assert is_valid is True
        assert error == ""

    #Debe detectar contenido inapropiado después de la sanitización
    def test_filtering_after_sanitization(self):
        content = "   spam   "
        is_valid, error = ContentFilterService.filter_content(content)

        assert is_valid is False

    #Debe detectar palabra inapropiada dentro de una oración
    def test_inappropriate_word_inside_sentence(self):
        content = "Hola, este mensaje contiene spam dentro."
        assert ContentFilterService.contains_inappropriate_content(content) is True
