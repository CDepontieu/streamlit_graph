import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import pandas as pd
import streamlit as st

import pandas as pd
import networkx as nx
from pyvis.network import Network


def simple_func_bis(physics): 
  nx_graph = nx.cycle_graph(10)
  nx_graph.nodes[1]['title'] = 'Number 1'
  nx_graph.nodes[1]['group'] = 1
  nx_graph.nodes[3]['title'] = 'I belong to a different group!'
  nx_graph.nodes[3]['group'] = 10
  nx_graph.add_node(20, size=20, title='couple', group=2)
  nx_graph.add_node(21, size=15, title='couple', group=2)
  nx_graph.add_edge(20, 21, weight=5)
  nx_graph.add_node(25, size=25, label='lonely', title='lonely node', group=3)


  nt = Network("500px", "500px",notebook=True,heading='')
  nt.from_nx(nx_graph)
  #physics=st.sidebar.checkbox('add physics interactivity?')
  if physics:
    nt.show_buttons(filter_=['physics'])
  nt.show('test.html')

def simple_func(hierarchical=False): 
    #df = pd.read_csv("C:\\Users\\CharlesDepontieu\\streamlit_network\\neo4j_database.csv", sep=",", header=0)
    df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vQL41ALXABaTA1_5UI0jVyVOoavBwrBaMUMjZlZ4sx4yHt9KCwDkOx_URPPfxuA2A/pub?gid=1772947737&single=true&output=csv", sep=",", header=0)
    net = Network(
        select_menu=True,
        filter_menu=True,
        cdn_resources="remote",
        bgcolor="#222222",
        font_color="white",
        height="750px",
        width="100%",
        layout=hierarchical
    )

    # Define a color mapping for the 'label_linked_to (normé)' column
    color_mapping = {
        "ecole": "red",
        "association": "blue",
        "lieu": "green",
        "entreprise": "yellow"
    }

    # Add a color column to the DataFrame
    df['color'] = df['label_linked_to (normé)'].map(color_mapping)

    # Create the graph using NetworkX
    G = nx.Graph()
    #G.set_options(

    # Add nodes with color attribute
    for index, row in df.iterrows():
        G.add_node(
            row['linked to (normé)'], 
            color=row['color'], 
            label=row['linked to (normé)'],
            title=row['Properties_linked_to'] if 'Properties_linked_to' in row else ''#,
            #value=1
        )
        G.add_node(
            row['Name'], 
            color='grey', 
            label=row['Name'],
            title=row['Properties_nom'] if 'Properties_nom' in row else ''#,
            #value=1
        )
        G.add_edge(row['Name'], row['linked to (normé)'])

    ####################################
    # Get the adjacency list and update node attributes
    #print(f"\n------------------------\n\nG.adjacency : {G.adjacency()}\n------------------------\n\n")

    # Get the adjacency list and compute node degrees
    degrees = dict(G.degree())
    
    # Min-max normalization of node values
    min_degree = min(degrees.values())
    max_degree = max(degrees.values())
    range_degree = max_degree - min_degree


    for node, degree in degrees.items():# in G.adjacency():
      if range_degree == 0:
            normalized_value = 1
      else:
            normalized_value = 1 + 3 * (degree - min_degree) / range_degree  # Scale values to range [1, 10]
      G.nodes[node]['value'] = normalized_value
      #print("-----------------------------")
      #print(f"node : {node}")
      #print(f"neigbors {neighbors} of len {len(neighbors)}")
      #print("------------------------------")
      #G.nodes[node]['title'] += f" Neighbors: {', '.join(neighbors)}"
      #G.nodes[node]['value'] = len(neighbors)
      #print(f"node : {G.nodes[node]}")

    ####################################

    # Load the NetworkX graph into the pyvis Network
    net.from_nx(G)

    # Show buttons for interaction
    #if physics:
      #net.show_buttons(filter_=['physics'])

    # Display the graph
    net.show("test.html")

    html_file = "test.html"
    with open(html_file, 'r') as file:
        html_content = file.read()

    # JavaScript for handling click events
    click_js = """
    <script type="text/javascript">
        document.addEventListener("DOMContentLoaded", function() {
            var network = document.querySelector("#mynetwork");
            network.onclick = function(params) {
                var nodeId = this.getEventPosition(params).nodes[0];
                var node = this.body.data.nodes.get(nodeId);
                if (node) {
                    alert('Node clicked: ' + node.label + '\\nTitle: ' + node.title);
                }
            };
        });
    </script>
    """

    # Insert the JavaScript before the closing </body> tag
    html_content = html_content.replace("</body>", click_js + "</body>")

    # Write the modified HTML content back to the file
    with open(html_file, 'w') as file:
        file.write(html_content)

