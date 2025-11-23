
import unittest
import os
from PyPDF2 import PdfWriter, PdfReader
from pdf_editor_package.extract_pages import extract_pages
from pdf_editor_package.reorder_pages import reorder_pages
from pdf_editor_package.insert_pages import insert_pages
from pdf_editor_package.check_interval import check_interval


class TestPdfEditor(unittest.TestCase):

    def setUp(self):
        # Create a dummy PDF for testing
        self.sample_pdf_path = "sample_pages.pdf"
        writer = PdfWriter()
        for i in range(3):
            writer.add_blank_page(width=612, height=792)
        with open(self.sample_pdf_path, "wb") as f:
            writer.write(f)

        # Create a dummy PDF for insertion
        self.insert_pdf_path = "dummy_insert.pdf"
        writer = PdfWriter()
        writer.add_blank_page(width=612, height=792)
        with open(self.insert_pdf_path, "wb") as f:
            writer.write(f)

        # Create an output directory
        self.output_dir = "output"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def tearDown(self):
        # Remove the dummy PDFs
        os.remove(self.sample_pdf_path)
        os.remove(self.insert_pdf_path)

        # Remove the output files
        for filename in os.listdir(self.output_dir):
            os.remove(os.path.join(self.output_dir, filename))
        os.rmdir(self.output_dir)

    def test_extract_pages(self):
        extract_pages(self.sample_pdf_path, 1, 2)
        output_path = os.path.join(self.output_dir, "sample_pages.pdf_extracted.pdf")
        self.assertTrue(os.path.exists(output_path))
        reader = PdfReader(output_path)
        if not self.assertEqual(len(reader.pages), 2):
            print('Test failed: test_extract_pages')
            print("Code tested: extract_pages(self.sample_pdf_path, 1, 2)")

    def test_reorder_pages(self):
        reorder_pages(self.sample_pdf_path, 1, 1, 'after', 2)
        output_path = os.path.join(self.output_dir, "sample_pages.pdf_reordered.pdf")
        self.assertTrue(os.path.exists(output_path))
        reader = PdfReader(output_path)
        if not self.assertEqual(len(reader.pages), 3):
            print('Test failed: test_reorder_pages')
            print("Code tested: reorder_pages(self.sample_pdf_path, 1, 1, 'after', 2)")

    def test_insert_pages(self):
        insert_pages(self.sample_pdf_path, self.insert_pdf_path, 1, 'after')
        output_path = os.path.join(self.output_dir, "sample_pages.pdf_expanded.pdf")
        self.assertTrue(os.path.exists(output_path))
        reader = PdfReader(output_path)
        if not self.assertEqual(len(reader.pages), 4):
            print('Test failed: test_insert_pages')
            print("Code tested: insert_pages(self.sample_pdf_path, self.insert_pdf_path, 1, 'after')")

if __name__ == '__main__':
    unittest.main()
