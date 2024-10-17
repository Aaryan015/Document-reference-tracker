## About: 

### Document reference tracker
![refresh page](https://github.com/Aaryan015/Track-reference/blob/main/Architecture%20diagram.png?raw=true)

- A simple document reference tracker that links AI-generated answers to specific locations in a source document.
-----
### Steps:
- Parses an uploaded PDF or text document, extracting text with page numbers.
- Generates a mock AI answer with references to the document.
- Stores and retrieves references (page number and text excerpt).
- Implements a basic command-line interface to display referenced text.
- Includes error handling and basic unit tests.
-----
## Setup: 🛠️
1. Clone this repository:
```sh
git clone https://github.com/Aaryan015/Track-reference.git
```
2. Install the necessary libraries:
```sh
pip install pdfplumber reportlab
```

## How to run: 🏃
🚨 NOTE: Place the text or PDF files which you want to query from, in the same project directory.

### 1. Tracker app:
a. Text files:
```sh
python drt.py YOUR_DOCUMENT_NAME.txt
```

b. PDF files:
```sh
python drt.py YOUR_DOCUMENT_NAME.pdf
```

### 2. Tests:
```sh
python -m unittest drt.py
```
