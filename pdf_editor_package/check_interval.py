from PyPDF2 import PdfReader
from pathlib import Path

def check_interval(file, start, end):
    if end < start:
        print('Error: start page cannot be lower than end page.')
        return
        
    # read pdf file
    reader = PdfReader(file)
    pdf_length = len(reader.pages)
    # print(f'The PDF file has {pdf_length} pages.')

    # check start and end pages are within pages range
    if start > pdf_length or end > pdf_length:
        print('Error: extract interval is out of boundaries of the PDF pages range.')
        if start > pdf_length:
            print(f'Start page must be between 1 and {pdf_length}.')
        elif end > pdf_length:
            print(f'End page must be between 1 and {pdf_length}.')

        return
    else:
        return True