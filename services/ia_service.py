"""
Serviço de feedback gerado por IA (Etapa 18 - preparação para a Fase 3).

Por padrão funciona no modo "simulado": mensagens variadas e calorosas,
sem precisar de internet, chave de API ou custo algum — o app funciona
100% completo sem IA nenhuma.

Quando quiser ativar IA de verdade, basta:
1. Definir a variável de ambiente IA_PROVIDER=anthropic
2. Definir ANTHROPIC_API_KEY com uma chave válida
3. Instalar o pacote: pip install anthropic

Nenhuma rota, template ou service precisa mudar — só esse arquivo.
"""
import random

from flask import current_app


def gerar_feedback(pontuacao, acertos, erros):
    """
    Retorna uma frase curta e motivadora para a criança, com base no resultado.
    Tenta a IA real primeiro (se configurada); se falhar por qualquer motivo
    (sem internet, sem chave, erro da API), cai automaticamente no modo simulado.
    """
    provider = current_app.config.get("IA_PROVIDER", "simulado")

    if provider == "anthropic" and current_app.config.get("ANTHROPIC_API_KEY"):
        try:
            return _gerar_feedback_anthropic(pontuacao, acertos, erros)
        except Exception:
            pass  # qualquer falha da IA real não pode quebrar a experiência da criança

    return _gerar_feedback_simulado(pontuacao, acertos, erros)


def _gerar_feedback_simulado(pontuacao, acertos, erros):
    if pontuacao == 100:
        opcoes = [
            "Mandou muito bem! Você entendeu a história inteira. 🌟",
            "Gabaritou! Sua leitura está cada vez mais afiada. 🎯",
            "Perfeito! Continue assim que você vai longe. 🚀",
        ]
    elif pontuacao >= 60:
        opcoes = [
            "Muito bom! Você entendeu a maior parte da história. 💪",
            "Bom trabalho! Só faltou prestar atenção em um detalhezinho. 👀",
            "Você está indo bem, continue treinando todo dia! 📈",
        ]
    else:
        opcoes = [
            "Bom começo! Vamos ler com calma de novo amanhã? 🌱",
            "Tudo bem errar, é assim que se aprende. Bora tentar outra história? 💙",
            "Você tentou, e isso já é o mais importante! Continue treinando. 🤝",
        ]

    return random.choice(opcoes)


def _gerar_feedback_anthropic(pontuacao, acertos, erros):
    """
    Ponto de extensão para a IA real (Fase 3). Não é chamado no modo padrão.
    Requer: pip install anthropic + variável de ambiente ANTHROPIC_API_KEY.
    """
    import anthropic  # importado aqui para não ser uma dependência obrigatória no MVP

    client = anthropic.Anthropic(api_key=current_app.config["ANTHROPIC_API_KEY"])

    prompt = (
        f"Uma criança respondeu a um exercício de interpretação de texto e acertou "
        f"{acertos} e errou {erros} perguntas (pontuação {pontuacao} de 100). "
        f"Escreva UMA frase curta (máximo 15 palavras), calorosa, motivadora e em "
        f"português do Brasil, adequada para uma criança. Não use emojis em excesso."
    )

    resposta = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=60,
        messages=[{"role": "user", "content": prompt}],
    )
    return resposta.content[0].text.strip()
