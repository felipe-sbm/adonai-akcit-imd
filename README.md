# Agente de IA - Curso do Akcit
Sistema de revisão de código com inteligência artificial, desenvolvido como projeto do curso de parceria do **IMD/UFRN** e do **Akcit**.

## Visão Geral
Este projeto combina um frontend feito **Blazor WebAssembly** com um backend em **Python/FastAPI** para oferecer uma **Revisão de Código** com análise inteligente de código com sugestões de melhoria, apontamento de erros e identificação de vulnerabilidades.

## Início Rápido
### Pré-requisitos
- [.NET 9 SDK](https://dotnet.microsoft.com/download)
- [Python 3.10+](https://python.org)
- [Chave de API do Groq](https://console.groq.com) (gratuito)

### 1. Backend (Python)
```bash
cd backend

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux ou MacOS
# ou em Windows: venv\Scripts\activate

# Instalar dependências
python3 -m pip install -r requirements.txt

# Rodar servidor
python3 app.py
```
O backend estará em: http://localhost:8000 (não esqueça de configurar a variável da API do Groq)

### 2. Frontend (Blazor)
```bash
cd frontend

# Restaurar pacotes
dotnet restore

# Rodar em modo desenvolvimento
dotnet watch
```

O frontend estará em: http://localhost:5000 (ou porta indicada)

## Endpoints da API
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/health` | Health check |
| POST | `/api/code-review` | Revisão de código (JSON) |
| POST | `/api/code-review/upload` | Revisão via upload |
| POST | `/api/writer` | Escrita de matérias |
| POST | `/api/fact-check` | Checagem de fatos |

Documentação interativa: http://localhost:8000/docs

## Configuração
### Variáveis de Ambiente (Backend)
| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `GROQ_API_KEY` | API key do Groq | - |
| `PORT` | Porta do servidor | `8000` |
| `DEBUG` | Modo debug | `false` |

## Tecnologias
### Frontend
- Blazor WebAssembly (com C# em .NET 9)
- Bootstrap 5 (já vem instalado com Blazor)

### Backend
- FastAPI (Python)
- Groq (LLM gratuito)

## Lecionadores e Orientadores
Projeto desenvolvido para o curso do **IMD/UFRN** em parceria com a **Akcit**.

- **Orientação**: Julia Dollis e Prof. Alyson Matheus

---
Projeto acadêmico - uso educacional de nível técnico.
