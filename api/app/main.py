from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from sqlmodel import Session
from datetime import datetime
from .models import Questions
from .services import engine, create_db_and_tables
from .api_jservice import get_date


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/add-questions/{questions_num}", response_model=Questions)
async def add_questions(questions_num: int):
    question_bd = {'id': 0, 'question': '','answer': '',
                 'created_at': datetime.utcnow()}
    with Session(engine) as session:
        questions = {}
        number_of_attempts = 20
        while len(questions) != questions_num:
            questions_api = get_date(questions_num - len(questions))
            new_questions = {item['id']:item for item in questions_api}
            questions = questions | new_questions
            filt_in = questions.keys()
            exist = session.query(Questions).filter(
                Questions.id.in_(filt_in)).all()
            for ex in exist:
                questions.pop(ex.id)
            number_of_attempts -= 1
            if number_of_attempts == 0:
                raise HTTPException(
                    status_code=400, detail="Failed to get the required "\
                      "number of new questions from the external api")
        if len(questions) > 0:
            for question in questions:
                item = questions[question]
                question_bd = Questions(
                    id=item['id'],
                    question=item['question'],
                    answer=item['answer'],
                )
                session.add(question_bd)
            session.commit()
            session.refresh(question_bd)
    return question_bd