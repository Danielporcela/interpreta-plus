from tests.conftest import cadastrar


def test_api_sem_login_retorna_401(client):
    r = client.get("/api/v1/usuario/me")
    assert r.status_code == 401


def test_api_usuario_me(client):
    cadastrar(client, nome="Asaph", email="api1@teste.com")
    r = client.get("/api/v1/usuario/me")
    dados = r.get_json()
    assert dados["nome"] == "Asaph"
    assert dados["nivel"] == 1


def test_api_lista_historias(client):
    cadastrar(client, email="api2@teste.com")
    r = client.get("/api/v1/historias")
    dados = r.get_json()
    assert isinstance(dados, list)
    assert len(dados) >= 1


def test_api_relatorio_me_estrutura(client):
    cadastrar(client, email="api3@teste.com")
    r = client.get("/api/v1/relatorio/me")
    dados = r.get_json()
    assert "resumo" in dados
    assert "por_categoria" in dados
    assert "percentual_acertos" in dados["resumo"]
