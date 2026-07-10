from pyvis.network import Network

def export_to_html(G, output_path):
    """
    Takes a networkx graph and exports it as an interactive HTML file using pyvis.
    Applies custom styling for components, power nets, and highly connected nodes.
    """
    net = Network(height="800px", width="100%", bgcolor="#222222", font_color="white")
    
    # Power nets for special highlighting
    power_nets = ["GND", "VCC", "+3V3", "+5V", "3V3", "5V", "VDD", "VSS"]
    
    for node, data in G.nodes(data=True):
        node_type = data.get('type', 'unknown')
        degree = G.degree[node]
        
        # Default styling
        color = "#aaaaaa"
        size = 15
        shape = "dot"
        
        if node_type == 'net':
            # Highlight power nets in red
            if any(p in str(node).upper() for p in power_nets):
                color = "#ff4444"
                size = 25
            else:
                color = "#4444ff" # Regular nets in blue
                size = 15
            shape = "ellipse"
        elif node_type == 'component':
            # Highlight highly connected components (e.g. MCUs)
            if degree > 10:
                color = "#ffaa00" # Orange
                size = 30
            else:
                color = "#44ff44" # Regular components in green
                size = 20
            shape = "box"
            
        title = f"{node}\nType: {node_type}\nConnections: {degree}"
        
        net.add_node(node, label=str(node), title=title, color=color, size=size, shape=shape)

    for edge in G.edges():
        net.add_edge(edge[0], edge[1], color="#555555")
        
    # Set some physics options for better layout
    net.set_options("""
    var options = {
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -30000,
          "centralGravity": 0.3,
          "springLength": 95,
          "springConstant": 0.04,
          "damping": 0.09,
          "avoidOverlap": 0.1
        }
      }
    }
    """)
    
    # write_html saves it to the path without trying to open a web browser synchronously
    net.write_html(output_path)
