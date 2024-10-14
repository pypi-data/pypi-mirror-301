# Nepal Constitution 2072 Document Chunker

`nepal-const-doc-chunker` is a Python package for chunking the Nepal Constitution 2072 PDF document. It segments the document into preamble, articles, and schedules, providing structured access to different parts of the constitution.

## Features

- **Document Segmentation**: Splits the constitution into preamble, articles, and schedules.
- **Metadata-Rich Output**: Each segment is represented as a dictionary with section names as keys and the corresponding text as values.
- **Configurable Verbosity**: Option to control the verbosity of the output.

## Installation

Install the package via pip:

```bash
pip install nepal-const-doc-chunker
```
## Usage
Here's an example of how to use the package to chunk the Nepal Constitution 2072:

```python
from nepal_const_doc_chunker import chunk_nepal_constitution

chunks = chunk_nepal_constitution(
    pdf_file_path="path_to_pdf/Nepal_Constitution_2072.pdf", 
    verbose=True)

# Access the structured output
for chunk in chunks:
    print(f"Section: {list(chunk.keys())[0]}")
    print(f"Content: {list(chunk.values())[0]}")

```
### Arguments
**file_path**: Path to the PDF file of the Nepal Constitution 2072.  
**verbose**: Boolean flag to control verbosity (default: False).

### Output
The function returns a list of dictionaries. Each dictionary contains:

A key representing the section title (e.g., 'Preamble', 'Article Part Title', 'Schedule Title').  
A value containing the corresponding text for that section.  

Example output:

```python
[
    {"Preamble": "Text of the preamble..."},
    {"Article Part Title 1": "Text of Article 1..."},
    {"Schedule 1": "Text of Schedule 1..."}
]
```

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests via GitHub.