import re

from tests.conftest import cadastrar


def _responder_correto(client):
    """Responde a única história do seed de teste acertando as duas perguntas."""
    r = client.get("/treino")
    historia_id = re.search(rb'name="historia_id" value="(\d+)"', r.data).group(1).decode()
    pergunta_ids = sorted(set(p.decode() for p in re.findall(rb'name="pergunta_(\d+)"', r.data)))

    # No seed de teste: 1a pergunta correta = 'a', 2a pergunta correta = 'b'
    form = {"historia_id": historia_id, f"pergunta_{pergunta_ids[0]}": "a", f"pergunta_{pergunta_ids[1]}": "b"}
    return client.post("/treino/responder", data=form, follow_redirects=True)


def test_completar_primeira_historia_concede_medalha_primeiro_dia(client):
    cadastrar(client, email="conquista1@teste.com")
    r = _responder_correto(client)
    assert "Primeiro Passo".encode("utf-8") in r.data


def test_acertar_tudo_concede_medalha_gabarito(client):
    cadastrar(client, email="conquista2@teste.com")
    r = _responder_correto(client)
    assert b"Gabarito" in r.data


def test_tela_de_conquistas_lista_medalhas_disponiveis(client):
    cadastrar(client, email="conquista3@teste.com")
    r = client.get("/conquistas")
    assert b"Primeiro Passo" in r.data
    assert b"Gabarito" in r.data


def test_medalha_so_e_concedida_uma_vez(client):
    cadastrar(client, email="conquista4@teste.com")
    _responder_correto(client)

    r = client.get("/api/v1/medalhas/me")
    dados = r.get_json()
    codigos = [m["codigo"] for m in dados]
    assert len(codigos) == len(set(codigos))  # sem duplicatas
