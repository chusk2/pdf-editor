from pathlib import Path
import io

from PyPDF2 import PdfReader, PdfWriter


### Insert pages from pdf

def insert_pages(insertion_file,
                 start_insertion = None, end_insertion = None):
    """
    Extracts a range of pages from a given PDF file.

    Args:
        insertion_file: The PDF file containing the pages you
                           want to insert.
        start_insertion (int, optional): The first page of the range to copy from
                                      the `inserted_file`. Defaults to the first page.
        end_insertion (int, optional): The last page of the range to copy from
                                    the `inserted_file`. Defaults to the last page.
    """

    insert_reader = PdfReader(insertion_file)
    insert_length = len(insert_reader.pages)

    # Use the full range if start/end are not specified
    start = start_insertion if start_insertion else 1
    end = end_insertion if end_insertion else insert_length

    # Return a list of the page objects to be inserted
    return insert_reader.pages[start - 1 : end]
