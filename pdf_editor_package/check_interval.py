from PyPDF2 import PdfReader
from pathlib import Path

def check_interval(file, start, end):
    if end < start:
        print('Start page cannot be lower than end page!')
        return None
        
    # read pdf file
    reader = PdfReader(file)
    pdf_length = len(reader.pages)
    print(f'The PDF file has {pdf_length} pages.')

    # check start and end pages are within pages range
    if start > pdf_length or end > pdf_length:
        print('The extract interval is out of the PDF pages range!')
        return None
    else:
        return True