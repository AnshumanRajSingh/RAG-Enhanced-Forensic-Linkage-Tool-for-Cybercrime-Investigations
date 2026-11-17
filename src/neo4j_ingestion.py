import json
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

with open("data/knowledge_graph.json", "r", encoding="utf-8") as f:
    data = json.load(f)

nodes = data.get("nodes", [])
edges = data.get("links") or data.get("edges", [])

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

    # 1. Upload all 34 nodes
    for node in nodes:
        node_id = str(node.get("id"))
        node_type = str(node.get("type", "")).upper()

        if "EVIDENCE" in node_type or node_id.startswith("EV-"):
            driver.execute_query(
                """
                MERGE (e:Evidence {evidence_id: $id})
                SET e.source_type = $source_type, e.timestamp = $timestamp
                """,
                id=node_id,
                source_type=node.get("source_type", "forensic_log"),
                timestamp=str(node.get("timestamp", "unknown")),
            )
        else:
            driver.execute_query(
                """
                MERGE (n:Entity {name: $name})
                SET n.category = $category
                """,
                name=node_id,
                category=str(node.get("category", node.get("entity_type", "ENTITY"))),
            )

    print(f"[PASS] Uploaded {len(nodes)} nodes to Neo4j!")

    # 2. Upload all 75 connections (edges)
    for edge in edges:
        src = str(edge.get("source"))
        tgt = str(edge.get("target"))

        if src.startswith("EV-") and not tgt.startswith("EV-"):
            src, tgt = tgt, src

        if tgt.startswith("EV-") and not src.startswith("EV-"):
            driver.execute_query(
                """
                MATCH (a:Entity {name: $src}), (b:Evidence {evidence_id: $tgt})
                MERGE (a)-[:APPEARS_IN]->(b)
                """,
                src=src,
                tgt=tgt,
            )
        else:
            driver.execute_query(
                """
                MATCH (a), (b)
                WHERE coalesce(a.name, a.evidence_id) = $src
                  AND coalesce(b.name, b.evidence_id) = $tgt
                MERGE (a)-[:CO_OCCURS_WITH]->(b)
                """,
                src=src,
                tgt=tgt,
            )

    print(f"[PASS] Uploaded {len(edges)} relationships to Neo4j!")