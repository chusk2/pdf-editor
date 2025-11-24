import os
from pathlib import Path

from PyPDF2 import PdfReader, PdfWriter

from pdf_editor_package.check_interval import check_interval

## Extract pages from a PDF file

def extract_pages(file: str, start: int, end: int, output_dir='./output'):
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
        output_dir (str, optional): The folder where the new, extracted PDF
                                    will be saved. Defaults to './output'.
    """
        
    # check pages interval
    if check_interval(file, start, end):
        reader = PdfReader(file)
        pages = reader.pages
    else:
        print("Page interval check failed. Extraction aborted.")
        return

    # modify start and end for 0-indexing
    start, end = start - 1, end - 1

    # select pages to extract
    pages_to_extract = pages[start : end + 1]

    # write pages to output file
    writer = PdfWriter()
    for page in pages_to_extract:
        writer.add_page(page)

    # create output folder
    os.makedirs(output_dir, exist_ok=True)

    # create output filename
    filename = Path(file).stem
    output_filename = f'{output_dir}/{filename}_extracted.pdf'

    # save new pdf
    with open(output_filename, 'wb') as file:
            writer.write(file)