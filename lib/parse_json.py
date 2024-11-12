import os
import aiofiles
import json
from pydoc import text
from fastapi import HTTPException, UploadFile, status
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import JSONLoader
from loguru import logger


async def parse_json_doc(
    json_file: UploadFile, vector_store: InMemoryVectorStore, embeddings
):
    """Parse a JSON file and store the text in a vector store.

    Args:
        json_file (UploadFile): The JSON file to parse.
        vectore_store (InMemoryVectorStore): The vector store to store the text in.
    """
    logger.debug("Parsing Doc JSON file")
    CHUNK_SIZE = 1024
    try:
        filepath = os.path.join("./", os.path.basename(json_file.filename))
        async with aiofiles.open(filepath, "wb") as f:
            while chunk := await json_file.read(CHUNK_SIZE):
                await f.write(chunk)
        loader = JSONLoader(filepath, jq_schema=".docs", text_content=False)
        data = loader.load()
        vector_store.from_documents(data, embedding=embeddings)
        os.remove(filepath)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="There was an error uploading the file",
        )
    finally:
        await json_file.close()


async def parse_json_question(
    json_file: UploadFile, vector_store: InMemoryVectorStore, embeddings
):
    """Parse a JSON file and store the text in a vector store.

    Args:
        json_file (UploadFile): The JSON file to parse.
        vectore_store (InMemoryVectorStore): The vector store to store the text in.
    """
    logger.debug("Parsing Question JSON file")
    try:
        json_str = await json_file.read()
        json_data = json.loads(json_str)
        return json_data["questions"]
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="There was an error uploading the file",
        )
