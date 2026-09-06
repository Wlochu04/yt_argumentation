import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

def generate_comparison_graphs(data_file="YT_comparison.xlsx"):
    # Generate side-by-side network graphs comparing rhetorical strategies between two YouTube videos.
    try:
        df_comparison = pd.read_excel(data_file)
    except FileNotFoundError:
        print(f"Error: '{data_file}' not found. Please run the comparison pipeline first.")
        return

    valid_classes = ['Value', 'Policy', 'Fact', 'Testimony', 'Rhetorical']
    color_map = {
        'Value': '#ff9999',     
        'Policy': '#66b3ff',    
        'Fact': '#99ff99',      
        'Testimony': '#ffcc99', 
        'Rhetorical': '#c2c2f0'
    }

    # Extract unique videos to create subplots
    videos = df_comparison['video_title'].unique()
    
    # Force maximum 2 videos for the 1x2 subplot layout safety
    videos = videos[:2] 

    fig, axes = plt.subplots(1, 2, figsize=(20, 10))

    for i, vid_title in enumerate(videos):
        ax = axes[i] 
        
        # Filter valid rhetorical classes and calculate frequencies
        df_filtered = df_comparison[
            (df_comparison['video_title'] == vid_title) & 
            (df_comparison['rhetoric_class'].isin(valid_classes))
        ] 
        class_counts = df_filtered['rhetoric_class'].value_counts().to_dict()
        
        # Initialize graph topology
        G = nx.Graph()
        center_label = vid_title
        G.add_node(center_label)

        # Central nodes: Rhetorical categories
        for rhet_class, count in class_counts.items():
            G.add_node(rhet_class)
            G.add_edge(center_label, rhet_class, weight=count)

        # Satellite nodes: Comment snippets (max 2 per category)
        for rhet_class in valid_classes:
            subset = df_filtered[df_filtered['rhetoric_class'] == rhet_class].head(2)
            
            for index, row in subset.iterrows():
                comment_text = str(row['comment'])
                shortened_text = comment_text[:25] + "..." if len(comment_text) > 25 else comment_text
                satellite_name = f"ID:{index}\n{shortened_text}"
                
                G.add_node(satellite_name)
                G.add_edge(rhet_class, satellite_name, weight=1)

        # Assign visual styling based on node hierarchy
        node_sizes = []
        edge_widths = []
        node_colors = []

        for node in G.nodes():
            if node == center_label:
                node_sizes.append(4000)
                node_colors.append('#ffe680')
            elif node in valid_classes:
                size = class_counts.get(node, 0) * 50 + 1000
                node_sizes.append(size)
                node_colors.append(color_map[node])
            else:
                node_sizes.append(300) # Satellites
                node_colors.append('#e6e6e6')

        # Scale edge thickness by weight
        for u, v in G.edges():
            weight = G[u][v].get('weight', 1) 
            thickness = weight * 0.1 + 1 
            edge_widths.append(thickness)

        pos = nx.spring_layout(G, k=1.5, iterations=100, weight=None)

        # Shift labels dynamically downwards based on node size to prevent overlapping
        node_size_dict = dict(zip(G.nodes(), node_sizes))
        label_pos = {}
        for node, coords in pos.items():
            size = node_size_dict[node]
            dynamic_shift = (size ** 0.5) * 0.002 
            label_pos[node] = (coords[0], coords[1] - dynamic_shift)

        # Render graph elements
        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=node_sizes, node_color=node_colors, edgecolors='black')
        nx.draw_networkx_edges(G, pos, ax=ax, width=edge_widths, alpha=0.5)
        nx.draw_networkx_labels(G, label_pos, ax=ax, font_size=7, font_weight='bold', verticalalignment='top')

        ax.set_title(f"Rhetorical Analysis: {vid_title}", fontsize=14, fontweight='bold')
        ax.axis("off")

    # Add vertical separator line between subplots
    fig.add_artist(plt.Line2D([0.5, 0.5], [0.1, 0.9], transform=fig.transFigure, color="gray", linestyle="--", linewidth=1.5, alpha=0.7))

    plt.tight_layout()
    plt.show()
