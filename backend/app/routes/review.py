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
        payload = request.get_json(silent=True) or {}
        task = (request.form.get("task") or payload.get("task", "")).strip()
        if not task:
            return jsonify({"error": "Descreva a tarefa que deseja realizar"}), 400

        ai_agent = current_app.config.get("AI_AGENT")
        file = request.files.get("file")

        if file and file.filename:
            if not allowed_file(file.filename, current_app.config["ALLOWED_EXTENSIONS"]):
                return jsonify({"error": "Tipo de arquivo não permitido"}), 400

            filepath = save_upload_file(file, current_app.config["UPLOAD_FOLDER"])
            code_content = read_file_content(filepath)

            review_request = CodeReviewRequest(
                filename=file.filename,
                task=task,
                code_content=code_content,
            )

            errors = review_request.validate()
            if errors:
                return jsonify({"errors": errors}), 400

            if ai_agent:
                analysis_result = ai_agent.review(
                    code_content,
                    task,
                    file.filename,
                )
            else:
                analysis_result = {
                    "status": "error",
                    "error": "Agente de IA não configurado. Verifique a chave GROQ_API_KEY.",
                }
        else:
            if ai_agent:
                analysis_result = ai_agent.review_without_file(task)
            else:
                analysis_result = {
                    "status": "error",
                    "error": "Agente de IA não configurado. Verifique a chave GROQ_API_KEY.",
                }

        has_file = bool(file and file.filename)
        filename = file.filename if has_file else "sem_arquivo"
        code_preview = (
            code_content[:500] + ("..." if len(code_content) > 500 else "")
            if has_file
            else "Nenhum arquivo anexado."
        )

        if analysis_result["status"] == "success":
            review_response = CodeReviewResponse(
                status="success",
                filename=filename,
                task=task,
                code_preview=code_preview,
                ai_response=analysis_result["summary"],
            )
            return jsonify({
                **review_response.to_dict(),
                "emotion": analysis_result.get("emotion", "explicativa"),
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
