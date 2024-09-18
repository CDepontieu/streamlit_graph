import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import pandas as pd
import streamlit as st

import pandas as pd
import networkx as nx
from pyvis.network import Network
import re

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

def add_function_htmlTitle(content):
    file_path = 'test.html'
    print(f"\n\n\n---------------\n{content}\n--------------------\n\n\n")
    # Read the content of the HTML file
    #with open(file_path, 'r', encoding='windows-1252') as file:
        #content = file.read()

    #print(content)
        

    # Define the pattern to match the old function and the replacement text
    pattern = """// This method is responsible for drawing the graph, returns the drawn network"""
    replacement = '''
              function htmlTitle(html) {
                  const container = document.createElement("div");
                  container.innerHTML = html;
                  return container;
              }

              // This method is responsible for drawing the graph, returns the drawn network
    '''
    
    # Perform the replacement
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # Write the modified content back to the file
    #with open(file_path, 'w') as file:
        #file.write(new_content)

    return new_content

# Function to replace title values with htmlTitle
def replace_titles(match):
    # Extract the part within the brackets of the DataSet
    data_set_content = match.group(1)
    # Define the replacement pattern for titles
    updated_data_set_content = re.sub(
        r'"title":\s*"([^"]*)"',
        lambda m: f'"title": htmlTitle("{m.group(1)}")',
        data_set_content
    )
    # Return the modified line with DataSet
    return f'nodes = new vis.DataSet([{updated_data_set_content}]);'

import re
def use_htmlTitle(content):
    # Define the path to your HTML file
    file_path = 'test.html'

    # Read the content of the HTML file
    #with open(file_path, 'r') as file:
        #content = file.read()

    # Define the regex pattern to match the nodes assignment line
    pattern = r'nodes\s*=\s*new\s+vis\.DataSet\(\[(.*?)\]\);'

    # Perform the replacement
    new_content = re.sub(pattern, replace_titles, content, flags=re.DOTALL)

    # Write the modified content back to the file
    #with open(file_path, 'w') as file:
        #file.write(new_content)
    return new_content


def add_function_htmlTitle(content):
    file_path = 'test.html'

    # Read the content of the HTML file
    #with open(file_path, 'r') as file:
        #content = file.read()

    # Define the pattern to match the old function and the replacement text
    pattern = """// This method is responsible for drawing the graph, returns the drawn network"""
    replacement = '''
                  function htmlTitle(html) {
                    const container = document.createElement("div");
                    container.innerHTML = html;
                    return container;
                  }

                  // This method is responsible for drawing the graph, returns the drawn network
    '''

    # Perform the replacement
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # Write the modified content back to the file
    #with open(file_path, 'w') as file:
        #file.write(new_content)

    return new_content

def simple_func(url_csv, hierarchical=False, height_input="900", width_input="100"): 
    #df = pd.read_csv("C:\\Users\\CharlesDepontieu\\streamlit_network\\neo4j_database.csv", sep=",", header=0)
    df = pd.read_csv(url_csv, sep=",", header=0)
    #### reorder new dataframe to old dataframe schema
    df = df.rename(columns={'Nom': 'Name', 'Node Label': 'node label (normé)'})
    df = df[['Name', 'node label (normé)', 'linked to (normé)', 'type_of_link (normé)', 'label_linked_to (normé)', 'Properties_nom', 'Properties_linked_to']]
    #### end of reorder
  
    #"https://docs.google.com/spreadsheets/d/e/2PACX-1vQL41ALXABaTA1_5UI0jVyVOoavBwrBaMUMjZlZ4sx4yHt9KCwDkOx_URPPfxuA2A/pub?gid=1772947737&single=true&output=csv"
    net = Network(
        select_menu=True,
        filter_menu=True,
        cdn_resources="remote",
        bgcolor="#222222",
        font_color="white",
        height=height_input+"px",
        width=width_input+"%",
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
    #net.show("test.html")

    html_file = net.generate_html()
    return html_file

def add_div_display_info_node(content):
    file_path = 'test.html'

    # Read the content of the HTML file
    #with open(file_path, 'r', encoding='windows-1252') as file:
        #content = file.read()

    #print(content)
    
    # Define the pattern to match the old function and the replacement text
    pattern = r'<div id="mynetwork" class="card-body"></div>\s*</div>'
    replacement = '''
            <div id="mynetwork" class="card-body"></div>
        </div>
        <div id="nodeInfo">Click on a node to see details here.</div>
        '''

    # Perform the replacement
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # Write the modified content back to the file
    #with open(file_path, 'w') as file:
        #file.write(new_content)

    return new_content

    

def add_onclick_node_event(content):
    file_path = 'test.html'

    # Read the content of the HTML file
    #with open(file_path, 'r', encoding='windows-1252') as file:
        #content = file.read()

    #print(content)
    
    # Define the pattern to match the old function and the replacement text
    pattern = r"""drawGraph\(\);"""
    replacement = '''
              drawGraph();
              // Step 2: Add an event listener for the click event
              network.on('click', function(params) {
                if (params.nodes.length > 0) {
                  var clickedNodeId = params.nodes[0];
                  var clickedNode = nodes.get(clickedNodeId);

                  // Update the display section with the clicked node information
                  var nodeInfoDiv = document.getElementById('nodeInfo');
                  nodeInfoDiv.innerHTML = `
                    <h3>Node Information</h3>
                    <p><strong>Nom:</strong> ${clickedNode.label}</p>
                    <p><strong>Informations:</strong> ${clickedNode.title.innerHTML}</p>
                  `;
                }
              });    
              '''

    # Perform the replacement
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # Write the modified content back to the file
    #with open(file_path, 'w') as file:
        #file.write(new_content)

    return new_content

    
