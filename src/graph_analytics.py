import sys
import os
import networkx as nx

# Add current directory to path for clean imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from graph_builder import build_knowledge_graph

def run_graph_analytics():
    """
    Performs link analysis, centrality scoring, and community detection
    on the forensic knowledge graph to rank critical entities.
    """
    G = build_knowledge_graph()
    
    if G.number_of_nodes() == 0:
        print("[!] Error: Graph has no nodes to analyze.")
        return

    print("\n==============================================")
    print("      FORENSIC LINK ANALYSIS REPORT          ")
    print("==============================================")

    # 1. Compute Centrality Metrics
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    pagerank_scores = nx.pagerank(G)

    # 2. Attach Analytics as Node Attributes
    for node in G.nodes():
        G.nodes[node]["degree_centrality"] = degree_centrality[node]
        G.nodes[node]["betweenness_centrality"] = betweenness_centrality[node]
        G.nodes[node]["pagerank"] = pagerank_scores[node]

    # 3. Print Top 5 Most Connected Nodes (Degree)
    sorted_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)
    print("\n[+] Top 5 Central Entities (Highest Connections):")
    for node, score in sorted_degree[:5]:
        n_type = G.nodes[node].get("node_type", "Entity")
        print(f"    - [{n_type}] {node} (Score: {score:.4f})")

    # 4. Print Top 5 Key Bridge Entities (Betweenness)
    sorted_betweenness = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)
    print("\n[+] Top 5 High-Risk Bridge Entities (Betweenness):")
    for node, score in sorted_betweenness[:5]:
        n_type = G.nodes[node].get("node_type", "Entity")
        print(f"    - [{n_type}] {node} (Score: {score:.4f})")

    # 5. Community Detection / Connected Clusters
    components = list(nx.connected_components(G))
    print(f"\n[+] Detected {len(components)} Sub-Network Cluster(s):")
    for idx, comp in enumerate(components, 1):
        entities_in_cluster = [n for n in comp if G.nodes[n].get("node_type") == "Entity"]
        print(f"    - Cluster {idx}: {len(comp)} total nodes ({len(entities_in_cluster)} entities)")

    return G

if __name__ == "__main__":
    run_graph_analytics()