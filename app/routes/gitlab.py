"""Rotas para receber e processar webhooks do GitLab."""

from fastapi import APIRouter, Body, Header, HTTPException, status

from app.core.config import GITLAB_WEBHOOK_TOKEN

router = APIRouter(
    prefix="/webhooks/gitlab",
    tags=["GitLab"]
)


@router.post(
    "/issues",
    summary="Recebe webhook de issues do GitLab",
    description="Endpoint seguro para receber eventos de criação de issues"
)
async def receive_issue_webhook(
    payload: dict = Body(default=dict),
    x_gitlab_token: str = Header(..., alias="X-Gitlab-Token")
):
    """Recebe e valida o webhook de issues enviado pelo GitLab."""
    if not GITLAB_WEBHOOK_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Webhook não configurado: GITLAB_WEBHOOK_TOKEN ausente no servidor"
        )

    if x_gitlab_token != GITLAB_WEBHOOK_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token inválido"
        )

    print("🔐 Webhook autenticado com sucesso")
    print(payload)

    return {"message": "Webhook recebido e autenticado"}
