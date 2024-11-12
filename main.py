from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi import FastAPI, File, UploadFile
from app.dependencies import get_embeddings
from lib import parse_json_doc, parse_pdf, parse_json_question, completion_prompt_list
from app import get_vector_store
from loguru import logger
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()


@app.post("/upload")
async def upload_file(
    question: UploadFile = File(...),
    doc: UploadFile = File(...),
    vector_store=Depends(get_vector_store),
    embeddings=Depends(get_embeddings),
):
    if doc.content_type == "application/pdf":
        await parse_pdf(doc, vector_store, embeddings)
    elif doc.content_type == "application/json":
        await parse_json_doc(doc, vector_store, embeddings)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only PDF and JSON files are supported",
        )

    if question.content_type == "application/json":
        questions = await parse_json_question(question, vector_store, embeddings)
        return await completion_prompt_list(questions, vector_store)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only JSON files are supported",
        )
