import json
import os
from typing import Dict, Any, Tuple
import networkx as nx

ENTITIES_FILE = "data/extracted_entities.json"
EVIDENCE_FILE = "data/parsed_evidence.json"

def build_knowledge_graph() -> nx.Graph:
    """
    Builds an undirected NetworkX graph from extracted forensic entities and raw evidence metadata.
    Nodes: Evidence Records & Forensic Entities
    Edges: MENTIONED_IN (Entity -> Evidence) & CO_OCCURRED (Entity <-> Entity)
    """
    G = nx.Graph()

    if not os.path.exists(ENTITIES_FILE) or not os.path.exists(EVIDENCE_FILE):
        print(f"[!] Error: Missing input dataset files ({ENTITIES_FILE} or {EVIDENCE_FILE}).")
        return G

    with open(EVIDENCE_FILE, "r", encoding="utf-8") as f:
        evidence_records = json.load(f)

    with open(ENTITIES_FILE, "r", encoding="utf-8") as f:
        entities = json.load(f)

    # 1. Add Evidence Nodes
    for ev in evidence_records:
        ev_id = ev.get("evidence_id")
        G.add_node(
            ev_id,
            node_type="Evidence",
            source_type=ev.get("source_type", "unknown"),
            timestamp=ev.get("timestamp", "")
        )

    # 2. Add Entity Nodes & Connect to Evidence Nodes
    evidence_entity_map = {}
    for ent in entities:
        ev_id = ent.get("evidence_id")
        entity_text = ent.get("entity_text")
        entity_type = ent.get("entity_type")

        # Use entity_text as unique node identifier
        G.add_node(
            entity_text,
            node_type="Entity",
            entity_type=entity_type,
            extractor=ent.get("extractor"),
            confidence=ent.get("confidence", 1.0)
        )

        # Edge: Entity -> Evidence Record
        G.add_edge(entity_text, ev_id, relation="MENTIONED_IN")

        # Track co-occurrence by evidence ID
        if ev_id not in evidence_entity_map:
            evidence_entity_map[ev_id] = []
        evidence_entity_map[ev_id].append(entity_text)

    # 3. Add Co-occurrence Edges between Entities in the same Evidence Record
    for ev_id, ent_list in evidence_entity_map.items():
        unique_ents = list(set(ent_list))
        for i in range(len(unique_ents)):
            for j in range(i + 1, len(unique_ents)):
                e1, e2 = unique_ents[i], unique_ents[j]
                if G.has_edge(e1, e2):
                    G[e1][e2]["weight"] += 1
                else:
                    G.add_edge(e1, e2, relation="CO_OCCURRED_WITH", weight=1)

    print(f"[+] Knowledge Graph Built Successfully!")
    print(f"    - Total Nodes: {G.number_of_nodes()}")
    print(f"    - Total Edges: {G.number_of_edges()}")

    return G

if __name__ == "__main__":
    build_knowledge_graph()