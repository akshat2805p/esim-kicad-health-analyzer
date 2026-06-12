import networkx as nx

def build_dependency_graph(board):
    """
    Reads a pcbnew Board object and builds a bipartite graph 
    of components and their connected nets.
    """
    G = nx.Graph()
    
    # Iterate through all footprints (components) on the board
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        
        # Add the component as a node
        G.add_node(ref, type='component')
        
        # Iterate through all pads of the footprint
        for pad in fp.Pads():
            net_name = pad.GetNetname()
            
            # If the pad is connected to a net (ignore empty string or "Unconnected")
            if net_name and net_name != "":
                # Add the net as a node
                G.add_node(net_name, type='net')
                
                # Create an edge between the component and the net
                G.add_edge(ref, net_name)
                
    return G
