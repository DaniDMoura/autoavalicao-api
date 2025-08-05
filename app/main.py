from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from http import HTTPStatus
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.database import get_session
from app.models import Subject
from app.schemas import (
    UpdateSubject,
    Subjects,
    ListSubjects,
    DeleteSubjectResponse,
    FilterTodo,
    CreateSubject,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://autoavaliacao-theta.vercel.app"
        ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", status_code=HTTPStatus.OK)
async def health_check():
    return JSONResponse(content={"status": "ok"})


@app.get("/autoavalaiacao/", status_code=HTTPStatus.OK, response_model=ListSubjects)
async def list_subjects(
    filter: FilterTodo = Query(None),
    session: AsyncSession = Depends(get_session),
):

    query = select(Subject)

    if filter.name:
        query = query.filter(Subject.name.ilike(f"%{filter.name}%"))

    if filter.subject:
        query = query.filter(Subject.subject_type.in_(filter.subject))

    if filter.stars:
        query = query.filter(Subject.stars == filter.stars)

    db_subjects = await session.scalars(query)
    subjects = db_subjects.all()

    if not subjects:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="No subject found")


    return {"subjects": subjects}


@app.post("/autoavalaiacao/", status_code=HTTPStatus.CREATED, response_model=Subjects)
async def register_subjects(
    subject: CreateSubject,
    session: AsyncSession = Depends(get_session),
):
    db_subject = Subject(name=subject.name, stars=subject.stars, subject_type=subject.subject_type)

    session.add(db_subject)
    await session.commit()
    await session.refresh(db_subject)

    return db_subject


@app.patch("/autoavalaiacao/{subject_id}", status_code=HTTPStatus.OK, response_model=Subjects)
async def update_subject(
    subject_id: int,
    new_subject: UpdateSubject,
    session: AsyncSession = Depends(get_session),
):
    db_subject = await session.scalar(select(Subject).where(Subject.id == subject_id))

    if not db_subject:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No subject found")

    if new_subject.name is not None:
        db_subject.name = new_subject.name
    if new_subject.stars is not None:
        db_subject.stars = new_subject.stars
    if new_subject.subject_type is not None:
        db_subject.subject_type = new_subject.subject_type

    await session.commit()
    await session.refresh(db_subject)

    return db_subject


@app.delete(
    "/autoavalaiacao/{subject_id}", status_code=HTTPStatus.OK, response_model=DeleteSubjectResponse
)
async def delete_subject(subject_id: int, session: AsyncSession = Depends(get_session)):
    db_subject = await session.scalar(select(Subject).where(Subject.id == subject_id))

    if not db_subject:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No subject found")

    await session.delete(db_subject)
    await session.commit()

    return {"detail": "Delete subject done successfully"}
