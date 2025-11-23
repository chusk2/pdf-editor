# streamlit app to extract pages from a PDF file

from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
import os
from pathlib import Path

os.makedirs('./temp', exist_ok = True)


def read_pdf(file, start, end):
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
      
def extract_pages(file, start, end):
        
        # check pages interval and read file
        reader = read_pdf(file, start, end)

        print(f'File has {len(reader.pages)} pages.')
        
        # select pages to extract
        pages_to_extract = reader.pages[start -1 : end]

        # write pages to output file
        writer = PdfWriter()
        for page in pages_to_extract:
            writer.add_page(page)

        filename = Path(file).name
        with open(f'{filename}_extracted.pdf', 'wb') as file:
              writer.write(file)

# extract_pages('sample.pdf', 2,5)

# reorder pages
def reorder_pages(file, start, end, relative_pos , new_pos):
    
    if relative_pos not in ['after', 'before']:
        print("Invalid relative position value. Use 'before' or 'after'.")
        return
    
    # check pages interval and read file
    reader = read_pdf(file, start, end)
    pages = reader.pages
    pdf_length = len(pages)

    if not (1 <= new_pos <= pdf_length):
        print(f'New position {new_pos} is out of range (1-{pdf_length}).')
        return

    # check if new_pos is out of the interval to reorder
    if new_pos in range(start, end + 1):
        print('The insertion page is within the interval of pages to reorder!')
        return
    
    # after check has passed, adjust start and end to zero index
    start, end, new_pos = start - 1, end -1, new_pos - 1

    writer = PdfWriter()

    if relative_pos == 'after':
        for i in range(pdf_length):
            # page index is not within interval
            if i not in range(start, end + 1):
                # insert pages until reaching insert point
                if i <= new_pos:
                    writer.add_page(pages[i])
                # insert point has just passed
                # insert the interval pages
                elif i == new_pos + 1:
                    for j in range(start, end + 1):
                        writer.add_page(pages[j])
                    # after inserting the interval pages
                    # add the new_pos page
                    writer.add_page(pages[i])
                # keep on adding pages after interval pages
                # have been inserted
                else:
                    writer.add_page(pages[i])
    
    if relative_pos == 'before':
        for i in range(pdf_length):
            # page index is not within interval
            if i not in range(start, end + 1):
                # insert pages until reaching insert point
                if i < new_pos:
                    writer.add_page(pages[i])
                # insert point has just passed
                # insert the interval pages
                elif i == new_pos:
                    for j in range(start, end + 1):
                        writer.add_page(pages[j])
                    # after inserting the interval pages
                    # add the new_pos page
                    writer.add_page(pages[i])
                # keep on adding pages after interval pages
                # have been inserted
                else:
                    writer.add_page(pages[i])
            
    # write the output file
    filename = Path(file).name
    with open(f'{filename}_reordered.pdf', 'wb') as file:
            writer.write(file)

#reorder_pages('sample_pages.pdf', 3,5, 'before', 3)
