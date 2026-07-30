from functools import wraps
from flask import session, redirect, url_for, flash, jsonify, request, g


def login_obrigatorio(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorada


def admin_obrigatorio(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("auth.login"))
        if not session.get("is_admin"):
            flash("Acesso restrito ao administrador.")
            return redirect(url_for("dashboard.index"))
        return f(*args, **kwargs)

    return decorada


def api_login_obrigatorio(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if "usuario_id" not in session:
            return jsonify({"erro": "autenticação necessária"}), 401
        return f(*args, **kwargs)

    return decorada


def api_auth_obrigatoria(f):
    """
    Autenticação da API que aceita DOIS métodos, para funcionar tanto no
    navegador (sessão com cookie) quanto no futuro app móvel (token):

    - Header "Authorization: Bearer <token>" (app móvel)
    - Sessão do navegador já logado (claude.ai / web)

    Em ambos os casos, deixa o id do usuário disponível em g.usuario_id_atual.
    """

    @wraps(f)
    def decorada(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1].strip()
            from models import api_token as api_token_model

            usuario_id = api_token_model.buscar_usuario_id_por_token(token)
            if usuario_id is None:
                return jsonify({"erro": "token inválido ou expirado"}), 401
            g.usuario_id_atual = usuario_id
            return f(*args, **kwargs)

        if "usuario_id" in session:
            g.usuario_id_atual = session["usuario_id"]
            return f(*args, **kwargs)

        return jsonify({"erro": "autenticação necessária"}), 401

    return decorada
