from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
from pdf_editor_package.check_interval import check_interval


# reorder pages
def rearrange_pages(file: str, start: int, end: int, relative_pos: str , new_pos: int, output_dir='./output'):
    
    if relative_pos not in ['after', 'before']:
        print("Invalid relative position value. Use 'before' or 'after'.")
        return
    
    # check pages interval and read file
    if check_interval(file, start, end):
        reader = PdfReader(file)
        pages = reader.pages
        pdf_length = len(pages)
    else:
        return

    if not (1 <= new_pos <= pdf_length):
        print(f'New position {new_pos} is out of range (1-{pdf_length}).')
        return

    # check if new_pos is out of the interval to reorder

    if new_pos in [start, end]:
        print("Rearrangement would not produce any change. PDF file will not be processed")
        return

    if new_pos in range(start, end + 1):
        print('Error: invalid value for the insertion page')
        print(f'Insertion page must be before page {start - 1} or after page {end+1}.')
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
    filename = Path(file).stem
    output_file = f'{output_dir}/{filename}_rearranged.pdf'
    with open(output_file, 'wb') as output_file:
            writer.write(output_file)