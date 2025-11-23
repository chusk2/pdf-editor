from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
from pdf_editor_package.check_interval import check_interval
      
def extract_pages(file: str, start: int, end: int, output_dir='./output'):
        
        # check pages interval and read file
        if check_interval(file, start, end):
            reader = PdfReader(file)
            pages = reader.pages
            pdf_length = len(pages)
        else:
            return

        # print(f'File has {pdf_length} pages.')

        # select pages to extract
        pages_to_extract = pages[start -1 : end]

        # write pages to output file
        writer = PdfWriter()
        for page in pages_to_extract:
            writer.add_page(page)

        filename = Path(file).stem
        with open(f'{output_dir}/{filename}_extracted.pdf', 'wb') as file:
              writer.write(file)