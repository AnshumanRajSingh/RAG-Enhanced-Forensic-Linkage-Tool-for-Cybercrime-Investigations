import os
import time
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    # 1. Test connection speed
    t0 = time.perf_counter()
    driver.verify_connectivity()
    conn_ms = (time.perf_counter() - t0) * 1000
    print(f"[PASS] Connected to Neo4j in {conn_ms:.2f} ms")

    # 2. Verify database counts
    nodes_res, _, _ = driver.execute_query("MATCH (n) RETURN count(n) AS count")
    rels_res, _, _ = driver.execute_query("MATCH ()-[r]->() RETURN count(r) AS count")
    print(f"[PASS] Database Inventory: {nodes_res[0]['count']} Nodes | {rels_res[0]['count']} Relationships")

    # 3. Benchmark 1-Hop Traversal (Direct links to DarkKni9ht)
    t1 = time.perf_counter()
    hop1, _, _ = driver.execute_query(
        """
        MATCH (a:Entity {name: 'DarkKni9ht'})-[r]-(connected)
        RETURN coalesce(connected.evidence_id, connected.name) AS item, type(r) AS link
        """
    )
    hop1_ms = (time.perf_counter() - t1) * 1000
    print(f"\n[+] 1-Hop Traversal ('DarkKni9ht'): {len(hop1)} direct connections in {hop1_ms:.2f} ms")
    for row in hop1[:5]:
        print(f"    - {row['link']} -> {row['item']}")

    # 4. Benchmark 2-Hop Traversal (DarkKni9ht -> Evidence -> Linked Entities)
    t2 = time.perf_counter()
    hop2, _, _ = driver.execute_query(
        """
        MATCH (a:Entity {name: 'DarkKni9ht'})--(ev:Evidence)--(other:Entity)
        WHERE other.name <> 'DarkKni9ht'
        RETURN ev.evidence_id AS evidence, collect(DISTINCT other.name) AS linked_entities
        """
    )
    hop2_ms = (time.perf_counter() - t2) * 1000
    print(f"\n[+] 2-Hop Traversal (Shared Evidence): {len(hop2)} bridges found in {hop2_ms:.2f} ms")
    for row in hop2:
        print(f"    - Via {row['evidence']}: {row['linked_entities']}")

    print("\n[PASS] Connectivity & Traversal Verification Complete!")