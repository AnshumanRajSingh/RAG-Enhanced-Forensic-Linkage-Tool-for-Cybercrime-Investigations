import os
import networkx as nx
from pyvis.network import Network
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from graph_builder import build_knowledge_graph

OUTPUT_HTML = "data/graph_visualization.html"

def generate_interactive_graph():
    """
    Renders an interactive 2D physics-based HTML network graph from the NetworkX Knowledge Graph.
    """
    G = build_knowledge_graph()

    if G.number_of_nodes() == 0:
        print("[!] Error: Graph is empty. Cannot generate visualization.")
        return

    # Initialize PyVis Network
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", select_menu=True, filter_menu=True)
    net.from_nx(G)

    # Apply Custom Styling to Nodes based on Type
    for node in net.nodes:
        node_id = node["id"]
        node_data = G.nodes[node_id]
        
        if node_data.get("node_type") == "Evidence":
            node["color"] = "#FF4B4B"  # Red for Evidence records
            node["shape"] = "box"
            node["title"] = f"Evidence ID: {node_id}\nType: {node_data.get('source_type')}"
        else:
            entity_type = node_data.get("entity_type", "Entity")
            node["color"] = "#00D26A" if entity_type in ["IP_ADDRESS", "crypto_wallet"] else "#1E90FF"
            node["shape"] = "dot"
            node["size"] = 18
            node["title"] = f"Entity: {node_id}\nType: {entity_type}\nExtractor: {node_data.get('extractor', 'N/A')}"

    # Configure Physics simulation options
    net.toggle_physics(True)
    
    # Save Interactive HTML Visualization
    os.makedirs("data", exist_ok=True)
    net.write_html(OUTPUT_HTML)
    print(f"[+] Interactive Knowledge Graph rendered successfully!")
    print(f"[PASS] Visualization saved to: {os.path.abspath(OUTPUT_HTML)}")

if __name__ == "__main__":
    generate_interactive_graph()