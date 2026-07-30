import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    # Em produção, defina a variável de ambiente SECRET_KEY com um valor
    # aleatório e seguro (ex.: python -c "import secrets; print(secrets.token_hex(32))").
    SECRET_KEY = os.environ.get("SECRET_KEY", "chave-secreta-interpreta-dev")
    DATABASE_PATH = os.environ.get(
        "DATABASE_PATH", os.path.join(BASE_DIR, "database", "banco.db")
    )
    SCHEMA_PATH = os.path.join(BASE_DIR, "database", "schema.sql")

    # DEBUG nunca deve ficar ativo em produção (evita expor stack traces).
    DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"

    # Origem permitida para chamadas à API (Etapa 19 - app móvel).
    # Em produção, troque "*" pelo domínio/esquema do seu app (ex.: capacitor://localhost).
    API_CORS_ORIGIN = os.environ.get("API_CORS_ORIGIN", "*")

    # Etapa 18 - Preparação para IA (Fase 3).
    # "simulado" funciona 100% offline, sem custo e sem chave de API — é o padrão.
    # Trocar para "anthropic" (e definir ANTHROPIC_API_KEY) ativa o feedback gerado por IA de verdade.
    IA_PROVIDER = os.environ.get("IA_PROVIDER", "simulado")
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

    # Cookies de sessão mais seguros quando servidos via HTTPS em produção.
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
