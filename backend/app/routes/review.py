"""
Rotas para code review.
"""
from flask import Blueprint, jsonify, request, current_app
from werkzeug.exceptions import BadRequest

from app.schemas.code_review import CodeReviewRequest, CodeReviewResponse
from app.utils.file_handler import (
    allowed_file,
    save_upload_file,
    read_file_content,
    get_file_extension,
    get_language_from_extension,
)

review_bp = Blueprint("review", __name__, url_prefix="/api/v1")


@review_bp.post("/review")
def review_code():
    """
    Recebe um arquivo de código e uma descrição da tarefa.
    Retorna análise da IA sobre o código.
    """
    try:
        # Validar arquivo
        if "file" not in request.files:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "Nome do arquivo vazio"}), 400

        if not allowed_file(file.filename, current_app.config["ALLOWED_EXTENSIONS"]):
            return jsonify({"error": "Tipo de arquivo não permitido"}), 400

        # Obter tarefa/mensagem
        task = request.form.get("task", "").strip()
        if not task:
            return jsonify({"error": "Descreva a tarefa que deseja realizar"}), 400

        # Salvar arquivo temporariamente
        filepath = save_upload_file(file, current_app.config["UPLOAD_FOLDER"])

        # Ler conteúdo do arquivo
        code_content = read_file_content(filepath)

        # Criar requisição validada
        review_request = CodeReviewRequest(
            filename=file.filename,
            task=task,
            code_content=code_content,
        )

        # Validar requisição
        errors = review_request.validate()
        if errors:
            return jsonify({"errors": errors}), 400

        # Chamar agente de IA para análise
        ai_agent = current_app.config.get("AI_AGENT")
        if ai_agent:
            analysis_result = ai_agent.review(
                code_content, 
                task, 
                file.filename
            )
        else:
            analysis_result = {
                "status": "error",
                "error": "Agente de IA não configurado. Verifique a chave GROQ_API_KEY."
            }

        # Preparar resposta
        code_preview = code_content[:500] + (
            "..." if len(code_content) > 500 else ""
        )

        if analysis_result["status"] == "success":
            review_response = CodeReviewResponse(
                status="success",
                filename=file.filename,
                task=task,
                code_preview=code_preview,
                ai_response=analysis_result["summary"],
            )
            return jsonify({
                **review_response.to_dict(),
                "understanding": analysis_result["understanding"],
                "review": analysis_result["review"],
            }), 200
        else:
            return jsonify({
                "status": "error",
                "error": analysis_result.get("error", "Erro desconhecido")
            }), 500

    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500
