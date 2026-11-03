import json
import os
from typing import List, Dict, Any

from spacy_extractor import extract_spacy_entities
from gliner_extractor import extract_gliner_entities
from regex_extractor import extract_regex_entities

EVIDENCE_FILE = "data/parsed_evidence.json"
OUTPUT_FILE = "data/extracted_entities.json"

def deduplicate_entities(entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Deduplicates overlapping entities prioritized by precision: Regex (1) > GLiNER (2) > spaCy (3).
    """
    seen = set()
    unique_entities = []
    priority_map = {"regex": 1, "gliner": 2, "spacy": 3}

    sorted_entities = sorted(entities, key=lambda x: priority_map.get(x["extractor"], 99))

    for ent in sorted_entities:
        key = (ent["evidence_id"], ent["entity_text"].lower(), ent["entity_type"])
        if key not in seen:
            seen.add(key)
            unique_entities.append(ent)

    return unique_entities

def run_ner_pipeline():
    if not os.path.exists(EVIDENCE_FILE):
        print(f"[!] Error: {EVIDENCE_FILE} not found. Ensure Week 2 output exists.")
        return

    with open(EVIDENCE_FILE, "r", encoding="utf-8") as f:
        records = json.load(f)

    print(f"[+] Loaded {len(records)} evidence records from {EVIDENCE_FILE}")

    spacy_ents = extract_spacy_entities(records)
    print(f"[+] spaCy Extractor: Found {len(spacy_ents)} entities.")

    gliner_ents = extract_gliner_entities(records)
    print(f"[+] GLiNER Extractor: Found {len(gliner_ents)} entities.")

    regex_ents = extract_regex_entities(records)
    print(f"[+] Regex Extractor: Found {len(regex_ents)} entities.")

    all_ents = spacy_ents + gliner_ents + regex_ents
    final_entities = deduplicate_entities(all_ents)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_entities, f, indent=2)

    print(f"[PASS] Multi-Model NER Pipeline complete. Extracted {len(final_entities)} unique entities.")
    print(f"[PASS] Saved entity dataset to: {os.path.abspath(OUTPUT_FILE)}")

if __name__ == "__main__":
    run_ner_pipeline()