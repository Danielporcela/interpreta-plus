from tests.conftest import cadastrar, responder_treino


def test_treino_mostra_historia_e_perguntas(client):
    cadastrar(client, email="treino1@teste.com")
    r = client.get("/treino")
    assert b"Pergunta 1" in r.data
    assert b"Pergunta 2" in r.data


def test_responder_tudo_certo_gera_pontuacao_100(client):
    cadastrar(client, email="treino2@teste.com")
    # As duas perguntas do seed de teste têm resposta correta 'a' e 'b'
    import re

    r = client.get("/treino")
    historia_id = re.search(rb'name="historia_id" value="(\d+)"', r.data).group(1).decode()
    perguntas = re.findall(rb'name="pergunta_(\d+)" value="(a|b)"', r.data)

    # monta as respostas corretas lendo qual letra corresponde à alternativa certa
    # (no seed de teste sabemos que a 1a pergunta é 'a' e a 2a é 'b', na ordem de criação)
    pergunta_ids = sorted(set(p[0].decode() for p in perguntas))
    form = {"historia_id": historia_id, f"pergunta_{pergunta_ids[0]}": "a", f"pergunta_{pergunta_ids[1]}": "b"}

    r = client.post("/treino/responder", data=form, follow_redirects=True)
    assert b"100" in r.data
    assert b"Acertos" in r.data or b"acertos" in r.data.lower()


def test_responder_tudo_errado_gera_pontuacao_zero(client):
    cadastrar(client, email="treino3@teste.com")
    r = responder_treino(client, resposta="c")  # 'c' está errada nas duas perguntas do seed
    assert r.status_code == 200
    assert b"0" in r.data


def test_progresso_e_salvo_apos_responder(client):
    cadastrar(client, email="treino4@teste.com")
    responder_treino(client, resposta="a")

    r = client.get("/api/v1/progresso/me")
    dados = r.get_json()
    assert len(dados) == 1
    assert dados[0]["historia_id"] is not None


def test_apos_concluir_todas_historias_do_nivel_mostra_aviso(client):
    cadastrar(client, email="treino5@teste.com")
    responder_treino(client)  # só existe 1 história no seed de teste

    r = client.get("/treino", follow_redirects=True)
    assert "concluiu todas as histórias".encode("utf-8") in r.data
