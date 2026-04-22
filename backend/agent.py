"""
Agente de IA para Code Review usando Groq API com múltiplas técnicas.
"""
import os
import logging
import re
from openai import OpenAI


# Configurar logging
logger = logging.getLogger(__name__)


class CodeReviewAgent:
    """Agente que analisa código em múltiplas etapas para fornecer feedback estruturado."""

    _EMOTION_PATTERN = re.compile(r"^\s*EMOCAO:\s*([a-z0-9_]+)\s*$", re.IGNORECASE)

    def __init__(self, understanding_prompt: str, review_prompt: str):
        """Inicializa o agente de code review."""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY não configurada")

        # Groq usa API compatível com OpenAI
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.understanding_prompt = understanding_prompt
        self.review_prompt = review_prompt
        logger.info(f"Agente inicializado com modelo: {self.model}")

    def _understand_code(self, code: str, task: str, filename: str, language: str) -> str:
        """
        Etapa 1: Entender o código.

        Args:
            code: Conteúdo do arquivo de código
            task: Descrição da tarefa/problema do usuário
            filename: Nome do arquivo
            language: Linguagem de programação

        Returns:
            Compreensão do código
        """
        user_message = f"""**Arquivo:** {filename}
**Linguagem:** {language}
**Tarefa do usuário:** {task}

**Código a ser analisado:**
```
{code}
```

Por favor, faça uma análise de compreensão do código acima."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.understanding_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.2,
                max_tokens=2048,
            )
            understanding = response.choices[0].message.content
            logger.info(f"Etapa 1 (Compreensão) concluída para: {filename}")
            return understanding

        except Exception as e:
            logger.error(f"Erro na etapa de compreensão: {str(e)}")
            raise

    def _review_code(self, code: str, understanding: str, task: str, filename: str, language: str) -> str:
        """
        Etapa 2: Revisar o código baseado na compreensão.

        Args:
            code: Conteúdo do arquivo de código
            understanding: Resultado da análise de compreensão
            task: Descrição da tarefa/problema do usuário
            filename: Nome do arquivo
            language: Linguagem de programação

        Returns:
            Revisão detalhada do código
        """
        user_message = f"""**Arquivo:** {filename}
**Linguagem:** {language}
**Tarefa do usuário:** {task}

**Análise prévia do código:**
{understanding}

**Código a ser revisado:**
```
{code}
```

Baseado na análise acima, forneça uma revisão detalhada do código."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.review_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
                max_tokens=4096,
            )
            review = response.choices[0].message.content
            logger.info(f"Etapa 2 (Revisão) concluída para: {filename}")
            return review

        except Exception as e:
            logger.error(f"Erro na etapa de revisão: {str(e)}")
            raise

    def _extract_emotion_from_review(self, review_text: str) -> tuple[str, str]:
        """
        Extrai a emoção da linha obrigatória `EMOCAO: <id>`.

        Returns:
            Tupla com (emotion_id, review_sem_linha_de_emocao)
        """
        emotion = "explicativa"
        cleaned_lines = []

        for line in review_text.splitlines():
            match = self._EMOTION_PATTERN.match(line)
            if match:
                emotion = match.group(1).lower()
                continue
            cleaned_lines.append(line)

        cleaned_review = "\n".join(cleaned_lines).strip()
        return emotion, cleaned_review

    def review(self, code: str, task: str, filename: str) -> dict:
        """
        Analisa o código em múltiplas etapas e retorna feedback estruturado.

        Args:
            code: Conteúdo do arquivo de código
            task: Descrição da tarefa/problema do usuário
            filename: Nome do arquivo para contexto

        Returns:
            Dicionário com etapas de análise:
            {
                "understanding": "Compreensão do código...",
                "review": "Revisão detalhada...",
                "summary": "Resumo executivo..."
            }
        """
        # Detectar linguagem pela extensão
        extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else "txt"
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
        language = language_map.get(extension, extension.upper())

        try:
            logger.info(f"Iniciando análise do arquivo: {filename}")

            # Etapa 1: Entender o código
            logger.info("Etapa 1: Compreendendo o código...")
            understanding = self._understand_code(code, task, filename, language)

            # Etapa 2: Revisar o código
            logger.info("Etapa 2: Revisando o código...")
            raw_review = self._review_code(code, understanding, task, filename, language)
            emotion, review = self._extract_emotion_from_review(raw_review)

            # Criar resumo executivo
            summary = f"""## 📋 Resumo Executivo

**Arquivo:** {filename}
**Linguagem:** {language}
**Tarefa:** {task}

---

### ✅ Etapa 1: Compreensão do Código
{understanding}

---

### 🔍 Etapa 2: Revisão Detalhada
{review}

---

**Análise concluída com sucesso!**"""

            result = {
                "status": "success",
                "emotion": emotion,
                "understanding": understanding,
                "review": review,
                "summary": summary,
            }

            logger.info(f"Análise completa concluída para: {filename}")
            return result

        except Exception as e:
            logger.error(f"Erro durante análise do código: {str(e)}")
            return {
                "status": "error",
                "error": f"❌ Erro ao processar com IA: {str(e)}",
            }
