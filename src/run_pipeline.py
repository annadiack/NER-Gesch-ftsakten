from pathlib import Path
from pdf_to_text import pdf_to_txt_file
from ner_letters import run_ner_on_txt
from tei_export import create_tei
from utils import list_pdfs

def main():
    pdfs = list_pdfs()

    for pdf in pdfs:
        print(f"\n=== Processing {pdf.name} ===")

        # 1. PDF → TXT
        txt_path = pdf_to_txt_file(pdf)

        # 2. TXT → NER
        json_output = Path("data/processed") / (pdf.stem + "_entities.json")
        entities = run_ner_on_txt(txt_path, json_output)

        # 3. TXT + NER → TEI/XML
        tei_output = Path("data/tei") / (pdf.stem + ".xml")
        original_text = Path(txt_path).read_text(encoding="utf-8")
        create_tei(entities, original_text, tei_output)


if __name__ == "__main__":
    main()
