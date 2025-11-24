from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
import os
from pdf_editor_package.check_interval import check_interval
      
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
        
    # check pages interval and read file
    if check_interval(file, start, end):
        reader = PdfReader(file)
        pages = reader.pages
        pdf_length = len(pages)
    else:
        return

    # print(f'File has {pdf_length} pages.')

    # select pages to extract
    pages_to_extract = pages[start -1 : end]

    # write pages to output file
    writer = PdfWriter()
    for page in pages_to_extract:
        writer.add_page(page)

    # create output folder
    os.makedirs(output_dir, exist_ok=True)

    filename = Path(file).stem
    with open(f'{output_dir}/{filename}_extracted.pdf', 'wb') as file:
            writer.write(file)