from pathlib import Path

def list_pdfs(pdf_dir="data/pdf"):
    """
    Returns a list of all PDF files in data/pdf.
    """
    pdf_dir = Path(pdf_dir)
    pdf_dir.mkdir(parents=True, exist_ok=True)
    return sorted(pdf_dir.glob("*.pdf"))
