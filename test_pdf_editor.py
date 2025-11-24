
import unittest
import os
from pathlib import Path
from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import sys

# Ensure the package is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdf_editor_package.extract_pages import extract_pages
from pdf_editor_package.rearrange_pages import rearrange_pages
from pdf_editor_package.insert_pages import insert_pages
from pdf_editor_package.remove_pages import delete_pages
from pdf_editor_package.check_interval import check_interval


def create_dummy_pdf(filename, content):
    """Helper function to create a PDF with given content on each page."""
    c = canvas.Canvas(str(filename), pagesize=letter)
    for item in content:
        c.drawString(100, 750, str(item))
        c.showPage()
    c.save()


class TestPdfEditor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up dummy files and directories for all tests."""
        print("Setting up test environment...")
        cls.sync_dir = Path("./sync")
        cls.output_dir = Path("./output")
        cls.sync_dir.mkdir(exist_ok=True)
        cls.output_dir.mkdir(exist_ok=True)

        cls.sample_pdf_filename = "sample_numbers.pdf"
        cls.sample_pdf_path = cls.sync_dir / cls.sample_pdf_filename
        create_dummy_pdf(cls.sample_pdf_path, range(1, 11))

        cls.insert_pdf_filename = "sample_letters.pdf"
        cls.insert_pdf_path = cls.sync_dir / cls.insert_pdf_filename
        create_dummy_pdf(cls.insert_pdf_path, [chr(i) for i in range(65, 75)])  # A-J
        print("Test environment set up.")

    @classmethod
    def tearDownClass(cls):
        """Clean up created files and directories after all tests."""
        print("\nTearing down test environment...")
        for f in cls.sync_dir.glob("*.pdf"):
            f.unlink()
        if not any(cls.sync_dir.iterdir()):
            cls.sync_dir.rmdir()

        for f in cls.output_dir.glob("*.pdf"):
            try:
                f.unlink()
            except OSError as e:
                print(f"Error removing file {f}: {e}")

        if cls.output_dir.exists() and not any(cls.output_dir.iterdir()):
            cls.output_dir.rmdir()
        print("Test environment torn down.")

    def test_check_interval(self):
        test_name = "test_check_interval"
        print(f"\n--- Running test: {test_name} ---")

        with self.subTest("Valid interval"):
            print(f"Subtest: Valid interval, Input: ('{self.sample_pdf_path}', 1, 10)")
            self.assertTrue(check_interval(self.sample_pdf_path, 1, 10))

        with self.subTest("Start larger than end"):
            print(f"Subtest: Start larger than end, Input: ('{self.sample_pdf_path}', 5, 4)")
            self.assertIsNone(check_interval(self.sample_pdf_path, 5, 4))

        with self.subTest("End out of bounds"):
            print(f"Subtest: End out of bounds, Input: ('{self.sample_pdf_path}', 1, 11)")
            self.assertIsNone(check_interval(self.sample_pdf_path, 1, 11))

        with self.subTest("Start out of bounds"):
            print(f"Subtest: Start out of bounds, Input: ('{self.sample_pdf_path}', 11, 12)")
            self.assertIsNone(check_interval(self.sample_pdf_path, 11, 12))
            
        with self.subTest("Single page interval at boundary"):
            print(f"Subtest: Single page interval at boundary, Input: ('{self.sample_pdf_path}', 10, 10)")
            self.assertTrue(check_interval(self.sample_pdf_path, 10, 10))

        print(f"--- Test {test_name} has passed! OK ---")

    def test_extract_pages(self):
        test_name = "test_extract_pages"
        print(f"\n--- Running test: {test_name} ---")

        # Case 1: Standard extraction
        with self.subTest("Standard extraction"):
            start, end = 3, 5
            print(f"Subtest: Standard extraction, Input: ('{self.sample_pdf_path}', {start}, {end})")
            extract_pages(self.sample_pdf_path, start, end, str(self.output_dir))
            output_path = self.output_dir / f"{self.sample_pdf_path.stem}_extracted.pdf"
            reader = PdfReader(output_path)
            self.assertEqual(len(reader.pages), 3)
            self.assertIn("3", reader.pages[0].extract_text())
            self.assertIn("5", reader.pages[2].extract_text())

        # Case 2: Extract single page
        with self.subTest("Extract single page"):
            start, end = 7, 7
            print(f"Subtest: Extract single page, Input: ('{self.sample_pdf_path}', {start}, {end})")
            extract_pages(self.sample_pdf_path, start, end, str(self.output_dir))
            output_path = self.output_dir / f"{self.sample_pdf_path.stem}_extracted.pdf"
            reader = PdfReader(output_path)
            self.assertEqual(len(reader.pages), 1)
            self.assertIn("7", reader.pages[0].extract_text())

        # Case 3: Extract all pages
        with self.subTest("Extract all pages"):
            start, end = 1, 10
            print(f"Subtest: Extract all pages, Input: ('{self.sample_pdf_path}', {start}, {end})")
            extract_pages(self.sample_pdf_path, start, end, str(self.output_dir))
            output_path = self.output_dir / f"{self.sample_pdf_path.stem}_extracted.pdf"
            reader = PdfReader(output_path)
            self.assertEqual(len(reader.pages), 10)
            self.assertIn("1", reader.pages[0].extract_text())
            self.assertIn("10", reader.pages[9].extract_text())

        print(f"--- Test {test_name} has passed! OK ---")

    def test_rearrange_pages(self):
        test_name = "test_rearrange_pages"
        print(f"\n--- Running test: {test_name} ---")

        with self.subTest("Move block to middle"):
            start, end, r_pos, n_pos = 1, 2, 'after', 5
            print(f"Subtest: Move block to middle, Input: (..., {start}, {end}, '{r_pos}', {n_pos})")
            rearrange_pages(self.sample_pdf_path, start, end, r_pos, n_pos)
            output_path = self.output_dir / f"{self.sample_pdf_path.stem}_rearranged.pdf"
            reader = PdfReader(output_path)
            self.assertEqual(len(reader.pages), 10)
            self.assertIn("3", reader.pages[0].extract_text())
            self.assertIn("5", reader.pages[2].extract_text())
            self.assertIn("1", reader.pages[3].extract_text())
            self.assertIn("2", reader.pages[4].extract_text())
            self.assertIn("6", reader.pages[5].extract_text())

        with self.subTest("Move single page to end"):
            start, end, r_pos, n_pos = 1, 1, 'after', 10
            print(f"Subtest: Move single page to end, Input: (..., {start}, {end}, '{r_pos}', {n_pos})")
            rearrange_pages(self.sample_pdf_path, start, end, r_pos, n_pos)
            output_path = self.output_dir / f"{self.sample_pdf_path.stem}_rearranged.pdf"
            reader = PdfReader(output_path)
            self.assertEqual(len(reader.pages), 10)
            self.assertIn("10", reader.pages[8].extract_text())
            self.assertIn("1", reader.pages[9].extract_text())
            
        with self.subTest("Move block to beginning"):
            start, end, r_pos, n_pos = 9, 10, 'before', 2
            print(f"Subtest: Move block to beginning, Input: (..., {start}, {end}, '{r_pos}', {n_pos})")
            rearrange_pages(self.sample_pdf_path, start, end, r_pos, n_pos)
            output_path = self.output_dir / f"{self.sample_pdf_path.stem}_rearranged.pdf"
            reader = PdfReader(output_path)
            self.assertEqual(len(reader.pages), 10)
            self.assertIn("1", reader.pages[0].extract_text())
            self.assertIn("9", reader.pages[1].extract_text())
            self.assertIn("10", reader.pages[2].extract_text())
            self.assertIn("2", reader.pages[3].extract_text())

        with self.subTest("Invalid new_pos inside interval"):
            start, end, r_pos, n_pos = 3, 6, 'after', 4
            print(f"Subtest: Invalid new_pos, Input: (..., {start}, {end}, '{r_pos}', {n_pos})")
            # This should print an error and not create a file, we can't easily check that without mocking stdout
            rearrange_pages(self.sample_pdf_path, start, end, r_pos, n_pos)
            output_path = self.output_dir / f"{self.sample_pdf_path.stem}_rearranged.pdf"
            self.assertFalse(output_path.exists()) # Should not create a file

        print(f"--- Test {test_name} has passed! OK ---")


    def test_insert_pages(self):
        test_name = "test_insert_pages"
        print(f"\n--- Running test: {test_name} ---")

        with self.subTest("Insert at beginning"):
            page, r_pos = 1, 'before'
            print(f"Subtest: Insert at beginning, Input: (..., {page}, '{r_pos}')")
            insert_pages(self.sample_pdf_path, self.insert_pdf_path, page, r_pos)
            output_path = self.output_dir / f"{self.sample_pdf_path.stem}_expanded.pdf"
            reader = PdfReader(output_path)
            self.assertEqual(len(reader.pages), 20)
            self.assertIn("A", reader.pages[0].extract_text())
            self.assertIn("J", reader.pages[9].extract_text())
            self.assertIn("1", reader.pages[10].extract_text())

        with self.subTest("Insert at end"):
            page, r_pos = 10, 'after'
            print(f"Subtest: Insert at end, Input: (..., {page}, '{r_pos}')")
            insert_pages(self.sample_pdf_path, self.insert_pdf_path, page, r_pos)
            output_path = self.output_dir / f"{self.sample_pdf_path.stem}_expanded.pdf"
            reader = PdfReader(output_path)
            self.assertEqual(len(reader.pages), 20)
            self.assertIn("10", reader.pages[9].extract_text())
            self.assertIn("A", reader.pages[10].extract_text())
            self.assertIn("J", reader.pages[19].extract_text())

        with self.subTest("Insert in the middle"):
            page, r_pos = 5, 'after'
            print(f"Subtest: Insert in the middle, Input: (..., {page}, '{r_pos}')")
            insert_pages(self.sample_pdf_path, self.insert_pdf_path, page, r_pos)
            output_path = self.output_dir / f"{self.sample_pdf_path.stem}_expanded.pdf"
            reader = PdfReader(output_path)
            self.assertEqual(len(reader.pages), 20)
            self.assertIn("5", reader.pages[4].extract_text())
            self.assertIn("A", reader.pages[5].extract_text())
            self.assertIn("6", reader.pages[15].extract_text())

        print(f"--- Test {test_name} has passed! OK ---")


    def test_delete_pages(self):
        test_name = "test_delete_pages"
        print(f"\n--- Running test: {test_name} ---")

        with self.subTest("Delete from beginning"):
            start, end = 1, 3
            print(f"Subtest: Delete from beginning, Input: (..., {start}, {end})")
            delete_pages(self.sample_pdf_path, start, end)
            output_path = self.output_dir / f"{self.sample_pdf_path.stem}_trimmed.pdf"
            reader = PdfReader(output_path)
            self.assertEqual(len(reader.pages), 7)
            self.assertIn("4", reader.pages[0].extract_text())

        with self.subTest("Delete from end"):
            start, end = 8, 10
            print(f"Subtest: Delete from end, Input: (..., {start}, {end})")
            delete_pages(self.sample_pdf_path, start, end)
            output_path = self.output_dir / f"{self.sample_pdf_path.stem}_trimmed.pdf"
            reader = PdfReader(output_path)
            self.assertEqual(len(reader.pages), 7)
            self.assertIn("7", reader.pages[6].extract_text())

        with self.subTest("Delete single page"):
            start, end = 5, 5
            print(f"Subtest: Delete single page, Input: (..., {start}, {end})")
            delete_pages(self.sample_pdf_path, start, end)
            output_path = self.output_dir / f"{self.sample_pdf_path.stem}_trimmed.pdf"
            reader = PdfReader(output_path)
            self.assertEqual(len(reader.pages), 9)
            self.assertIn("4", reader.pages[3].extract_text())
            self.assertIn("6", reader.pages[4].extract_text())
            
        with self.subTest("Delete all pages"):
            start, end = 1, 10
            print(f"Subtest: Delete all pages, Input: (..., {start}, {end})")
            delete_pages(self.sample_pdf_path, start, end)
            output_path = self.output_dir / f"{self.sample_pdf_path.stem}_trimmed.pdf"
            reader = PdfReader(output_path)
            self.assertEqual(len(reader.pages), 0)

        print(f"--- Test {test_name} has passed! OK ---")


if __name__ == '__main__':
    # We manage the test execution to provide a custom summary
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestPdfEditor)
    runner = unittest.TextTestRunner(verbosity=0) # We handle our own verbosity
    result = runner.run(suite)
    
    passed = result.testsRun - len(result.failures) - len(result.errors)
    failed = len(result.failures) + len(result.errors)
    
    print("\n--- Test Summary ---")
    print(f"Total tests run: {result.testsRun}")
    print(f"Passed tests: {passed}")
    print(f"Failed tests: {failed}")
    print("--------------------")
