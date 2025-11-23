from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
from pdf_editor_package.check_interval import check_interval
      
def delete_pages(file, start, end, output_dir='./output'):
        
        # check pages interval and read file
        if check_interval(file, start, end):
            reader = PdfReader(file)
            pages = reader.pages
            pdf_length = len(pages)
        else:
            return

        print(f'File has {pdf_length} pages.')

        # select pages to extract
        pages_to_be_kept = [pages[i] for i in range(pdf_length)
                           if i not in range(start -1 , end) ]

        # write pages to output file
        writer = PdfWriter()
        for page in pages_to_be_kept:
            writer.add_page(page)

        filename = Path(file).name
        with open(f'{output_dir}/{filename}_cleaned.pdf', 'wb') as file:
              writer.write(file)