from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from backend.app.core.explainer import explain_concept
from backend.app.core.visualizer import generate_visual
from backend.app.core.quizzer import generate_questions, solve_questions, evaluate_answers
from backend.app.core.flashcards import generate_flashcards_api
from backend.app.core.interview import interview_prep
from backend.app.core.resume_reviewer import review_resume
from backend.app.core.summarizer import summarize_text

load_dotenv(dotenv_path="../.env")

app = FastAPI(title="Student Copilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    prompt: str
    context: str = ""
    style: str = "Beginner Friendly"
    api_choice: str = "Gemini"

@app.get("/")
def read_root():
    return {"message": "Welcome to Student Copilot API v1.0", "status": "operational"}

@app.post("/api/explain")
def handle_explain(req: QueryRequest):
    result = explain_concept(
        concept=req.prompt,
        previous_context=req.context,
        answer_style=req.style,
        api_choice=req.api_choice
    )
    return {"response": result}

@app.post("/api/visualize")
def handle_visualize(req: QueryRequest):
    result = generate_visual(
        concept=req.prompt,
        previous_context=req.context,
        api_choice=req.api_choice
    )
    return {"response": result}

class QuizEvalRequest(BaseModel):
    questions: str
    user_answers: str
    context: str = ""
    style: str = "Beginner Friendly"
    api_choice: str = "Gemini"

@app.post("/api/quiz/generate")
def handle_quiz_generate(req: QueryRequest):
    result = generate_questions(
        text=req.prompt,
        previous_context=req.context,
        answer_style=req.style,
        api_choice=req.api_choice
    )
    return {"response": result}

@app.post("/api/quiz/solve")
def handle_quiz_solve(req: QueryRequest):
    result = solve_questions(
        user_questions=req.prompt,
        previous_context=req.context,
        answer_style=req.style,
        api_choice=req.api_choice
    )
    return {"response": result}

@app.post("/api/quiz/evaluate")
def handle_quiz_evaluate(req: QuizEvalRequest):
    result = evaluate_answers(
        questions=req.questions,
        user_answers=req.user_answers,
        previous_context=req.context,
        answer_style=req.style,
        api_choice=req.api_choice
    )
    return {"response": result}

@app.post("/api/flashcards")
def handle_flashcards(req: QueryRequest):
    result = generate_flashcards_api(
        topic=req.prompt,
        previous_context=req.context,
        api_choice=req.api_choice
    )
    return {"response": result}

@app.post("/api/interview")
def handle_interview(req: QueryRequest):
    result = interview_prep(
        user_input=req.prompt,
        level=req.style,
        api_choice=req.api_choice
    )
    return {"response": result}

@app.post("/api/resume")
def handle_resume(req: QueryRequest):
    result = review_resume(
        prompt=req.prompt,
        previous_context=req.context,
        api_choice=req.api_choice
    )
    return {"response": result}

class SummarizeRequest(BaseModel):
    text: str
    context: str = ""
    user_focus: str = ""
    extra_instruction: str = ""
    style: str = "Beginner Friendly"
    api_choice: str = "Gemini"

@app.post("/api/summarize")
def handle_summarize(req: SummarizeRequest):
    result = summarize_text(
        text=req.text,
        previous_context=req.context,
        user_focus=req.user_focus,
        extra_instruction=req.extra_instruction,
        answer_style=req.style,
        api_choice=req.api_choice
    )
    return {"response": result}
