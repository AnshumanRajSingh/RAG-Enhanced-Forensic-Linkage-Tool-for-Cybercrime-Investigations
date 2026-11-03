import spacy
from typing import List, Dict, Any

# Load standard English model
nlp = spacy.load("en_core_web_sm")

# Standard NLP entity types to extract
TARGET_LABELS = {"PERSON", "ORG", "GPE", "DATE", "TIME"}

def extract_spacy_entities(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Extracts standard entities (names, organizations, locations, dates) using spaCy.
    """
    extracted_entities = []

    for record in records:
        evidence_id = record.get("evidence_id")
        text = record.get("raw_content", "")
        if not text:
            continue

        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ in TARGET_LABELS:
                extracted_entities.append({
                    "evidence_id": evidence_id,
                    "entity_text": ent.text,
                    "entity_type": ent.label_,
                    "confidence": 1.0,
                    "extractor": "spacy",
                    "start_char": ent.start_char,
                    "end_char": ent.end_char
                })

    return extracted_entities