import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models.db import init_db, get_db


@pytest.fixture
def app():
    """Cria uma instância da aplicação com um banco SQLite temporário e isolado."""
    db_fd, db_path = tempfile.mkstemp()

    application = create_app(
        {
            "TESTING": True,
            "DATABASE_PATH": db_path,
            "SECRET_KEY": "chave-de-teste",
        }
    )

    with application.app_context():
        init_db(application)
        _seed_minimo()

    yield application

    os.close(db_fd)
    os.unlink(db_path)


def _seed_minimo():
    """Cadastra 1 história com 2 perguntas e as medalhas básicas, para os testes."""
    db = get_db()

    cur = db.execute(
        "INSERT INTO historias (titulo, texto, nivel, categoria) VALUES (?, ?, ?, ?)",
        ("História de teste", "Era uma vez... um texto de teste.", 1, "geral"),
    )
    historia_id = cur.lastrowid

    db.execute(
        """INSERT INTO perguntas (historia_id, texto, a, b, c, d, e, correta, explicacao)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (historia_id, "Pergunta 1?", "certa", "errada", "errada", "errada", "", "a", "porque sim"),
    )
    db.execute(
        """INSERT INTO perguntas (historia_id, texto, a, b, c, d, e, correta, explicacao)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (historia_id, "Pergunta 2?", "errada", "certa", "errada", "errada", "", "b", "porque sim"),
    )

    medalhas = [
        ("primeiro_dia", "Primeiro Passo", "Completou a primeira história.", "🥇"),
        ("gabarito", "Gabarito", "Acertou todas as perguntas de uma história.", "🎯"),
        ("pontuacao_100", "Centena", "Alcançou 100 pontos.", "💯"),
        ("nivel_2", "Subindo de Nível", "Chegou ao nível 2.", "⭐"),
        ("sequencia_3", "Em Ritmo", "Estudou 3 dias seguidos.", "🔥"),
        ("sequencia_7", "Semana Completa", "Estudou 7 dias seguidos.", "🏆"),
    ]
    for codigo, titulo, descricao, icone in medalhas:
        db.execute(
            "INSERT INTO medalhas (codigo, titulo, descricao, icone) VALUES (?, ?, ?, ?)",
            (codigo, titulo, descricao, icone),
        )

    db.commit()


@pytest.fixture
def client(app):
    return app.test_client()


def cadastrar(client, nome="Criança Teste", email="crianca@teste.com", senha="123456", tipo="crianca", idade="8"):
    return client.post(
        "/cadastro",
        data={"nome": nome, "email": email, "senha": senha, "idade": idade, "tipo": tipo},
        follow_redirects=True,
    )


def login(client, email, senha="123456"):
    return client.post("/login", data={"email": email, "senha": senha}, follow_redirects=True)


def responder_treino(client, resposta="a"):
    """Busca a próxima atividade de treino e responde todas as perguntas com a mesma letra."""
    import re

    r = client.get("/treino")
    historia_id = re.search(rb'name="historia_id" value="(\d+)"', r.data).group(1).decode()
    pergunta_ids = sorted(set(p.decode() for p in re.findall(rb'name="pergunta_(\d+)"', r.data)))

    form = {"historia_id": historia_id}
    for pid in pergunta_ids:
        form[f"pergunta_{pid}"] = resposta

    return client.post("/treino/responder", data=form, follow_redirects=True)
