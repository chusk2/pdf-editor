from pathlib import Path
import io

from PyPDF2 import PdfReader, PdfWriter

from scripts.check_interval import check_interval

### Insert pages from pdf

def insert_pages(source_file, inserted_file, insert_pos: int, relative_pos: str,
                 start_insertion = None, end_insertion = None):
    """
    Inserts pages from one PDF into another.

    This feature allows you to take all pages (or a specific range of pages)
    from a second PDF and merge them into your main PDF. You can choose
    exactly where you want the new pages to go.

    For example, you can insert pages from 'report.pdf' either 'before' or
    'after' page 5 of your 'main_document.pdf'.

    Args:
        source_file (str): The path to the main PDF file you are adding pages to.
        inserted_file (str): The path to the PDF file containing the pages you
                           want to insert.
        insert_pos (int): The page number in the main PDF that will be the
                          reference point for the insertion.
        relative_pos (str): Determines where to place the new pages.
                            Use 'before' or 'after' the `insert_pos`.
        start_insertion (int, optional): The first page of the range to copy from
                                      the `inserted_file`. Defaults to the first page.
        end_insertion (int, optional): The last page of the range to copy from
                                    the `inserted_file`. Defaults to the last page.
    """

    # check if relative_pos is valid
    if relative_pos not in ['before', 'after']:
        print("Error: invalid relative position value. Use 'before' or 'after'.")
        return

    # read source file
    source_reader = PdfReader(source_file)
    source_length = len(source_reader.pages)
    source_pages = source_reader.pages

    # check if the insert point is within source pdf pages range
    if  insert_pos < 1:
        print('Error: minimum insert position is 1.')
        return
    elif insert_pos > source_length:
        print(f'Error: insert page position ({insert_pos}) is greater than the PDF file length ({source_length} pages).')
        return 
    
    
    # read the inserted_file to check its length
    insert_reader = PdfReader(inserted_file)
    insert_length = len(insert_reader.pages)

    # if start_insertion is None, assign it to be first page
    if not start_insertion:
        start_insertion = 1
    # if end_insertion is None, assign it to be last page
    if not end_insertion:
        end_insertion = insert_length

    # check pages interval
    if check_interval(inserted_file, start_insertion, end_insertion):
        insert_pages = insert_reader.pages[start_insertion - 1 : end_insertion]
        insert_length = len(insert_pages)
    else:
        print("Error: page interval check for insertion pdf failed. Insertion aborted.")
        return
    
    ## write the pages
    
    # adjust the insert_pos to be 0-indexing compliant
    insert_pos -= 1

    ## insert pages before
    if relative_pos == 'before':
        writer = PdfWriter()
        for i in range(source_length):

            # if current page is the insert position
            if insert_pos == i:

                # add the insertion pages before insert position
                for j in range(insert_length):
                    writer.add_page(insert_pages[j])

                # add insertion page from source pdf
                writer.add_page(source_pages[i])
            
            # add regular pages from source pdf
            else:
                writer.add_page(source_pages[i])

    
    ## insert pages after
    if relative_pos == 'after':
        writer = PdfWriter()
        for i in range(source_length):

            # if current page is the insert position
            if insert_pos  == i:

                # add insertion page from source pdf
                writer.add_page(source_pages[i])

                # add the insertion pages after insert position
                for j in range(insert_length):
                    writer.add_page(insert_pages[j])
            
            # add regular pages from source pdf
            else:
                writer.add_page(source_pages[i])
    
    ## write the output file

    # create output filename
    filename = Path(source_file.name)
    output_filename = f'{filename.stem}_expanded.pdf'

    # create a memory buffer to store output pdf
    output_buffer = io.BytesIO()
    writer.write(output_buffer)

    return output_buffer, output_filename
        
