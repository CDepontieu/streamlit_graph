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

password = st.text_input("Test application")

if password == "charles":

  st.sidebar.title('Choose your favorite Graph')
  option=st.sidebar.selectbox('select graph',('graph','excel'))
  




  #from streamlit_gsheets import GSheetsConnection
  import pandas as pd
  import streamlit.components.v1 as components



  if option=='excel':
    df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vQL41ALXABaTA1_5UI0jVyVOoavBwrBaMUMjZlZ4sx4yHt9KCwDkOx_URPPfxuA2A/pub?gid=1772947737&single=true&output=csv", sep=",", header=0)
    st.dataframe(df)
    # Create a connection object.
    #conn = st.connection("gsheets", type=GSheetsConnection)
    iframe_src = "https://docs.google.com/spreadsheets/d/10Ntz8ioCljJ6uJKox0Aj7YGkGfzIjwKi/edit?usp=sharing&ouid=117463936283670123491&rtpof=true&sd=true"
    components.iframe(iframe_src, height=500)

    #df = conn.read()


  if option=='graph':
    hierachical_display=st.sidebar.selectbox('Hierarchical display ?',(True, False))
    got.simple_func(hierachical_display)

    got.add_function_htmlTitle()
    got.use_htmlTitle()
    got.add_div_display_info_node()
    got.add_onclick_node_event()

    HtmlFile = open("test.html", 'r')#, encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 1200,width=900, scrolling=True)


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
