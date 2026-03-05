"""
Rotas de health check.
"""
from flask import jsonify, Blueprint

health_bp = Blueprint("health", __name__)


@health_bp.get("/")
def hello():
    """Rota raiz da API."""
    return jsonify({"message": "Hello from Flask backend"}), 200


@health_bp.get("/health")
def health():
    """Health check da API."""
    return jsonify({"status": "ok"}), 200
