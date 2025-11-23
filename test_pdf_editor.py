
import unittest
import os
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from pdf_editor_package.extract_pages import extract_pages
from pdf_editor_package.rearrange_pages import rearrange_pages
from pdf_editor_package.insert_pages import insert_pages


class TestPdfEditor(unittest.TestCase):

    def setUp(self):
        # Create a dummy PDF for testing
        self.sync_dir = "./sync"
        if not os.path.exists(self.sync_dir):
            os.makedirs(self.sync_dir)

        self.sample_pdf_filename = "sample_numbers.pdf"
        self.sample_pdf_path = os.path.join(self.sync_dir, self.sample_pdf_filename)

        # Create a dummy PDF for insertion
        self.insert_pdf_filename = "sample_letters.pdf"
        self.insert_pdf_path = os.path.join(self.sync_dir, self.insert_pdf_filename)
        # Create an output directory
        self.output_dir = "./output"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    # def tearDown(self):
    #     # Remove the dummy PDFs
    #     if os.path.exists(self.sample_pdf_path):
    #         os.remove(self.sample_pdf_path)
    #     if os.path.exists(self.insert_pdf_path):
    #         os.remove(self.insert_pdf_path)
    #     if os.path.exists(self.sync_dir):
    #         os.rmdir(self.sync_dir)

    #     # Remove the output files
    #     if os.path.exists(self.output_dir):
    #         for filename in os.listdir(self.output_dir):
    #             os.remove(os.path.join(self.output_dir, filename))
    #         os.rmdir(self.output_dir)

    def test_extract_pages(self):
        extract_pages(self.sample_pdf_path, 1, 2, self.output_dir)
        output_path = os.path.join(self.output_dir, f"{self.sample_pdf_filename[:-4]}_extracted.pdf")
        reader = PdfReader(output_path)
        self.assertEqual(len(reader.pages), 2)

    def test_rearrange_pages(self):
        rearrange_pages(self.sample_pdf_path, 1, 1, 'after', 2, self.output_dir)
        output_path = os.path.join(self.output_dir, f"{self.sample_pdf_filename[:-4]}_rearranged.pdf")
        reader = PdfReader(output_path)
        self.assertEqual(len(reader.pages), 3)

    def test_insert_pages(self):
        insert_pages(self.sample_pdf_path, self.insert_pdf_path, 1, 'after', self.output_dir)
        output_path = os.path.join(self.output_dir, f"{self.sample_pdf_filename[:-4]}_expanded.pdf")
        reader = PdfReader(output_path)
        self.assertEqual(len(reader.pages), 4)

if __name__ == '__main__':
    unittest.main()
