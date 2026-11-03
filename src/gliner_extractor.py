from gliner import GLiNER
from typing import List, Dict, Any

# Load lightweight zero-shot model
model = GLiNER.from_pretrained("urchade/gliner_small-v2.1")

# Target custom forensic labels for zero-shot recognition
FORENSIC_LABELS = ["threat_actor", "handle", "software_alias", "malware", "crypto_wallet"]

def extract_gliner_entities(records: List[Dict[str, Any]], threshold: float = 0.4) -> List[Dict[str, Any]]:
    """
    Extracts custom zero-shot cybersecurity entities using GLiNER.
    """
    extracted_entities = []

    for record in records:
        evidence_id = record.get("evidence_id")
        text = record.get("raw_content", "")
        if not text:
            continue

        entities = model.predict_entities(text, FORENSIC_LABELS, threshold=threshold)
        for ent in entities:
            extracted_entities.append({
                "evidence_id": evidence_id,
                "entity_text": ent["text"],
                "entity_type": ent["label"].upper(),
                "confidence": round(float(ent["score"]), 3),
                "extractor": "gliner",
                "start_char": ent["start"],
                "end_char": ent["end"]
            })

    return extracted_entities