import json
import os
import sys
import networkx as nx

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from graph_analytics import run_graph_analytics
from graph_visualizer import generate_interactive_graph

GRAPH_JSON_FILE = "data/knowledge_graph.json"

def run_master_graph_pipeline():
    """
    Executes the end-to-end Knowledge Graph construction, link analysis,
    JSON serialization, and interactive HTML visualization export.
    """
    print("==================================================")
    print("   STARTING KNOWLEDGE GRAPH PIPELINE       ")
    print("==================================================")

    # 1. Run Link Analysis & Get Populated NetworkX Graph
    G = run_graph_analytics()
    if not G or G.number_of_nodes() == 0:
        print("[!] Pipeline aborted due to empty graph.")
        return

    # 2. Export Graph to Node-Link JSON Dataset
    graph_data = nx.node_link_data(G)
    with open(GRAPH_JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, indent=2)
    print(f"\n[PASS] Serialized Knowledge Graph dataset saved to: {GRAPH_JSON_FILE}")

    # 3. Generate Interactive HTML Visualization
    generate_interactive_graph()

    print("\n[PASS] Master Knowledge Graph Pipeline completed successfully!")

if __name__ == "__main__":
    run_master_graph_pipeline()