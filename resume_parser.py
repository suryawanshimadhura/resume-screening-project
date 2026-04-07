from pdfminer.high_level import extract_text
import docx2txt
import tempfile

def extract_resume_text(file):

    text = ""

    if file.name.endswith(".pdf"):
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name

        text = extract_text(tmp_path)

    elif file.name.endswith(".docx"):
        text = docx2txt.process(file)

    return text