from app.data_processing import fetch_examples, tidy_examples
from app.generator import generateTempTextFile, generateTempDocxFile, generateTempPDFFile
from fastapi import FastAPI, Query
from typing import Union
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.background import BackgroundTasks
import time
import os

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def remove_file(path: str) -> None:
    os.unlink(path)


@app.get("/")
def home():
    return {"message": "Hello World"}


@app.get("/getSentences/text")
def getSentencesText(q: Union[list[str], None] = Query(default=None), n: int = 1):
    words = q

    start = time.time()

    examples_list = fetch_examples(words)
    examples_list, answers_list = tidy_examples(words, examples_list, n)

    end = time.time()
    print(f"Time taken for fetching: {end - start}")

    return {"examples": examples_list, "answers": answers_list}


@app.get("/getSentences/textFile")
def getSentencesTextFile(q: Union[list[str], None] = Query(default=None), n: int = 1, background_tasks: BackgroundTasks = BackgroundTasks()):
    words = q

    start = time.time()

    examples_list = fetch_examples(words)
    examples_list, answers_list = tidy_examples(words, examples_list, n)

    end = time.time()
    print(f"Time taken for fetching: {end - start}")

    filePath = generateTempTextFile(examples_list, answers_list)
    background_tasks.add_task(remove_file, filePath)

    return FileResponse(filePath, media_type="text/plain", filename="sentences.txt")


@app.get("/getSentences/docxFile")
def getSentencesDocxFile(q: Union[list[str], None] = Query(default=None), n: int = 1, background_tasks: BackgroundTasks = BackgroundTasks()):
    words = q

    start = time.time()

    examples_list = fetch_examples(words)
    examples_list, answers_list = tidy_examples(words, examples_list, n)

    end = time.time()
    print(f"Time taken for fetching: {end - start}")

    filePath = generateTempDocxFile(examples_list, answers_list)
    background_tasks.add_task(remove_file, filePath)

    return FileResponse(filePath, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename="sentences.docx")


@app.get("/getSentences/pdfFile")
def getSentencesPDFFile(q: Union[list[str], None] = Query(default=None), n: int = 1, background_tasks: BackgroundTasks = BackgroundTasks()):
    words = q

    start = time.time()

    examples_list = fetch_examples(words)
    examples_list, answers_list = tidy_examples(words, examples_list, n)

    end = time.time()
    print(f"Time taken for fetching: {end - start}")

    filePath = generateTempPDFFile(examples_list, answers_list)
    background_tasks.add_task(remove_file, filePath)

    return FileResponse(filePath, media_type="application/pdf", filename="sentences.pdf")
