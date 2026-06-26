from pydantic import BaseModel, Field


class MailRequest(BaseModel):
    subject: str = Field(..., min_length=1, max_length=50, description="Тема рассылки")
    body: str = Field(..., min_length=1, max_length=500, description="Текст письма")


class MailResponse(BaseModel):
    task_id: str = Field(..., description="ID задачи")
    status: str = Field(..., description="Статус задачи")
