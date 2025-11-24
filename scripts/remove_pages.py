import os
from pathlib import Path

from PyPDF2 import PdfReader, PdfWriter

from scripts.check_interval import check_interval

## Remove pages from a PDF file

def remove_pages(file: str, start: int, end, output_dir='./output'):
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
        output_dir (str, optional): The folder where the new, trimmed PDF
                                    will be saved. Defaults to './output'.
    """
        
    # check pages interval
    if check_interval(file, start, end):
        reader = PdfReader(file)
        pages = reader.pages
        pdf_length = len(pages)
    else:
        print("Page interval is not valid. Removal aborted.")
        return

    # modify start and end for 0-indexing
    start, end = start - 1, end - 1

    # select pages to extract
    pages_to_be_kept = [pages[i] for i in range(pdf_length)
                        if i not in range(start , end + 1) ]

    # add pages to writer object
    writer = PdfWriter()
    for page in pages_to_be_kept:
        writer.add_page(page)

    # create the output folder
    os.makedirs(output_dir, exist_ok=True)

    # create output filename
    filename = Path(file).stem
    output_filename = f'{output_dir}/{filename}_trimmed.pdf'

    # save the new PDF
    with open(output_filename, 'wb') as file:
            writer.write(file)