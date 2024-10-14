from loguru import logger
from .chunking import load_and_chunk_pdf_content

def load_and_chunk_const_doc(file_path: str, verbose: bool=False) -> list[dict]:
    """
    Main function to load the PDF file, chunk the content, and return it.
    
    Returns:
    list[dict]: A list of dictionaries where each dictionary maps metadata to a chunk of text.
    """
    if not file_path:
        raise ValueError("Nepal Constitution 2072 PDF file path is required.")
    
    # Load and chunk the PDF content into text chunks and their corresponding metadata
    try:
        chunked_data_dict_list = load_and_chunk_pdf_content(file_path=file_path, verbose=verbose)
    except Exception as e:
        logger.error(f"Error loading and chunking PDF content, provide the valid PDF file path")
        raise e

    return chunked_data_dict_list
