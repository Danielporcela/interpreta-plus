from services import ia_service


def test_feedback_simulado_pontuacao_100(app):
    with app.app_context():
        app.config["IA_PROVIDER"] = "simulado"
        texto = ia_service.gerar_feedback(100, 3, 0)
        assert isinstance(texto, str) and len(texto) > 0


def test_feedback_simulado_pontuacao_baixa(app):
    with app.app_context():
        app.config["IA_PROVIDER"] = "simulado"
        texto = ia_service.gerar_feedback(0, 0, 3)
        assert isinstance(texto, str) and len(texto) > 0


def test_feedback_aparece_na_tela_de_resultado(client):
    from tests.conftest import cadastrar, responder_treino

    cadastrar(client, email="ia1@teste.com")
    r = responder_treino(client)
    assert "💬".encode("utf-8") in r.data


def test_provider_anthropic_sem_chave_cai_no_simulado(app):
    with app.app_context():
        app.config["IA_PROVIDER"] = "anthropic"
        app.config["ANTHROPIC_API_KEY"] = ""  # sem chave -> não deve nem tentar chamar a API real
        texto = ia_service.gerar_feedback(80, 4, 1)
        assert isinstance(texto, str) and len(texto) > 0
