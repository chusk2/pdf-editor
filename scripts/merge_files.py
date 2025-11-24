import os

from PyPDF2 import PdfReader, PdfWriter

## Merge PDF files

def merge_files(files: list[str], output_dir='./output'):
    """
    Merges multiple PDF files into a single PDF file.

    This feature combines all pages from the input PDF files into one
    output file. The files are merged in the order they are provided in
    the input list.

    Args:
        files (list[str]): A list of paths to the PDF files to merge.
        output_dir (str, optional): The folder where the new, merged PDF
                                    will be saved. Defaults to './output'.
    """

    # create a writer object
    writer = PdfWriter()

    # read the pdf files and add them to writer object
    for file in files:
         reader = PdfReader(file)
        
         # add all pages from reader
         writer.append_pages_from_reader(reader)
    
    # create output folder
    os.makedirs(output_dir, exist_ok = True)
    filename = f'{output_dir}/merged_pdf_files.pdf'

    # save the merged file
    with open(filename, 'wb') as output_file:
        writer.write(output_file)