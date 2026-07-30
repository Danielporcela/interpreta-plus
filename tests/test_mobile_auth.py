from tests.conftest import cadastrar


def test_login_via_api_retorna_token(client):
    cadastrar(client, nome="Asaph", email="mobile1@teste.com", senha="123456")
    client.get("/logout")  # garante que não está usando sessão de navegador

    r = client.post("/api/v1/auth/login", json={"email": "mobile1@teste.com", "senha": "123456"})
    assert r.status_code == 200
    dados = r.get_json()
    assert "token" in dados
    assert dados["usuario"]["nome"] == "Asaph"


def test_login_via_api_com_senha_errada_retorna_401(client):
    cadastrar(client, email="mobile2@teste.com", senha="123456")
    client.get("/logout")

    r = client.post("/api/v1/auth/login", json={"email": "mobile2@teste.com", "senha": "errada"})
    assert r.status_code == 401


def test_endpoint_funciona_com_token_sem_sessao(client):
    cadastrar(client, nome="Asaph", email="mobile3@teste.com", senha="123456")
    r = client.post("/api/v1/auth/login", json={"email": "mobile3@teste.com", "senha": "123456"})
    token = r.get_json()["token"]

    client.get("/logout")  # remove qualquer cookie de sessão

    r = client.get("/api/v1/usuario/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.get_json()["nome"] == "Asaph"


def test_endpoint_sem_token_e_sem_sessao_retorna_401(client):
    r = client.get("/api/v1/usuario/me")
    assert r.status_code == 401


def test_token_invalido_retorna_401(client):
    r = client.get("/api/v1/usuario/me", headers={"Authorization": "Bearer token-que-nao-existe"})
    assert r.status_code == 401


def test_logout_via_api_revoga_o_token(client):
    cadastrar(client, email="mobile4@teste.com", senha="123456")
    r = client.post("/api/v1/auth/login", json={"email": "mobile4@teste.com", "senha": "123456"})
    token = r.get_json()["token"]
    client.get("/logout")

    headers = {"Authorization": f"Bearer {token}"}
    r = client.post("/api/v1/auth/logout", headers=headers)
    assert r.status_code == 200

    r = client.get("/api/v1/usuario/me", headers=headers)
    assert r.status_code == 401  # token já revogado


def test_resposta_da_api_tem_cabecalho_cors(client):
    r = client.get("/api/v1/usuario/me")
    assert "Access-Control-Allow-Origin" in r.headers
