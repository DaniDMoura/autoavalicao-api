from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Subject
from app.schemas import (
  CreateSubject,
  UpdateSubject,
  Subjects,
  ListSubjects,
  DeleteSubjectResponse
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#colocar filtros
@app.get('/', status_code=HTTPStatus.OK, response_model=ListSubjects)
async def list_subjects(session: AsyncSession = Depends(get_session)):
  db_subjects = await session.scalars(select(Subject))
  subjects = db_subjects.all()

  return {"subjects": subjects}

@app.post('/', status_code=HTTPStatus.CREATED, response_model=Subjects)
async def register_subjects(subject: CreateSubject ,session: AsyncSession = Depends(get_session)):

  db_subject = Subject(
    name=subject.name,
    stars=subject.stars,
    subject_type=subject.subject_type
  )

  session.add(db_subject)
  await session.commit()
  await session.refresh(db_subject)

  return db_subject

@app.patch('/{subject_id}', status_code=HTTPStatus.OK, response_model=Subjects)
async def update_subject(subject_id: int, new_subject: UpdateSubject, session: AsyncSession = Depends(get_session)):
  db_subject = await session.scalar(select(Subject).where(Subject.id == subject_id))

  if not db_subject:
      raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='No subject found'
        )

  if new_subject.name is not None:
      db_subject.name = new_subject.name
  if new_subject.stars is not None:
      db_subject.stars = new_subject.stars
  if new_subject.subject_type is not None:
      db_subject.subject_type = new_subject.subject_type

  await session.commit()
  await session.refresh(db_subject)

  return db_subject

@app.delete('/{subject_id}', status_code=HTTPStatus.OK, response_model=DeleteSubjectResponse)
async def delete_subject(subject_id: int, session: AsyncSession = Depends(get_session)):
  db_subject = await session.scalar(select(Subject).where(Subject.id == subject_id))

  if not db_subject:
      raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='No subject found'
        )

  await session.delete(db_subject)
  await session.commit()

  return {"detail": "Delete subject done successfully"}
