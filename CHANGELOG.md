# CHANGELOG — INTERPRETA+ (Fase 1, MVP completo)

Todas as 20 etapas do cronograma planejado foram implementadas e testadas
integradas entre si (não só isoladamente).

## Etapas 1–9 — Base do produto
1. **Arquitetura do sistema**: rotas → services → models → banco, desacoplada
   para as próximas fases (IA, app móvel) não exigirem reescrita.
2. **Cadastro e login** com senha protegida por hash (Werkzeug).
3. **Dashboard** com nível, pontos, dias de estudo e sequência.
4. **Treino diário**: história do dia escolhida automaticamente pelo nível do usuário.
5. **Perguntas de múltipla escolha** vinculadas a cada história.
6. **Correção automática** das respostas.
7. **Pontuação** (0–100) calculada pela proporção de acertos.
8. **Progresso salvo** no banco, com subida automática de nível.
9. **Perfil** com histórico de atividades.

## Etapas 10–13 — Engajamento e conteúdo
10. **Conquistas/medalhas** concedidas automaticamente (primeira história, sequência
    de dias, 100 pontos, gabarito, subida de nível).
11. **Configurações**: preferências de som/animação/lembrete e troca de senha.
12. **Área dos pais**: conta tipo "responsável", vínculo por e-mail, relatório de
    desempenho geral e por categoria/habilidade.
13. **Biblioteca de conteúdo**: todas as histórias navegáveis por nível, com prática livre.

## Etapas 14–17 — Infraestrutura
14. **Administração**: painel para cadastrar/editar/excluir histórias e perguntas
    sem programar (conta admin criada automaticamente pelo seed).
15. **API interna** (`/api/v1/...`): endpoints JSON para consultar dados do usuário logado.
16. **Testes automatizados**: 37 testes com `pytest` cobrindo os fluxos principais.
17. **Otimização**: índices no banco, modo WAL do SQLite, config de produção.

## Etapas 18–20 — Preparação para o futuro
18. **Preparação para IA**: feedback motivacional gerado após cada treino, com modo
    simulado (offline, sem custo) e ponto de extensão pronto para IA real.
19. **Preparação para app móvel**: login por token (`/api/v1/auth/login`) e CORS,
    para um app iOS/Android/React Native consumir a mesma API sem duplicar lógica.
20. **Consolidação final do MVP**: revisão de ponta a ponta simulando um dia real
    de uso — admin cadastra conteúdo, criança treina e recebe feedback, responsável
    acompanha o progresso, app móvel consulta os dados via token — tudo integrado.

## Não incluído neste MVP (fases futuras, fora do escopo desta entrega)

- IA de verdade (o gancho existe em `services/ia_service.py`, mas não é chamado por padrão)
- Ranking entre usuários
- Vídeos e jogos interativos
- App móvel nativo publicado (a API já está pronta para consumo por um)
