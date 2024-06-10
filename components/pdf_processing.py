from PyPDF2 import PdfReader
from fpdf import FPDF

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def create_pdf(raw_text):
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size = 12)
    pdf.multi_cell(w=0,h=10,text=raw_text)
    newpdf=pdf.output(dest="S")
    return newpdf