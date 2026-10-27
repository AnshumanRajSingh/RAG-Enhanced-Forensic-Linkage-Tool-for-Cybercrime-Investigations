import os
import csv
from datetime import datetime, timezone
from typing import List, Dict, Any


def parse_network_telemetry(file_path: str) -> List[Dict[str, Any]]:
    """
    Ankit's Module: Parses NetFlow telemetry CSV files into the standardized evidence schema.
    """
    parsed_records = []
    if not os.path.exists(file_path):
        print(f"[!] Warning: Network telemetry file not found at {file_path}")
        return parsed_records

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=1):
            record = {
                "evidence_id": f"EV-NET-{idx:04d}",
                "source_type": "network",
                "source_format": "netflow_telemetry",
                "timestamp": row.get("timestamp", datetime.now(timezone.utc).isoformat()),
                "raw_content": f"Flow from {row.get('src_ip')}:{row.get('src_port')} to {row.get('dst_ip')}:{row.get('dst_port')} ({row.get('protocol', 'TCP')}, {row.get('bytes_transferred', 0)} bytes)",
                "metadata": {
                    "src_ip": row.get("src_ip"),
                    "dst_ip": row.get("dst_ip"),
                    "src_port": row.get("src_port"),
                    "dst_port": row.get("dst_port"),
                    "protocol": row.get("protocol"),
                    "bytes_transferred": row.get("bytes_transferred")
                }
            }
            parsed_records.append(record)

    return parsed_records