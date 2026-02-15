"""Configuração e variáveis de ambiente da aplicação."""

import os
from dotenv import load_dotenv

load_dotenv()

GITLAB_WEBHOOK_TOKEN = os.getenv("GITLAB_WEBHOOK_TOKEN")
