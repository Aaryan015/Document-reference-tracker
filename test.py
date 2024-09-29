import unittest
import tempfile
import os
from drt import DocumentParser, AIAnswerGenerator, ReferenceStore

class TestDocumentReferenceTracker(unittest.TestCase):
    def setUp(self):
        # Create a temporary PDF file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, 'test_document.pdf')
        self.create_test_pdf()
        
        self.document_parser = DocumentParser(self.test_file)
        self.ai_generator = AIAnswerGenerator()
        self.reference_store = ReferenceStore()

    def create_test_pdf(self):
        # You'll need to install reportlab: pip install reportlab
        from reportlab.pdfgen import canvas
        
        c = canvas.Canvas(self.test_file)
        c.drawString(100, 750, "Page 1 content")
        c.showPage()
        c.drawString(100, 750, "Page 2 content")
        c.showPage()
        c.drawString(100, 750, "Page 3 content")
        c.save()

    def test_document_parser(self):
        self.assertEqual(len(self.document_parser.content), 3)
        self.assertEqual(self.document_parser.content[0][0], 1)
        self.assertTrue("Page 1 content" in self.document_parser.content[0][1])

    def test_ai_answer_generator(self):
        query = "content"
        answer, references = self.ai_generator.generate_answer(query, self.document_parser.content)
        
        self.assertTrue(query in answer)
        self.assertTrue(len(references) > 0)
        self.assertLessEqual(len(references), len(self.document_parser.content))
        
        for page, excerpt in references:
            self.assertIsInstance(page, int)
            self.assertIsInstance(excerpt, str)
            self.assertTrue(query.lower() in excerpt.lower())

    def test_reference_store(self):
        query = "test query"
        references = [(1, "test reference")]
        self.reference_store.store_reference(query, references)
        self.assertEqual(self.reference_store.get_reference(query), references)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)

if __name__ == "__main__":
    unittest.main()