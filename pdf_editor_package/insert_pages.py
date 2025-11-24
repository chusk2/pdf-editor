from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
from pdf_editor_package.check_interval import check_interval

### Insert pages from pdf

def insert_pages(source_file: str, insert_file: str, insert_pos: int, relative_pos: str, output_dir='./output',
                 start_insert = None, end_insert = None):
    """
    Inserts pages from one PDF into another.

    This feature allows you to take all pages (or a specific range of pages)
    from a second PDF and merge them into your main PDF. You can choose
    exactly where you want the new pages to go.

    For example, you can insert pages from 'report.pdf' either 'before' or
    'after' page 5 of your 'main_document.pdf'.

    Args:
        source_file (str): The path to the main PDF file you are adding pages to.
        insert_file (str): The path to the PDF file containing the pages you
                           want to insert.
        insert_pos (int): The page number in the main PDF that will be the
                          reference point for the insertion.
        relative_pos (str): Determines where to place the new pages.
                            Use 'before' or 'after' the `insert_pos`.
        output_dir (str, optional): The folder where the new, combined PDF
                                    will be saved. Defaults to './output'.
        start_insert (int, optional): The first page of the range to copy from
                                      the `insert_file`. Defaults to the first page.
        end_insert (int, optional): The last page of the range to copy from
                                    the `insert_file`. Defaults to the last page.
    """

    if relative_pos not in ['before', 'after']:
        print("Invalid relative position value. Use 'before' or 'after'.")
        return

    # read source file
    source_reader = PdfReader(source_file)
    source_length = len(source_reader.pages)
    source_pages = source_reader.pages

    # check if the insert point is within source pdf pages range
    if  insert_pos < 1:
        print('Minimum insert position is 1!')
        return
    elif insert_pos > source_length:
        print(f'PDF file to be inserted to has {source_length} but insert page ({insert_pos} is greater.')
        return 
    
    # read file and check insert_pos is ok
    
    # read the insert_file to check its size
    insert_reader = PdfReader(insert_file)
    insert_length = len(insert_reader.pages)

    # if start_insert is None, assign it to first page
    if not start_insert:
        start_insert = 1
    # if end_insert is None, assign it to last page
    if not end_insert:
        end_insert = insert_length

    # check pages interval
    if check_interval(insert_file, start_insert, end_insert):
        insert_pages = insert_reader.pages[start_insert - 1 : end_insert]
        insert_length = len(insert_pages)
    else:
        return
    
    # write the pages
    
    # adjust the insert_pos to zero index
    insert_pos -= 1

    # insert pages before
    if relative_pos == 'before':
        writer = PdfWriter()
        for i in range(source_length):
            if insert_pos  == i:
                # add the insert pages before insert position
                for j in range(insert_length):
                    writer.add_page(insert_pages[j])
                # insert current page
                writer.add_page(source_pages[i])
            else:
                writer.add_page(source_pages[i])

    
    # insert pages after
    if relative_pos == 'after':
        writer = PdfWriter()
        for i in range(source_length):
            if insert_pos  == i:
                # insert current page
                writer.add_page(source_pages[i])
                # add the insert pages after insert position
                for j in range(insert_length):
                    writer.add_page(insert_pages[j])
            else:
                writer.add_page(source_pages[i])
    
    # write the output file
    filename = Path(source_file).stem
    output_file = f'{output_dir}/{filename}_expanded.pdf'
    with open(output_file, 'wb') as output_file:
        writer.write(output_file)
        

