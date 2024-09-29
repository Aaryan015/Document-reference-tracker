# Reference tracker
![refresh page](https://github.com/Aaryan015/Track-reference/blob/main/Architecture%20diagram.png?raw=true)

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
NOTE: Place the text or PDF files which you want to query from, in the same project directory.

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
