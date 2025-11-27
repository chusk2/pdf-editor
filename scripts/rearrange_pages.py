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
    pdf_length = len(reader.pages)
    source_pages = reader.pages

    # Isolate the block of pages to be moved
    moving_block = source_pages[start - 1 : end]

    # Create a list of pages that are NOT being moved
    stationary_pages = [p for i, p in enumerate(source_pages) if i not in range(start - 1, end)]

    # Calculate the correct 0-indexed insertion point in the modified list
    pages_to_discount = len([p for p in range(start - 1, end) if p < new_pos - 1])
    final_pos = (new_pos - 1) - pages_to_discount
    if relative_pos == 'after':
        final_pos += 1

    # Re-insert the block at the new position
    stationary_pages[final_pos:final_pos] = moving_block

    # Add the final ordered pages to a new writer
    writer = PdfWriter()
    for page in stationary_pages:
        writer.add_page(page)
    ## write the output file

    # prepare output file name
    filename = Path(file.name)
    output_filename = f'{filename.stem}_rearranged.pdf'

    # create a memory buffer to store output pdf
    output_buffer = io.BytesIO()
    writer.write(output_buffer)

    return output_buffer, output_filename