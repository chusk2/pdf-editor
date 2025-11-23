from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
from pdf_editor_package.check_interval import check_interval
import os
      
def delete_pages(file: str, start: int, end, output_dir='./output'):
        
        # check pages interval and read file
        if check_interval(file, start, end):
            reader = PdfReader(file)
            pages = reader.pages
            pdf_length = len(pages)
        else:
            return

        # select pages to extract
        pages_to_be_kept = [pages[i] for i in range(pdf_length)
                           if i not in range(start -1 , end) ]

        # write pages to output file
        writer = PdfWriter()
        for page in pages_to_be_kept:
            writer.add_page(page)

        # create the output folder
        os.makedirs(output_dir, exist_ok=True)

        filename = Path(file).stem
        with open(f'{output_dir}/{filename}_trimmed.pdf', 'wb') as file:
              writer.write(file)