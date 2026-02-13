# GitLab Webhook Agent

API em FastAPI para receber e processar webhooks do GitLab. Ideal para integrar eventos do GitLab (como criação de issues) com outros sistemas ou automações.

## Tecnologias

- **Python 3.x**
- **FastAPI** – API moderna e assíncrona
- **Uvicorn** – servidor ASGI
- **python-dotenv** – variáveis de ambiente

## Pré-requisitos

- Python 3.10 ou superior
- pip

## Instalação com Docker

Para facilitar a execução e o desenvolvimento, o projeto inclui uma configuração com [Docker e Docker Compose](https://docs.docker.com/engine/install/).

Estas serão as dependências necessárias na sua máquina. Se você já tem o Docker instalado, poderá seguir as instruções abaixo para rodar a aplicação usando Docker.

[Leia mais sobre a instalação com Docker](./docs/running-with-docker.md)
## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/LzLuscas/LzLuscas-gitlab-webhook-agent.git
cd LzLuscas-gitlab-webhook-agent
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# Linux/macOS
source venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env` na raiz do projeto com o token que será usado para validar os webhooks do GitLab:

```env
GITLAB_WEBHOOK_TOKEN=seu_token_secreto_aqui
```

> **Importante:** Use o mesmo valor ao configurar o "Secret token" no webhook do GitLab. Nunca commite o arquivo `.env` (ele já está no `.gitignore`).

## Executando

Inicie o servidor com:

```bash
uvicorn app.main:app --reload
```

A API estará disponível em **http://127.0.0.1:8000**.

- Documentação interativa (Swagger): **http://127.0.0.1:8000/docs**
- Health check: **http://127.0.0.1:8000/**

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/` | Health check – retorna `{"status": "ok"}` |
| `POST` | `/webhooks/gitlab/issues` | Recebe webhook de **issues** do GitLab |

### Webhook de issues

O endpoint `/webhooks/gitlab/issues` espera:

- **Body:** JSON com o payload do evento (enviado automaticamente pelo GitLab).
- **Header:** `X-Gitlab-Token` com o mesmo valor definido em `GITLAB_WEBHOOK_TOKEN` (ou o token configurado no código).

Respostas:

- **200** – Webhook recebido e token válido.
- **403** – Token ausente ou inválido.

## Configurando o webhook no GitLab

1. No seu projeto GitLab, vá em **Settings** → **Webhooks**.
2. **URL:** `https://seu-dominio.com/webhooks/gitlab/issues` (ou sua URL pública + `/webhooks/gitlab/issues`).
3. **Secret token:** o mesmo valor de `GITLAB_WEBHOOK_TOKEN` no `.env`.
4. Em **Trigger**, marque pelo menos **Issues events**.
5. Salve o webhook.

Para testar em ambiente local, use um túnel (por exemplo [ngrok](https://ngrok.com)) e use a URL gerada + `/webhooks/gitlab/issues`.

## Estrutura do projeto

```
gitlab-webhook-agent/
├── app/
│   ├── core/
│   │   └── config.py      # Configuração e variáveis de ambiente
│   ├── routes/
│   │   └── gitlab.py      # Rotas dos webhooks GitLab
│   └── main.py            # Aplicação FastAPI
├── .env                    # Suas variáveis (não versionado)
├── .gitignore
├── requirements.txt
└── README.md
```

## Licença

Uso livre para estudo e projetos pessoais. Ajuste conforme sua necessidade.
