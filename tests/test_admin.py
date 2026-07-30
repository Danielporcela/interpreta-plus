import re

from tests.conftest import cadastrar
from models.db import get_db
from werkzeug.security import generate_password_hash


def _criar_admin(app):
    with app.app_context():
        db = get_db()
        db.execute(
            "INSERT INTO usuarios (nome, email, senha, tipo, is_admin) VALUES (?, ?, ?, ?, ?)",
            ("Admin Teste", "admin_teste@teste.com", generate_password_hash("admin123"), "responsavel", 1),
        )
        db.commit()


def _login_admin(client, app):
    _criar_admin(app)
    return client.post(
        "/login", data={"email": "admin_teste@teste.com", "senha": "admin123"}, follow_redirects=True
    )


def test_usuario_comum_nao_acessa_admin(client):
    cadastrar(client, email="comum@teste.com")
    r = client.get("/admin/", follow_redirects=True)
    assert "restrito ao administrador".encode("utf-8") in r.data


def test_admin_acessa_painel(client, app):
    r = _login_admin(client, app)
    assert b"Administra" in r.data


def test_admin_cria_edita_e_exclui_historia(client, app):
    _login_admin(client, app)

    r = client.post(
        "/admin/historia/nova",
        data={"titulo": "Nova História", "texto": "Texto qualquer.", "nivel": "2", "categoria": "escola"},
        follow_redirects=True,
    )
    assert "Agora adicione as perguntas".encode("utf-8") in r.data

    historia_id = re.search(rb"/admin/historia/(\d+)/pergunta/nova", r.data).group(1).decode()

    r = client.post(
        f"/admin/historia/{historia_id}/editar",
        data={"titulo": "História Editada", "texto": "Texto editado.", "nivel": "2", "categoria": "escola"},
        follow_redirects=True,
    )
    assert "atualizada com sucesso".encode("utf-8") in r.data

    r = client.post(f"/admin/historia/{historia_id}/excluir", follow_redirects=True)
    assert "excluída".encode("utf-8") in r.data


def test_admin_adiciona_e_exclui_pergunta(client, app):
    _login_admin(client, app)

    r = client.post(
        "/admin/historia/nova",
        data={"titulo": "História Perguntas", "texto": "Texto.", "nivel": "1", "categoria": "geral"},
        follow_redirects=True,
    )
    historia_id = re.search(rb"/admin/historia/(\d+)/pergunta/nova", r.data).group(1).decode()

    r = client.post(
        f"/admin/historia/{historia_id}/pergunta/nova",
        data={
            "texto": "Pergunta nova?",
            "a": "A",
            "b": "B",
            "c": "C",
            "d": "D",
            "e": "",
            "correta": "a",
            "explicacao": "explicação",
        },
        follow_redirects=True,
    )
    assert "adicionada".encode("utf-8") in r.data

    pergunta_id = re.search(rb"/admin/pergunta/(\d+)/excluir", r.data).group(1).decode()
    r = client.post(f"/admin/pergunta/{pergunta_id}/excluir", follow_redirects=True)
    assert "excluída".encode("utf-8") in r.data
