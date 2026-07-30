from flask import Blueprint, jsonify, request, g
from werkzeug.security import check_password_hash

from models import usuario as usuario_model
from models import biblioteca as biblioteca_model
from models import progresso as progresso_model
from models import medalha as medalha_model
from models import api_token as api_token_model
from services import relatorio_service
from utils.helpers import api_auth_obrigatoria

bp = Blueprint("api", __name__, url_prefix="/api/v1")


def usuario_para_json(user):
    return {
        "id": user["id"],
        "nome": user["nome"],
        "idade": user["idade"],
        "tipo": user["tipo"],
        "nivel": user["nivel"],
        "pontos": user["pontos"],
        "dias_estudo": user["dias_estudo"],
        "sequencia": user["sequencia"],
    }


# --- Autenticação por token (Etapa 19 - preparação para o app móvel) -------------

@bp.route("/auth/login", methods=["POST"])
def login():
    """
    Login para clientes que não usam cookie de sessão (app móvel).
    Aceita JSON ou form-data: {"email": "...", "senha": "..."}
    Retorna um token que deve ser enviado em requisições futuras como:
    Authorization: Bearer <token>
    """
    dados = request.get_json(silent=True) or request.form
    email = (dados.get("email") or "").strip().lower()
    senha = dados.get("senha") or ""

    user = usuario_model.buscar_por_email(email)
    if not user or not check_password_hash(user["senha"], senha):
        return jsonify({"erro": "e-mail ou senha inválidos"}), 401

    token = api_token_model.gerar_token(user["id"])
    return jsonify({"token": token, "usuario": usuario_para_json(user)})


@bp.route("/auth/logout", methods=["POST"])
@api_auth_obrigatoria
def logout():
    """Revoga o token enviado (se a autenticação foi feita por Bearer token)."""
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1].strip()
        api_token_model.revogar_token(token)
    return jsonify({"ok": True})


# --- Dados do usuário logado (funcionam com sessão OU token) ---------------------

@bp.route("/usuario/me")
@api_auth_obrigatoria
def usuario_me():
    user = usuario_model.buscar_por_id(g.usuario_id_atual)
    return jsonify(usuario_para_json(user))


@bp.route("/historias")
@api_auth_obrigatoria
def listar_historias():
    historias = biblioteca_model.listar_todas()
    return jsonify(
        [
            {"id": h["id"], "titulo": h["titulo"], "nivel": h["nivel"], "categoria": h["categoria"]}
            for h in historias
        ]
    )


@bp.route("/progresso/me")
@api_auth_obrigatoria
def progresso_me():
    itens = progresso_model.listar_por_usuario(g.usuario_id_atual)
    return jsonify(
        [
            {
                "historia_id": p["historia_id"],
                "nivel": p["nivel"],
                "pontos": p["pontos"],
                "acertos": p["acertos"],
                "erros": p["erros"],
                "data": p["data"],
            }
            for p in itens
        ]
    )


@bp.route("/relatorio/me")
@api_auth_obrigatoria
def relatorio_me():
    usuario_id = g.usuario_id_atual
    return jsonify(
        {
            "resumo": relatorio_service.resumo_geral(usuario_id),
            "por_categoria": relatorio_service.desempenho_por_categoria(usuario_id),
        }
    )


@bp.route("/medalhas/me")
@api_auth_obrigatoria
def medalhas_me():
    conquistadas = medalha_model.listar_conquistadas(g.usuario_id_atual)
    return jsonify(
        [
            {"codigo": m["codigo"], "titulo": m["titulo"], "icone": m["icone"], "data": m["data_conquista"]}
            for m in conquistadas
        ]
    )
