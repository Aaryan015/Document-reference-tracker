import os
import sys
from typing import List, Tuple
import pdfplumber
import re

class DocumentParser:
    def __init__(self, filename: str):
        self.filename = filename
        self.content = self.parse_document()

    def parse_document(self) -> List[Tuple[int, str]]:
        _, file_extension = os.path.splitext(self.filename)
        if file_extension.lower() == '.pdf':
            return self.parse_pdf()
        else:
            return self.parse_text()

    def parse_pdf(self) -> List[Tuple[int, str]]:
        content = []
        with pdfplumber.open(self.filename) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    content.append((page_num, text.strip()))
        return content

    def parse_text(self) -> List[Tuple[int, str]]:
        content = []
        with open(self.filename, 'r', encoding='utf-8') as file:
            for page_num, line in enumerate(file, 1):
                if line.strip():
                    content.append((page_num, line.strip()))
        return content

class AIAnswerGenerator:
    def generate_answer(self, query: str, document: List[Tuple[int, str]]) -> Tuple[str, List[Tuple[int, str]]]:
        # Mock AI answer generation
        answer = f"Based on the document, {query}"
        references = []
        for page, text in document:
            if any(word.lower() in text.lower() for word in query.lower().split()):
                excerpt = self.get_relevant_excerpt(text, query)
                references.append((page, excerpt))
                if len(references) == 5:  # References limited to 5
                    break
        return answer, references

    def get_relevant_excerpt(self, text: str, query: str, context_sentences: int = 2) -> str:
        sentences = re.split(r'(?<=[.!?])\s+', text)
        query_words = query.lower().split()
        
        for i, sentence in enumerate(sentences):
            if any(q_word in sentence.lower() for q_word in query_words):
                start = max(0, i)
                end = min(len(sentences), i + context_sentences + 1)
                return " ".join(sentences[start:end])
        
        return text[:500] + "..."  # Fallback to first 500 characters if no match is found

class ReferenceStore:
    def __init__(self):
        self.references = {}

    def store_reference(self, query: str, references: List[Tuple[int, str]]):
        self.references[query] = references

    def get_reference(self, query: str) -> List[Tuple[int, str]]:
        return self.references.get(query, [])

class CommandLineInterface:
    def __init__(self, document_parser: DocumentParser, ai_generator: AIAnswerGenerator, reference_store: ReferenceStore):
        self.document_parser = document_parser
        self.ai_generator = ai_generator
        self.reference_store = reference_store

    def run(self):
        while True:
            query = input("Enter your query (or 'quit' to exit): ")
            if query.lower() == 'quit':
                break
            
            answer, references = self.ai_generator.generate_answer(query, self.document_parser.content)
            self.reference_store.store_reference(query, references)
            
            print(f"Answer: {answer}")
            print("References:")
            for page, text in references:
                print(f"Page {page}: {text}")

def main(filename: str):
    try:
        if not os.path.isabs(filename):
            filename = os.path.abspath(filename)
        
        # Check if the file exists
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File not found: {filename}")
        
        document_parser = DocumentParser(filename)
        ai_generator = AIAnswerGenerator()
        reference_store = ReferenceStore()
        cli = CommandLineInterface(document_parser, ai_generator, reference_store)
        cli.run()
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python drt.py <filename>")
    else:
        main(sys.argv[1])