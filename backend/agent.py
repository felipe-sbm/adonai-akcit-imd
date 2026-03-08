"""
Agente de IA para Code Review usando Groq API com múltiplas técnicas.
"""
import os
import logging
from openai import OpenAI


# Configurar logging
logger = logging.getLogger(__name__)


class CodeReviewAgent:
    """Agente que analisa código em múltiplas etapas para fornecer feedback estruturado."""

    UNDERSTANDING_PROMPT = """Você é uma especialista em análise de código chamada Adonai.
Sua tarefa é entender e mapear o código fornecido.

Analise o código e responda:
1. Qual é a função/objetivo principal do código?
2. Quais são as funções/classes principais?
3. Qual é o fluxo lógico?
4. Quais dependências externas há?
5. Qual é a complexidade geral?

Seja conciso mas completo na análise.
Responda em português brasileiro"""

    REVIEW_PROMPT = """Você é um especialista em revisão de código com anos de experiência.
Sua função é revisar código e fornecer feedback detalhado baseado na análise prévia.

Ao revisar o código, você deve:
1. Identificar bugs, erros de lógica ou problemas potenciais
2. Sugerir melhorias de performance quando aplicável
3. Apontar más práticas e sugerir alternativas
4. Verificar se o código segue boas práticas da linguagem
5. Fornecer exemplos de código corrigido quando necessário

Formato da resposta:
- Use markdown para formatar sua resposta
- Seja claro e objetivo
- Forneça exemplos de código quando sugerir correções
- Organize por categorias: Bugs Críticos, Bugs Menores, Melhorias, Boas Práticas, etc.
- No final, forneça uma nota geral (de 1 a 10)

Responda sempre em português brasileiro."""

    def __init__(self):
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
                    {"role": "system", "content": self.UNDERSTANDING_PROMPT},
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
                    {"role": "system", "content": self.REVIEW_PROMPT},
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
            review = self._review_code(code, understanding, task, filename, language)

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
