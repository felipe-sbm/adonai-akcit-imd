"""
Schemas (validação) para requisições de code review.
"""
from dataclasses import dataclass


@dataclass
class CodeReviewRequest:
    """Schema para requisição de code review."""
    
    filename: str
    task: str
    code_content: str
    
    def validate(self) -> list[str]:
        """
        Valida os dados da requisição.
        
        Returns:
            Lista de erros (vazia se válido)
        """
        errors = []
        
        if not self.filename or not self.filename.strip():
            errors.append("Nome do arquivo é obrigatório")
            
        if not self.task or not self.task.strip():
            errors.append("Descrição da tarefa é obrigatória")
            
        if not self.code_content or not self.code_content.strip():
            errors.append("Código para análise é obrigatório")
            
        return errors


@dataclass
class CodeReviewResponse:
    """Schema para resposta de code review."""
    
    status: str
    filename: str
    task: str
    code_preview: str
    ai_response: str
    
    def to_dict(self) -> dict:
        """Converte para dicionário."""
        return {
            "status": self.status,
            "filename": self.filename,
            "task": self.task,
            "code_preview": self.code_preview,
            "ai_response": self.ai_response,
        }
