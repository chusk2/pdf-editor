from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
from pdf_editor_package.check_interval import check_interval

### Insert pages from pdf

def insert_pages(source_file: str, insert_file: str, insert_pos: int, relative_pos: str, output_dir='./output',
                 start_insert = None, end_insert = None):

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
    elif not end_insert:
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
        

