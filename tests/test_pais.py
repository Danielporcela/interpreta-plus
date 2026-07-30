from tests.conftest import cadastrar


def test_responsavel_vincula_crianca_pelo_email(client):
    cadastrar(client, nome="Filho", email="filho@teste.com", tipo="crianca")
    client.get("/logout")

    cadastrar(client, nome="Responsável", email="resp@teste.com", tipo="responsavel")
    r = client.post("/pais/vincular", data={"email_crianca": "filho@teste.com"}, follow_redirects=True)
    assert "vinculado".encode("utf-8") in r.data

    r = client.get("/pais")
    assert b"Filho" in r.data


def test_nao_vincula_email_inexistente(client):
    cadastrar(client, nome="Responsável", email="resp2@teste.com", tipo="responsavel")
    r = client.post("/pais/vincular", data={"email_crianca": "naoexiste@teste.com"}, follow_redirects=True)
    assert "N\u00e3o encontramos".encode("utf-8") in r.data


def test_crianca_nao_acessa_area_dos_pais(client):
    cadastrar(client, tipo="crianca")
    r = client.get("/pais", follow_redirects=True)
    assert "exclusiva para contas de respons".encode("utf-8") in r.data
