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

    # from pdf to be inserted there is start page but not end page
    if ( bool(start_insert) + bool(end_insert) ) == 1:
        if start_insert:
            print('A start page in the pdf to insert was provided but not an end page!')
        else:
            print('An end page in the pdf to insert was provided but not a start page!')
        return
    
    # from insert pdf, only a selected interval of pages will be inserted
    if start_insert and end_insert:

        # check pages interval
        if check_interval(insert_file, start_insert, end_insert):
            insert_reader = PdfReader(insert_file)
            insert_pages = insert_reader.pages[start_insert - 1 : end_insert]
            insert_length = len(insert_pages)
        else:
            return

    # the whole insert pdf will be inserted    
    else:
        insert_reader = PdfReader(insert_file)
        insert_pages = insert_reader.pages
        insert_length = len(insert_pages)
    
    # write the pages
    
    # adjust the insert_pos to zero index
    insert_pos -= 1

    # insert pages before
    if relative_pos == 'before':
        writer = PdfWriter()
        for i in range(source_length):
            # if insert pages are to be inserted
            # at the very beginning of source file
            if insert_pos  == 0:
                for j in range(insert_length):
                    writer.add_page(insert_pages[j])
            # insert page has not come yet, so
            # insert source page
            elif i < insert_pos:
                writer.add_page(source_pages[i])
            # insert point has come, add insert_pages
            elif i == insert_pos:
                 for j in range(insert_length):
                    writer.add_page(insert_pages[j])
            # insert pages have already been added, so
            # insert source page
            else:
                writer.add_page(source_pages[i])

    
    # insert pages after
    if relative_pos == 'after':
        writer = PdfWriter()
        for i in range(source_length):
            # if insert pages are to be inserted
            # just after 1st page
            if (insert_pos  == 0) and i == 0:
                # insert the 1st page
                writer.add_page(source_pages[i])
                
                # add the insert pages after 1st page
                for j in range(insert_length):
                    writer.add_page(insert_pages[j])
            # insert page has not come yet, so
            # insert source page
            elif i <= insert_pos:
                writer.add_page(source_pages[i])
            # insert point has just passed, add insert_pages
            elif i == (insert_pos + 1):
                 for j in range(insert_length):
                    writer.add_page(insert_pages[j])
            # insert pages have already been added, so
            # insert source page
            else:
                writer.add_page(source_pages[i])
    
    # write the output file
    filename = Path(source_file).stem
    output_file = f'{output_dir}/{filename}_expanded.pdf'
    with open(output_file, 'wb') as output_file:
        writer.write(output_file)
        

