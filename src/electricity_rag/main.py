from pydantic import BaseModel
from fastapi import FastAPI

from electricity_rag.rag_pipeline import answer_question

class QuestionRequest(BaseModel):
    question: str


class CitedSource(BaseModel):
    document_title: str
    document_source: str


class QuestionResponse(BaseModel):
    answer: str
    sources: list[CitedSource]


app = FastAPI()

@app.post("/ask", response_model=QuestionResponse)
def ask(request: QuestionRequest) -> QuestionResponse:
    rag_answer = answer_question(request.question)
    cited_sources = [
        CitedSource(
            document_title=source.document_title,
            document_source=source.document_source,
        )
        for source in rag_answer.sources
    ]
    return QuestionResponse(answer=rag_answer.answer, sources=cited_sources)
