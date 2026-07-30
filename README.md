# INTERPRETA+ (Fase 1 – MVP completo, 20/20 etapas)

Plataforma de treino de interpretação de linguagem e cognição social, no estilo Duolingo.

> ✅ As 20 etapas planejadas para o MVP foram implementadas, testadas isoladamente e
> testadas **integradas entre si** (veja o [CHANGELOG.md](./CHANGELOG.md) para o resumo
> etapa por etapa).

## O que já funciona nesta versão

- Estrutura completa do projeto (rotas → services → models → banco), pronta para
  receber IA, jogos e vídeos nas próximas fases sem reescrever o código.
- Cadastro e login de usuário (senha com hash).
- Dashboard com nível, pontos, dias de estudo e sequência.
- Treino diário: história → perguntas de múltipla escolha → correção automática → pontuação.
- Progresso salvo no banco (SQLite) e subida automática de nível.
- Tela de perfil com histórico de atividades.
- **Conquistas/medalhas** concedidas automaticamente (primeira história, sequência de dias,
  100 pontos, gabarito, subida de nível), com tela dedicada mostrando conquistadas e bloqueadas.
- **Configurações**: preferências de som/animações/lembrete e troca de senha.
- **Área dos pais**: conta do tipo "responsável", vincula-se à conta da criança pelo e-mail
  e acompanha dias estudados, sequência, pontos, nível e desempenho por área/categoria.
- **Biblioteca de conteúdo**: lista todas as histórias organizadas por nível, permitindo
  praticar qualquer uma livremente (além do treino diário sequencial).
- **Administração**: painel para cadastrar, editar e excluir histórias e perguntas sem
  programar (login: `admin@interpreta.com` / `admin123`, criado automaticamente pelo seed).
- **API interna** (`/api/v1/...`): endpoints JSON autenticados por sessão para o usuário
  logado consultar seus próprios dados — usados como base para o futuro app móvel e para a IA.
- **Testes automatizados**: 26 testes cobrindo autenticação, treino/pontuação, conquistas,
  administração e API interna (veja "Como rodar os testes" abaixo).
- **Otimizações**: índices no banco para as consultas mais usadas, modo WAL do SQLite
  (melhor leitura/escrita concorrente) e configuração separada para desenvolvimento/produção.
- **Preparação para IA** (`services/ia_service.py`): gera uma frase motivadora personalizada
  no final de cada treino. Funciona 100% offline por padrão ("modo simulado"); basta trocar
  uma variável de ambiente para plugar a IA real no futuro, sem mudar nenhuma rota.
- **Preparação para app móvel**: a API interna agora aceita login por token
  (`POST /api/v1/auth/login`), além da sessão do navegador, e responde com cabeçalhos CORS —
  pronta para ser consumida por um app iOS/Android/React Native.
- Visual colorido, botões grandes, barra de status e responsivo (estilo Duolingo).

## Como rodar

```bash
cd interpreta
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Cria o banco e popula com histórias de exemplo
python database/seed.py

# Inicia o servidor
python app.py
```

Acesse http://127.0.0.1:5000 no navegador, crie uma conta e comece o treino.

## Estrutura do projeto

```
interpreta/
├── app.py                   # ponto de entrada (cria a app e registra as rotas)
├── config.py                 # configurações (chave secreta, banco, IA, CORS)
├── requirements.txt
├── requirements-dev.txt        # + pytest, para rodar os testes
├── pytest.ini
├── CHANGELOG.md                # resumo das 20 etapas implementadas
├── database/
│   ├── schema.sql             # criação das tabelas + índices
│   └── seed.py                # popula histórias, medalhas e a conta admin
├── models/                    # acesso ao banco (uma tabela por arquivo)
├── services/                   # regras de negócio (correção, pontuação, nível, IA)
├── routes/                     # rotas Flask (auth, dashboard, admin, api, etc.)
├── templates/                   # HTML (Jinja2)
├── static/
│   ├── css/style.css           # visual estilo Duolingo
│   └── js/main.js
├── data/                       # conteúdo inicial (histórias, medalhas), separado do código
├── tests/                      # 37 testes automatizados (pytest)
└── utils/helpers.py             # decorators de autenticação (web, admin, API)
```

## Funcionalidades da Fase 1 (conforme planejado)

| Item                     | Status |
|--------------------------|--------|
| Login                    | ✅ |
| Cadastro                 | ✅ |
| Dashboard                | ✅ |
| Ler história              | ✅ |
| Responder perguntas        | ✅ |
| Corrigir automaticamente    | ✅ |
| Pontuação                 | ✅ |
| Salvar progresso           | ✅ |
| Perfil                    | ✅ |
| Conquistas / Medalhas       | ✅ |
| Configurações              | ✅ |
| Área dos Pais              | ✅ |
| Biblioteca de Conteúdo       | ✅ |
| Administração               | ✅ |
| API interna                | ✅ |
| Testes automatizados        | ✅ |
| Otimização (índices/WAL)    | ✅ |
| Preparação para IA          | ✅ |
| Preparação para app móvel    | ✅ |
| IA de verdade / App móvel publicado | ❌ (fases 3 e 4 completas) |

## Como rodar os testes

```bash
pip install -r requirements-dev.txt
pytest
```

Os testes usam um banco SQLite temporário e isolado (criado e apagado automaticamente
a cada execução), então nunca tocam no `database/banco.db` real. Ao todo são 37 testes.

## Ativando a IA de verdade (quando quiser)

Por padrão, o feedback ao final do treino usa frases pré-escritas (modo "simulado"),
sem precisar de internet nem custo algum. Para usar uma IA de verdade:

```bash
pip install anthropic
export IA_PROVIDER=anthropic
export ANTHROPIC_API_KEY=sua-chave-aqui
```

Se a chamada à IA falhar por qualquer motivo (sem internet, chave inválida, etc.), o
sistema cai automaticamente de volta no modo simulado — a criança nunca fica sem feedback.

## Rodando em produção

Antes de colocar em produção:

1. Defina uma `SECRET_KEY` própria via variável de ambiente:
   ```bash
   export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
   export FLASK_DEBUG=0
   ```
2. Use um servidor WSGI de verdade em vez do `python app.py` (que é só para desenvolvimento):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

## Endpoints da API interna

Aceitam DOIS métodos de autenticação:
- **Sessão do navegador** (já logado via `/login`)
- **Token** (app móvel): faça login em `/api/v1/auth/login` e envie
  `Authorization: Bearer <token>` nas próximas chamadas.

| Endpoint                    | Método | Descrição |
|------------------------------|--------|-----------|
| `/api/v1/auth/login`          | POST   | Login por token (`email`, `senha`) — retorna `{token, usuario}` |
| `/api/v1/auth/logout`         | POST   | Revoga o token enviado |
| `/api/v1/usuario/me`          | GET    | Dados do usuário logado |
| `/api/v1/historias`           | GET    | Lista todas as histórias disponíveis |
| `/api/v1/progresso/me`        | GET    | Histórico de progresso do usuário logado |
| `/api/v1/relatorio/me`        | GET    | Resumo geral e desempenho por categoria |
| `/api/v1/medalhas/me`         | GET    | Medalhas conquistadas pelo usuário logado |

## Status final

MVP completo — as 20 etapas planejadas estão implementadas e testadas (veja o
[CHANGELOG.md](./CHANGELOG.md) para o detalhamento). O projeto está pronto para:

- Ser usado como está (Fase 1, sem custo de IA);
- Evoluir para a **Fase 3** (IA de verdade — basta configurar `IA_PROVIDER=anthropic`);
- Evoluir para a **Fase 4** (app móvel nativo — a API e a autenticação por token já existem);

sem precisar reescrever rotas, services ou models já construídos.
