import os
from langchain.llms import OpenAI
from PyPDF2 import PdfReader
from docx import Document

# Functions to read documents
def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def read_docx(file_path):
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def read_txt(file_path):
    with open(file_path, "r") as file:
        return file.read()

def load_document(file_path):
    _, ext = os.path.splitext(file_path)
    if ext == ".pdf":
        return read_pdf(file_path)
    elif ext == ".docx":
        return read_docx(file_path)
    elif ext == ".txt":
        return read_txt(file_path)
    else:
        raise ValueError("Unsupported file format")

# Function to summarize text
def summarize_text(llm, text, max_words=150):
    prompt = (
        f"Please summarize the following text in {max_words} words:\n\n"
        f"{text[:3000]}"  # Limit to 3000 characters to avoid truncation
    )
    return llm(prompt)

# Initialize OpenAI LLM
llm = OpenAI(model="text-davinci-003", temperature=0.5)

# Main script
if __name__ == "__main__":
    # Input file path
    file_path = input("Enter the file path (PDF, DOCX, or TXT): ")

    try:
        # Load and summarize the document
        document_text = load_document(file_path)
        summary = summarize_text(llm, document_text, max_words=150)
        print("\nSummary:\n", summary)
    except Exception as e:
        print("Error:", str(e))