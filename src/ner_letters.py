from transformers import AutoTokenizer, pipeline
from pathlib import Path
import json

MODEL_NAME = "impresso-project/ner-stacked-bert-multilingual"

def load_ner(device="cpu"):
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    ner_pipe = pipeline(
        "generic-ner",
        model=MODEL_NAME,
        tokenizer=tokenizer,
        trust_remote_code=True,
        device=device
    )
    return ner_pipe


def extract_entities(text: str, ner_pipe):
    wanted = {"pers", "loc"}

    results = ner_pipe(text)
    filtered = [ent for ent in results if ent.get("type") in wanted]

    return filtered


def run_ner_on_txt(txt_path: str, output_json: str, device="cpu"):
    ner_pipe = load_ner(device=device)

    text = Path(txt_path).read_text(encoding="utf-8")
    entities = extract_entities(text, ner_pipe)

    Path(output_json).write_text(
        json.dumps(entities, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"[OK] Extracted {len(entities)} entities → {output_json}")
    return entities
