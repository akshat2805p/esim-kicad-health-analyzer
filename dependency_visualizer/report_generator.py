import json

def generate_report(G, output_path):
    """
    Generates a statistical report from the dependency graph and exports it to JSON.
    """
    # Count components and nets
    components = sum(1 for _, data in G.nodes(data=True) if data.get('type') == 'component')
    nets = sum(1 for _, data in G.nodes(data=True) if data.get('type') == 'net')
    connections = G.number_of_edges()
    
    # Find most connected component
    component_degrees = {node: deg for node, deg in G.degree() if G.nodes[node].get('type') == 'component'}
    most_connected = max(component_degrees, key=component_degrees.get) if component_degrees else None
    
    report_data = {
        "components": components,
        "nets": nets,
        "connections": connections,
        "most_connected": most_connected
    }
    
    with open(output_path, 'w') as f:
        json.dump(report_data, f, indent=4)
        
    return report_data
