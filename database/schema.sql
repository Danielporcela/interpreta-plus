-- INTERPRETA+ | Fase 1 - MVP
-- Estrutura do banco de dados

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    idade INTEGER,
    tipo TEXT NOT NULL DEFAULT 'crianca',
    is_admin INTEGER NOT NULL DEFAULT 0,
    nivel INTEGER NOT NULL DEFAULT 1,
    pontos INTEGER NOT NULL DEFAULT 0,
    dias_estudo INTEGER NOT NULL DEFAULT 0,
    sequencia INTEGER NOT NULL DEFAULT 0,
    ultima_atividade TEXT,
    data_cadastro TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS historias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    texto TEXT NOT NULL,
    nivel INTEGER NOT NULL DEFAULT 1,
    categoria TEXT NOT NULL DEFAULT 'geral'
);

CREATE TABLE IF NOT EXISTS perguntas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    historia_id INTEGER NOT NULL,
    texto TEXT NOT NULL,
    a TEXT NOT NULL,
    b TEXT NOT NULL,
    c TEXT NOT NULL,
    d TEXT NOT NULL,
    e TEXT,
    correta TEXT NOT NULL,
    explicacao TEXT,
    FOREIGN KEY (historia_id) REFERENCES historias (id)
);

CREATE TABLE IF NOT EXISTS respostas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    pergunta_id INTEGER NOT NULL,
    resposta TEXT NOT NULL,
    acertou INTEGER NOT NULL,
    tempo TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
    FOREIGN KEY (pergunta_id) REFERENCES perguntas (id)
);

CREATE TABLE IF NOT EXISTS progresso (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    historia_id INTEGER NOT NULL,
    nivel INTEGER NOT NULL,
    pontos INTEGER NOT NULL,
    acertos INTEGER NOT NULL,
    erros INTEGER NOT NULL,
    data TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
    FOREIGN KEY (historia_id) REFERENCES historias (id)
);

-- Etapa 10: Conquistas / medalhas
CREATE TABLE IF NOT EXISTS medalhas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    icone TEXT NOT NULL DEFAULT '🏅'
);

CREATE TABLE IF NOT EXISTS usuario_medalhas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    medalha_id INTEGER NOT NULL,
    data_conquista TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
    FOREIGN KEY (medalha_id) REFERENCES medalhas (id),
    UNIQUE (usuario_id, medalha_id)
);

-- Etapa 11: Configurações do usuário
CREATE TABLE IF NOT EXISTS configuracoes (
    usuario_id INTEGER PRIMARY KEY,
    som_ativado INTEGER NOT NULL DEFAULT 1,
    animacoes_ativadas INTEGER NOT NULL DEFAULT 1,
    lembrete_diario INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
);

-- Etapa 12: Área dos pais (vínculo responsável <-> criança)
CREATE TABLE IF NOT EXISTS vinculos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    responsavel_id INTEGER NOT NULL,
    crianca_id INTEGER NOT NULL,
    data_vinculo TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (responsavel_id) REFERENCES usuarios (id),
    FOREIGN KEY (crianca_id) REFERENCES usuarios (id),
    UNIQUE (responsavel_id, crianca_id)
);

-- Etapa 17: Índices para acelerar as consultas mais frequentes
CREATE INDEX IF NOT EXISTS idx_perguntas_historia_id ON perguntas (historia_id);
CREATE INDEX IF NOT EXISTS idx_respostas_usuario_id ON respostas (usuario_id);
CREATE INDEX IF NOT EXISTS idx_respostas_pergunta_id ON respostas (pergunta_id);
CREATE INDEX IF NOT EXISTS idx_progresso_usuario_id ON progresso (usuario_id);
CREATE INDEX IF NOT EXISTS idx_progresso_historia_id ON progresso (historia_id);
CREATE INDEX IF NOT EXISTS idx_usuario_medalhas_usuario_id ON usuario_medalhas (usuario_id);
CREATE INDEX IF NOT EXISTS idx_vinculos_responsavel_id ON vinculos (responsavel_id);
CREATE INDEX IF NOT EXISTS idx_vinculos_crianca_id ON vinculos (crianca_id);
CREATE INDEX IF NOT EXISTS idx_historias_nivel ON historias (nivel);

-- Etapa 19: Tokens de API para autenticação do app móvel (alternativa à sessão do navegador)
CREATE TABLE IF NOT EXISTS api_tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    token TEXT NOT NULL UNIQUE,
    criado_em TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
);
CREATE INDEX IF NOT EXISTS idx_api_tokens_token ON api_tokens (token);
