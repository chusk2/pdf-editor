import os
from pathlib import Path
import io

from PyPDF2 import PdfReader, PdfWriter


## Extract pages from a PDF file

def extract_pages(file, start: int, end: int):
    """
    Extracts a range of pages from a PDF and saves them as a new file.

    Select a starting and an ending page from your PDF to create a new, smaller
    PDF containing only the pages within that range (inclusive).

    For example, if you choose start=3 and end=5, the new PDF will contain
    pages 3, 4, and 5 from the original file.

    Args:
        file (str): The path to the PDF file you want to extract pages from.
        start (int): The first page number of the range to extract.
        end (int): The last page number of the range to extract.
    """
        
    reader = PdfReader(file)
    pages = reader.pages

    # modify start and end for 0-indexing
    start, end = start - 1, end - 1

    # select pages to extract
    pages_to_extract = pages[start : end + 1]

    # write pages to output file
    writer = PdfWriter()
    for page in pages_to_extract:
        writer.add_page(page)

    # create output filename
    file_path = Path(file.name)
    filename = file_path.stem
    output_filename = f'{filename}_extracted.pdf'

    # create a memory buffer to store output pdf
    output_buffer = io.BytesIO()
    writer.write(output_buffer)

    return output_buffer, output_filename

