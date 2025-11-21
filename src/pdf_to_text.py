import pdfplumber
import pytesseract
from pathlib import Path
from pdf2image import convert_from_path

def read_pdf_text(pdf_path: str) -> str:
    """
    Versucht zuerst: Text extrahieren (pdfplumber).
    Wenn fast kein Text vorhanden ist -> OCR (Tesseract).
    """
    pdf_path = Path(pdf_path)

    # 1. Versuch: normaler Text-PDF
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        if len(text.strip()) > 50:
            return text
    except:
        pass

    # 2. Fallback: OCR
    print(f"[OCR] Running Tesseract on {pdf_path.name}...")
    images = convert_from_path(pdf_path)
    ocr_text = ""
    for img in images:
        ocr_text += pytesseract.image_to_string(img, lang="deu+fra+eng")  # viele Briefe multilingual
    return ocr_text

def pdf_to_txt_file(pdf_path: str, txt_output_dir: str = "data/txt"):
    """
    Wandelt PDF in .txt um
    """
    txt_output_dir = Path(txt_output_dir)
    txt_output_dir.mkdir(parents=True, exist_ok=True)

    pdf_path = Path(pdf_path)
    text = read_pdf_text(pdf_path)

    output_path = txt_output_dir / (pdf_path.stem + ".txt")
    output_path.write_text(text, encoding="utf-8")
    print(f"[OK] {pdf_path.name} -> {output_path.name}")

    return output_path
