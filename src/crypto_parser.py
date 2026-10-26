import os
import csv
from datetime import datetime, timezone
from typing import List, Dict, Any


def parse_crypto_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Ankit's Module: Parses crypto transaction ledger CSV files into the standardized evidence schema.
    """
    parsed_records = []
    if not os.path.exists(file_path):
        print(f"[!] Warning: Crypto transactions file not found at {file_path}")
        return parsed_records

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=1):
            record = {
                "evidence_id": f"EV-CRYPTO-{idx:04d}",
                "source_type": "crypto",
                "source_format": "ledger_csv",
                "timestamp": row.get("timestamp", datetime.now(timezone.utc).isoformat()),
                "raw_content": f"TxHash: {row.get('tx_hash')} | From: {row.get('sender_wallet')} To: {row.get('receiver_wallet')} | Amount: {row.get('amount')} {row.get('asset', 'BTC')}",
                "metadata": {
                    "tx_hash": row.get("tx_hash"),
                    "sender_wallet": row.get("sender_wallet"),
                    "receiver_wallet": row.get("receiver_wallet"),
                    "amount": row.get("amount"),
                    "asset": row.get("asset")
                }
            }
            parsed_records.append(record)

    return parsed_records