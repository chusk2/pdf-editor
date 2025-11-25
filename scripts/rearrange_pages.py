import io
from pathlib import Path

from PyPDF2 import PdfReader, PdfWriter


def rearrange_pages(file, start: int, end: int, relative_pos: str , new_pos: int):
    """
    Changes the order of pages in a PDF file.

    This feature lets you select a single page or a range of pages and move
    them to a new position in the document.

    For example, you can take pages 8-10 and move them 'before' page 2,
    making them the new pages 2, 3, and 4.

    Args:
        file (str): The path to the PDF file you want to reorganize.
        start (int): The first page number of the block you want to move.
        end (int): The last page number of the block you want to move.
                   (Use the same number as `start` to move a single page).
        relative_pos (str): Determines where to place the block. Use 'before'
                            or 'after' the `new_pos`.
        new_pos (int): The page number that will be the reference point for
                       the move.
    """
    reader = PdfReader(file)
    pages = reader.pages
    pdf_length = len(pages)

    # after check has passed, adjust start and end to be zero indexing compliant
    start, end, new_pos = start - 1, end -1, new_pos - 1

    writer = PdfWriter()

    # moving block after the new position
    if relative_pos == 'after':
        for i in range(pdf_length):

            # page index is not within moving pages interval
            if not i in range(start, end + 1):

                # if insertion page has not been reached
                # insert regular page
                if i != new_pos:
                    writer.add_page(pages[i])

                # insertion page has just been reached
                # insert the new pages block after it
                elif i == new_pos:
                    writer.add_page(pages[i])

                    # after inserting the new_pos page
                    # add the moving pages block
                    for j in range(start, end + 1):
                        writer.add_page(pages[j])
    
    # moving block before the new position
    if relative_pos == 'before':
        for i in range(pdf_length):
            # page index is not within moving pages interval
            if i not in range(start, end + 1):

                # if insertion page has not been reached
                # insert regular page
                if i != new_pos:
                    writer.add_page(pages[i])

                # insert point has just been reached
                # insert the new pages block before it
                elif i == new_pos:
                    for j in range(start, end + 1):
                        writer.add_page(pages[j])

                    # after inserting the moving pages block
                    # add the new_pos page
                    writer.add_page(pages[i])

            
    ## write the output file

    # prepare output file name
    filename = Path(file)
    output_filename = f'{filename.stem}_rearranged.pdf'

    # create a memory buffer to store output pdf
    output_buffer = io.BytesIO()
    writer.write(output_buffer)

    return output_buffer, output_filename