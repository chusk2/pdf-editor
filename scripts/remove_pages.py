import os
from pathlib import Path
import io

from PyPDF2 import PdfReader, PdfWriter


## Remove pages from a PDF file

def remove_pages(file, start: int, end: int):
    """
    Removes a range of pages from a PDF file.

    This feature creates a new PDF that excludes the pages you specify. Select
    a starting and an ending page to remove that entire range (inclusive).

    For example, if you choose start=3 and end=5, the new PDF will contain
    all pages from the original except for pages 3, 4, and 5.

    Args:
        file (str): The path to the PDF file you want to remove pages from.
        start (int): The first page number of the range to delete.
        end (int): The last page number of the range to delete.
    """

    reader = PdfReader(file)
    pages = reader.pages
    pdf_length = len(pages)

    # modify start and end for 0-indexing
    start, end = start - 1, end - 1

    # select pages to extract
    pages_to_be_kept = [pages[i] for i in range(pdf_length)
                        if i not in range(start , end + 1) ]

    # add pages to writer object
    writer = PdfWriter()
    for page in pages_to_be_kept:
        writer.add_page(page)

    # create output filename
    file_path = Path(file.name)
    filename = file_path.stem
    output_filename = f'{filename}_trimmed.pdf'

    # create a memory buffer to store output pdf
    output_buffer = io.BytesIO()
    writer.write(output_buffer)

    return output_buffer, output_filename