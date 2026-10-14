
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.llm import generate_sql
from src.analytics import run_read_query

app = FastAPI(
    title="AI Data Analyst Copilot",
    description="Ask business questions about your MySQL data.",
    version="1.0.0",
)


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)


@app.get("/")
def home():
    return {
        "message": "AI Data Analyst Copilot API is running"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        sql = generate_sql(request.question)
        result = run_read_query(sql)

        return {
            "question": request.question,
            "sql": result["sql"],
            "row_count": result["row_count"],
            "results": result["rows"],
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        # Log details in the server terminal, not in the API response.
        print(f"Question processing failed: {error}")
        raise HTTPException(
            status_code=500,
            detail="Unable to process the question. Check server logs.",
        ) from error
