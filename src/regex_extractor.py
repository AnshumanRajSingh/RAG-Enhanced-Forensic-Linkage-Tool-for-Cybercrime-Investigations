import re
from typing import List, Dict, Any

# High-precision regular expressions for deterministic forensic entities
PATTERNS = {
    "IP_ADDRESS": r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
    "CRYPTO_WALLET_BTC": r"\b(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}\b",
    "CRYPTO_WALLET_ETH": r"\b0x[a-fA-F0-9]{40}\b",
    "PGP_FINGERPRINT": r"\b[0-9a-fA-F]{40}\b"
}

def extract_regex_entities(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Extracts deterministic forensic targets (IPs, Wallets, PGP keys) using Regex.
    """
    extracted_entities = []

    for record in records:
        evidence_id = record.get("evidence_id")
        text = record.get("raw_content", "")
        if not text:
            continue

        for entity_type, pattern in PATTERNS.items():
            for match in re.finditer(pattern, text):
                normalized_type = "CRYPTO_WALLET" if "CRYPTO" in entity_type else entity_type

                extracted_entities.append({
                    "evidence_id": evidence_id,
                    "entity_text": match.group(0),
                    "entity_type": normalized_type,
                    "confidence": 1.0,
                    "extractor": "regex",
                    "start_char": match.start(),
                    "end_char": match.end()
                })

    return extracted_entities