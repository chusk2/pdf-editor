from PyPDF2 import PdfReader

def check_interval(file, start: int, end:int):
    """
    Checks if a given page interval is valid for a PDF file.

    This is an internal utility function to ensure that the start and end pages
    for an operation are within the bounds of the PDF's total page count and
    that the start page is not greater than the end page.

    Args:
        file (str or Path): The path to the PDF file.
        start (int): The starting page number of the interval (1-based).
        end (int): The ending page number of the interval (1-based).

    Returns:
        bool: True if the interval is valid, None otherwise.
    """
    if end < start:
        print('Error: start page cannot be lower than end page.')
        return
        
    # read pdf file
    reader = PdfReader(file)
    pdf_length = len(reader.pages)

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