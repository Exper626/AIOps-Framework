from pyPDF import PdfReader

def extract_text_from_pdf():

    file_path = "/data/2021.pdf"

    reader = PdfReader(file_path)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text 


text = extract_text_from_pdf()
print(text[:500])
