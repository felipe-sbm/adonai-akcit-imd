"""
Utilitários para manipulação de arquivos.
"""
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


def allowed_file(filename: str, allowed_extensions: set) -> bool:
    """
    Verifica se o arquivo tem extensão permitida.
    
    Args:
        filename: Nome do arquivo
        allowed_extensions: Conjunto de extensões permitidas
        
    Returns:
        True se o arquivo é permitido, False caso contrário
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def save_upload_file(file: FileStorage, upload_folder: str) -> str:
    """
    Salva arquivo enviado de forma segura.
    
    Args:
        file: Arquivo da requisição
        upload_folder: Pasta onde salvar o arquivo
        
    Returns:
        Caminho completo do arquivo salvo
        
    Raises:
        ValueError: Se houver erro ao salvar o arquivo
    """
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        return filepath
    except Exception as e:
        raise ValueError(f"Erro ao salvar arquivo: {str(e)}")


def read_file_content(filepath: str) -> str:
    """
    Lê o conteúdo de um arquivo de forma segura.
    
    Args:
        filepath: Caminho do arquivo
        
    Returns:
        Conteúdo do arquivo
        
    Raises:
        ValueError: Se houver erro ao ler o arquivo
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        raise ValueError(f"Erro ao ler arquivo: {str(e)}")


def get_file_extension(filename: str) -> str:
    """
    Extrai a extensão do arquivo.
    
    Args:
        filename: Nome do arquivo
        
    Returns:
        Extensão do arquivo em minúsculas
    """
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else "txt"


def get_language_from_extension(extension: str) -> str:
    """
    Mapeia extensão de arquivo para linguagem de programação.
    
    Args:
        extension: Extensão do arquivo
        
    Returns:
        Nome da linguagem de programação
    """
    language_map = {
        "py": "Python",
        "js": "JavaScript",
        "ts": "TypeScript",
        "cs": "C#",
        "java": "Java",
        "cpp": "C++",
        "c": "C",
        "razor": "Razor (C#/HTML)",
        "html": "HTML",
        "css": "CSS",
        "json": "JSON",
        "xml": "XML",
    }
    return language_map.get(extension, extension.upper())
