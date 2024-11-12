import os
import aiofiles
from fastapi import HTTPException, UploadFile, status
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import PyPDFLoader
from loguru import logger
from langchain_text_splitters import RecursiveCharacterTextSplitter


async def parse_pdf(
    pdf_file: UploadFile,
    vector_store: InMemoryVectorStore,
    embeddings,
):
    """Parse a PDF file and store the text in a vector store.

    Args:
        pdf_file (UploadFile): The PDF file to parse.
        vectore_store (InMemoryVectorStore): The vector store to store the text in.
    """
    CHUNK_SIZE = 1024
    pages = []
    logger.debug("Parsing PDF file")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    try:
        filepath = os.path.join("./", os.path.basename(pdf_file.filename))
        async with aiofiles.open(filepath, "wb") as f:
            while chunk := await pdf_file.read(CHUNK_SIZE):
                await f.write(chunk)
        loader = PyPDFLoader(filepath)
        async for page in loader.alazy_load():
            pages.append(page)
        splitted = text_splitter.split_documents(pages)
        vector_store.from_documents(splitted, embedding=embeddings)
        os.remove(filepath)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="There was an error uploading the file",
        )
    finally:
        await pdf_file.close()
