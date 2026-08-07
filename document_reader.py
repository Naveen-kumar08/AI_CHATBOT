import os
import pandas as pd
from pypdf import PdfReader
from docx import Document


# =====================================
# Read PDF
# =====================================

def read_pdf(file_path):

    text = ""

    reader = PdfReader(file_path)

    for page in reader.pages:
        text += page.extract_text()

    return text



# =====================================
# Read DOCX
# =====================================

def read_docx(file_path):

    doc = Document(file_path)

    text = ""

    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

    return text



# =====================================
# Read TXT
# =====================================

def read_txt(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()



# =====================================
# Read Excel
# =====================================

def read_excel(file_path):

    df = pd.read_excel(file_path)

    return df.to_string()



# =====================================
# Main File Reader
# =====================================

def read_document(file_path):

    extension = os.path.splitext(file_path)[1].lower()


    if extension == ".pdf":

        return read_pdf(file_path)


    elif extension == ".docx":

        return read_docx(file_path)


    elif extension == ".txt":

        return read_txt(file_path)


    elif extension == ".xlsx":

        return read_excel(file_path)


    else:

        return "Unsupported file format"