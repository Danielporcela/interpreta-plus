from tests.conftest import cadastrar, login


def test_cadastro_cria_conta_e_faz_login_automatico(client):
    r = cadastrar(client, nome="Asaph", email="asaph@teste.com")
    assert r.status_code == 200
    assert "Olá, Asaph".encode("utf-8") in r.data


def test_nao_permite_email_duplicado(client):
    cadastrar(client, email="duplicado@teste.com")
    r = cadastrar(client, nome="Outro", email="duplicado@teste.com")
    assert "já está cadastrado".encode("utf-8") in r.data


def test_login_com_senha_errada_nao_entra(client):
    cadastrar(client, email="senha@teste.com", senha="senhacerta")
    client.get("/logout")
    r = login(client, "senha@teste.com", senha="senhaerrada")
    assert "inválidos".encode("utf-8") in r.data


def test_login_com_sucesso_redireciona_ao_dashboard(client):
    cadastrar(client, email="login_ok@teste.com", senha="123456")
    client.get("/logout")
    r = login(client, "login_ok@teste.com", "123456")
    assert "Olá,".encode("utf-8") in r.data


def test_rotas_protegidas_exigem_login(client):
    r = client.get("/treino", follow_redirects=True)
    assert b"INTERPRETA" in r.data  # caiu na tela de login
    assert r.request.path == "/login"


def test_logout_encerra_sessao(client):
    cadastrar(client, email="logout@teste.com")
    client.get("/logout")
    r = client.get("/treino", follow_redirects=True)
    assert r.request.path == "/login"
