from pydantic import BaseModel

import jwt

from fastapi import Depends, HTTPException, status, FastAPI
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from electricity_rag.rag_pipeline import answer_question
from electricity_rag.auth import verify_password, create_access_token, decode_access_token
from electricity_rag.db import SessionLocal
from electricity_rag.models import User

class QuestionRequest(BaseModel):
    question: str


class CitedSource(BaseModel):
    document_title: str
    document_source: str


class QuestionResponse(BaseModel):
    answer: str
    sources: list[CitedSource]


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_username(token: str = Depends(oauth2_scheme)) -> str:
    try:
        return decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with SessionLocal() as session:
        user = session.query(User).filter_by(username=form_data.username).first()

        if user is None or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos",
            )

        access_token = create_access_token(user.username)
        return {"access_token": access_token, "token_type": "bearer"}
    

@app.post("/ask", response_model=QuestionResponse)
def ask(request: QuestionRequest, username: str = Depends(get_current_username)) -> QuestionResponse:
    rag_answer = answer_question(request.question)
    cited_sources = [
        CitedSource(
            document_title=source.document_title,
            document_source=source.document_source,
        )
        for source in rag_answer.sources
    ]
    return QuestionResponse(answer=rag_answer.answer, sources=cited_sources)
