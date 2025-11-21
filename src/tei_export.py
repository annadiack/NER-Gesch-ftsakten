from pathlib import Path
import xml.etree.ElementTree as ET

def create_tei(entities: list, original_text: str, output_path: str):
    """
    Creates a minimal TEI/XML file with <persName> and <placeName>.
    """
    root = ET.Element("TEI")
    body = ET.SubElement(root, "text")
    body_text = ET.SubElement(body, "body")
    div = ET.SubElement(body_text, "div")

    p = ET.SubElement(div, "p")
    p.text = original_text

    entity_list = ET.SubElement(div, "list")

    for ent in entities:
        tag = "persName" if ent["type"] == "pers" else "placeName"
        item = ET.SubElement(entity_list, tag)
        item.text = ent["surface"]

    tree = ET.ElementTree(root)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)

    print(f"[OK] TEI saved → {output_path}")
