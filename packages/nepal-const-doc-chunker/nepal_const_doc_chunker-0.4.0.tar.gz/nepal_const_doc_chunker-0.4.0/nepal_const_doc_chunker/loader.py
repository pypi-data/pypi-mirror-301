import os
from typing import Union
from loguru import logger
from langchain_community.document_loaders import PyMuPDFLoader

def load_pdf(file_path: str, verbose: bool=False) -> Union[list[dict], None]:
    """Loads a PDF file and returns its content as a list of dictionaries, or None if unsuccessful."""
    
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension != '.pdf': # validate pdf file only
        logger.error(f"Invalid file type: {file_extension}. Expected a .pdf file.")
        raise ValueError("Invalid file type. Expected a .pdf file.")
    
    try:
        if verbose: logger.info(f"Attempting to load PDF from {file_path}")
        loader = PyMuPDFLoader(
            file_path=file_path,
            extract_images=False # Images are excluded.
        )
        if verbose: logger.info("PDF loaded successfully")
        return loader.load()

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise e

    except Exception as e: # Catch any other unexpected errors that might occur and log them
        logger.error(f"An error occurred while loading the PDF: {e}")
        raise e
