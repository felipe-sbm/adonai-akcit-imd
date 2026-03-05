"""
Configurações da aplicação Flask.
"""
import os
import tempfile


class Config:
    """Configurações base da aplicação."""
    
    # Flask
    DEBUG = False
    TESTING = False
    
    # Upload (fora da pasta do projeto para evitar restart do reloader durante upload)
    UPLOAD_FOLDER = os.getenv(
        "AKCIT_UPLOAD_DIR",
        os.path.join(tempfile.gettempdir(), "akcit-agent-uploads"),
    )
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB
    
    ALLOWED_EXTENSIONS = {
        "cs", "js", "ts", "py", "java", "cpp", "c", "razor",
        "html", "css", "json", "xml", "txt", "md"
    }
    
    # API
    API_VERSION = "v1"
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    """Configurações para desenvolvimento."""
    DEBUG = True


class TestingConfig(Config):
    """Configurações para testes."""
    TESTING = True


class ProductionConfig(Config):
    """Configurações para produção."""
    DEBUG = False


def get_config():
    """Retorna a configuração apropriada baseada no ambiente."""
    env = os.getenv("FLASK_ENV", "development")
    
    config_map = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }
    
    return config_map.get(env, DevelopmentConfig)
