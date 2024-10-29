import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import got 
#import connexion_google_sheet
#from streamlit_gsheets import GSheetsConnection


#Network(notebook=True)
st.title('Hello Pyvis')
# make Network show itself with repr_html

#def net_repr_html(self):
#  nodes, edges, height, width, options = self.get_network_data()
#  html = self.template.render(height=height, width=width, nodes=nodes, edges=edges, options=options)
#  return html

#Network._repr_html_ = net_repr_html
################## RAJOUT SEPTEMBRE 2024 ##################
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# https://discuss.streamlit.io/t/cannot-import-name-hasher-from-streamlit-authenticator/65675
#from streamlit_authenticator.utilities.hasher import Hasher

#passwords_to_hash = [mdp]
#hashed_passwords = Hasher(passwords_to_hash).generate()

# Pre-hashing all plain text passwords once
# Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']#,
    #config['pre-authorized']
)

#name, authentication_status, username = authenticator.login('Login', 'sidebar')

authenticator.login()

import time
if st.session_state['authentication_status']:
  authenticator.logout()
  st.write(f'Welcome *{st.session_state["name"]}*')
  st.title('Some content')

  st.sidebar.title('Choose your favorite Graph')
  option=st.sidebar.selectbox('select graph',('graph','excel'))
  




  #from streamlit_gsheets import GSheetsConnection
  import pandas as pd
  import streamlit.components.v1 as components
  url_csv = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR8okehu69k3stGTmNEJ1vM-ty4U1pkfyHa8tqV8AIU9LCwdT_YpK3UJmXNvs0jXCqFh-tI5nAd_p_G/pub?gid=772613351&single=true&output=csv"
    #new : "https://docs.google.com/spreadsheets/d/e/2PACX-1vR8okehu69k3stGTmNEJ1vM-ty4U1pkfyHa8tqV8AIU9LCwdT_YpK3UJmXNvs0jXCqFh-tI5nAd_p_G/pub?gid=772613351&single=true&output=csv"
    #old : "https://docs.google.com/spreadsheets/d/e/2PACX-1vQL41ALXABaTA1_5UI0jVyVOoavBwrBaMUMjZlZ4sx4yHt9KCwDkOx_URPPfxuA2A/pub?gid=1772947737&single=true&output=csv" 
    
    #"https://docs.google.com/spreadsheets/d/e/2PACX-1vR8okehu69k3stGTmNEJ1vM-ty4U1pkfyHa8tqV8AIU9LCwdT_YpK3UJmXNvs0jXCqFh-tI5nAd_p_G/pub?gid=772613351&single=true&output=csv"
    #"https://docs.google.com/spreadsheets/d/e/2PACX-1vQL41ALXABaTA1_5UI0jVyVOoavBwrBaMUMjZlZ4sx4yHt9KCwDkOx_URPPfxuA2A/pub?gid=1772947737&single=true&output=csv"



  if option=='excel':
    st.markdown("[Formulaire pour ajouter et modifier la base de données](https://docs.google.com/spreadsheets/d/1Nrml-VocDYtnUxcLhEZlWhdlNheN1DeSttGbOHCtFRg/edit?usp=sharing)")

    df = pd.read_csv(url_csv, sep=",", header=0)
    st.dataframe(df)
    

    #df = conn.read()


  if option=='graph':
    hierachical_display=st.sidebar.selectbox('Hierarchical display ?',(False, True))
    
    smartphone = st.checkbox("Smartphone display")
    if smartphone : 
      height_input ="800"
      width_input_px=350
    else:
      height_input = "900"
      width_input_px = 900
    #( url_csv, hierarchical=False, height_input="900", width_input="100")


    selected_mode_filter_dataframe = st.selectbox("Filtrer le df par:", ["mot_dans_description_node","Toute_la_database", "node"])

    df = pd.read_csv(url_csv, sep=",", header=0)
    #st.dataframe(df)
      
    if selected_mode_filter_dataframe == "mot_dans_description_node":
        #st.write("mot_dans_description_node")
        # Add input for filtering by word
        word_to_filter = st.text_input("Enter a word to filter rows by:")
    
        # If a word is entered, filter the DataFrame
        if word_to_filter:
            filtered_by_word_df = got.filter_rows_by_word(word_to_filter, df)
            #st.write(f"Filtered results containing the word '{word_to_filter}':")
            #st.dataframe(filtered_by_word_df)
            filtered_df = filtered_by_word_df.copy()
        else:
            st.write("Merci d'entrer un mot pour filtrer le dataframe")

        
        
    elif selected_mode_filter_dataframe == "node":
        top_nodes = got.find_top_two_nodes_with_most_relations(df)
        # Create a select box for node selection
        # Create a select box for node selection with counts
        node_options = [f"{node[0]} (Nombre de connexions: {node[1]})" for node in top_nodes]  # Format: Node (Count)

        col1, col2 = st.columns(2)
        with col1:
            selected_node_str = st.selectbox("Select a node to filter by:", node_options)
        with col2:
            depth_analysis = st.selectbox("Profondeur des relations:", [1, 2, 3])
        
        # Extract the node name from the selected option
        selected_node = selected_node_str.split(" (Nombre de connexions:")[0]  # Get the node name without the count
        # Filter DataFrame based on selected node
        filtered_df = got.filter_by_node(selected_node, df, depth_analysis)
        #filtered_df = got.filter_by_node(selected_node, df)
    
        # Display the filtered DataFrame
        #st.write(f"Filtered results for node: {selected_node}")
        #st.dataframe(filtered_df)
    
        # Display top nodes
        #st.write("Top two nodes with the most relations:")
        #for node in top_nodes:
            #st.write(f"Node: {node[0]}, Relations Count: {node[1]}")
    elif selected_mode_filter_dataframe =="Toute_la_database":
        st.write("all database selected")
        filtered_df = df.copy()
        
    st.dataframe(filtered_df)        

    if st.button("Submit_dataframe"):
        Htmlfile = got.simple_func(filtered_df, hierachical_display, height_input)
    
        Htmlfile = got.add_function_htmlTitle(Htmlfile)
        Htmlfile = got.use_htmlTitle(Htmlfile)
        Htmlfile = got.add_div_display_info_node(Htmlfile)
        Htmlfile = got.add_onclick_node_event(Htmlfile)
    
        #HtmlFile = open("test.html", 'r')#, encoding='utf-8')
        #source_code = Htmlfile.read() 
        components.html(Htmlfile, height = int(height_input)*1.6,width=width_input_px, scrolling=True)


  #got.got_func(physics)

  #if option=='GOT':
    #HtmlFile = open("gameofthrones.html", 'r', encoding='utf-8')
    #source_code = HtmlFile.read() 
    #components.html(source_code, height = 1200,width=1000)



  #got.karate_func(physics)

  #if option=='Karate':
    #HtmlFile = open("karate.html", 'r', encoding='utf-8')
    #source_code = HtmlFile.read() 
    #components.html(source_code, height = 1200,width=1000)
elif st.session_state['authentication_status'] is False:
    time.sleep(5)
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    time.sleep(5)
    st.warning('Please enter your username and password')
