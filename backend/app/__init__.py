"""
Factory para criar aplicação Flask com configurações e rotas.
"""
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

from app.config.settings import get_config
from app.routes import api
from app.routes.health import health_bp
from app.routes.review import review_bp
from bot.base_persona_prompt import BASE_PERSONA_PROMPT
from bot.response_language_prompt import RESPONSE_LANGUAGE_PROMPT
from bot.response_emotion import RESPONSE_EMOTION_PROMPT
from bot.understanding_prompt import UNDERSTANDING_TASK_PROMPT
from bot.review_prompt import REVIEW_TASK_PROMPT

# Carregar variáveis de ambiente
load_dotenv()


def create_app():
    """
    Factory function para criar a aplicação Flask.
    
    Returns:
        Aplicação Flask configurada
    """
    # Criar aplicação
    app = Flask(__name__)
    
    # Aplicar configurações
    config = get_config()
    app.config.from_object(config)
    
    # Ativar CORS para todas as origens e rotas
    CORS(app, resources={r"/*": {"origins": "*"}})

    understanding_prompt = "\n\n".join([
        BASE_PERSONA_PROMPT,
        UNDERSTANDING_TASK_PROMPT,
        RESPONSE_LANGUAGE_PROMPT,
    ])

    review_prompt = "\n\n".join([
        BASE_PERSONA_PROMPT,
        REVIEW_TASK_PROMPT,
        RESPONSE_EMOTION_PROMPT,
        RESPONSE_LANGUAGE_PROMPT,
    ])
    
    # Inicializar agente de IA
    try:
        from agent import CodeReviewAgent
        app.config["AI_AGENT"] = CodeReviewAgent(
            understanding_prompt=understanding_prompt,
            review_prompt=review_prompt,
        )
        print("✓ Agente de IA inicializado com sucesso")
    except Exception as e:
        app.config["AI_AGENT"] = None
        print(f"⚠ Erro ao inicializar agente de IA: {e}")
    
    # Registrar blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(review_bp)
    
    return app
