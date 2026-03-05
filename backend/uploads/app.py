import os
import tempfile
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from agent import CodeReviewAgent

app = Flask(__name__)
CORS(app)

# Inicializar agente
try:
    ai_agent = CodeReviewAgent()
    print("Agente de IA inicializado")
except Exception as e:
    ai_agent = None
    print(f"Erro: {e}")

# Upload (fora da pasta do projeto para evitar restart do reloader durante upload)
UPLOAD_FOLDER = os.getenv(
    "AKCIT_UPLOAD_DIR",
    os.path.join(tempfile.gettempdir(), "akcit-agent-uploads"),
)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB

ALLOWED_EXTENSIONS = {
    "cs", "js", "ts", "py", "java", "cpp", "c", "razor",
    "html", "css", "json", "xml", "txt", "md"
}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.get("/")
def hello():
    return jsonify({"message": "Hello from Flask backend"})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/review")
def review_code():
    """
    Recebe um arquivo de código e uma descrição da tarefa.
    Retorna uma resposta placeholder que será substituída pelo agente de IA.
    """
    # Validar arquivo
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Nome do arquivo vazio"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Tipo de arquivo não permitido"}), 400

    # Obter tarefa/mensagem
    task = request.form.get("task", "")
    if not task.strip():
        return jsonify({"error": "Descreva a tarefa que deseja realizar"}), 400

    # Salvar arquivo temporariamente
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    ####### IMPORTANTE: Adicionar um llm técnica para entender o código e outra para revisar e enviar para o usuário
    # Ler conteúdo do arquivo
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            code_content = f.read()
    except Exception as e:
        return jsonify({"error": f"Erro ao ler arquivo: {str(e)}"}), 500

    # Chamar agente de IA para análise
    if ai_agent:
        ai_response = ai_agent.review(code_content, task, filename)
    else:
        ai_response = "Erro: Verifique a configuração da key."

    response = {
        "status": "success",
        "filename": filename,
        "task": task,
        "code_preview": code_content[:500] + ("..." if len(code_content) > 500 else ""),
        "ai_response": ai_response
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2518, debug=True)
