from fastapi import APIRouter, Body, Header, HTTPException, status

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
    payload: dict = Body(...),
    x_gitlab_token: str = Header(..., alias="X-Gitlab-Token")
):
    if x_gitlab_token != "super_secret_token_123":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token inválido"
        )

    print("🔐 Webhook autenticado com sucesso")
    print(payload)

    return {"message": "Webhook recebido e autenticado"}
