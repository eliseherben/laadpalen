#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import plotly.express as px
import streamlit as st
import requests
import plotly.graph_objects as go
import matplotlib.pyplot as plt
# import ipywidgets as widgets
#from ipywidgets import interact
from IPython.display import display
import folium
from streamlit_folium import folium_static
from streamlit_folium import st_folium
import numpy as np
from plotly.subplots import make_subplots
import math
import plotly.figure_factory as ff


# In[ ]:


tab1, tab2, tab3, tab4 = st.tabs(["Introductie", "API laadpalen", "Laadpalen dataset", "RDW datasets"])


# In[ ]:


with tab1:
    Laadpalen = pd.read_csv("Laadpalen.csv")


# In[ ]:


with tab1:
    Laadpalen['Type Laadpaal'] = Laadpalen['CurrentTypeID']
    Laadpalen['Snelladen'] = Laadpalen['Level.IsFastChargeCapable']
    Laadpalen['Niveau Laadpaal'] = Laadpalen['LevelID']


# In[ ]:


with tab1:


    # Titel van de app
    st.title('Laadpalen in Nederland')

    # Weergave van de tekst
    st.write("Op de onderstaande kaart van Nederland is weergeven waar de laadpalen in Nederland te vinden zijn. Met behulp van de eerste dropdownmenu kan gewisseld worden tussen verschillende variabelen voor de laadpalen. Daarnaast kan met de andere dropdownmenu in gezoomd op een bepaalde stad naar keuze.")

    def coordinaten(regio):
        if regio == 'Nederland':
            return [52.1326, 5.2913]
        if regio == 'Amsterdam':
            return [52.3702, 4.8952]
        if regio == 'Rotterdam':
            return [51.9225, 4.47917]
        if regio == 'Utrecht':
            return [52.0893191, 5.1101691]
        if regio == 'Groningen':
            return [53.2194, 6.5665]
        if regio == 'Arnhem':
            return [51.9851, 5.8987]
        if regio == "'s-Hertogenbosch":
            return [51.6998, 5.3049]
        if regio == 'Leeuwarden':
            return [53.2014, 5.8086]
        if regio == 'Assen':
            return [52.9925, 6.5649]
        if regio == 'Zwolle':
            return [52.5159, 6.0836]
        if regio == 'Middelburg':
            return [51.4988, 3.6109]
        if regio == 'Maastricht':
            return [50.8514, 5.6913]

    def zoomstart(regio):
        if regio == 'Nederland':
            return 7
        else:
            return 10


    def color_producer(type):
        if type == 10.0:
            return 'pink'
        if type == 20.0:
            return 'RGB(255,255,179)'
        if type == 30.0:
            return 'RGB(128,177,211)'
        if type == True:
            return 'RGB(251,128,114)'
        if type == False:
            return 'RGB(128,177,211)'
        if type == 1.0:
            return 'RGB(251,128,114)' 
        if type == 2.0:
            return 'RGB(179,222,105)'
        if type == 3.0: 
            return 'purple'

        # Voeg andere types en hun bijbehorende kleuren toe zoals nodig
        return 'grey'  # Standaardkleur voor onbekende types


    def create_legend(selected_variable):
        legend_html = """
        <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; background-color: white; padding: 10px; border: 2px solid gray; border-radius: 5px;">
        <h4>Legenda</h4>
        """
        if selected_variable == 'Type Laadpaal':
            for type_value, color in [('AC (Enkelfasig)', 'pink'), ('AC (Driefasig)', 'RGB(255,255,179)'), ('DC', 'RGB(128,177,211)'), ('Onbekend', 'grey')]:
                legend_html += f'<p><i style="background:{color}; border-radius:50%; width: 20px; height: 20px; display:inline-block;"></i> {type_value}</p>'
        elif selected_variable == 'Snelladen':
            for type_value, color in [('Snelladen', 'RGB(251,128,114)'), ('Niet snelladen', 'RGB(128,177,211)'), ('Onbekend', 'grey')]:
                legend_html += f'<p><i style="background:{color}; border-radius:50%; width: 20px; height: 20px; display:inline-block;"></i> {type_value}</p>'    
            # Voeg legenda voor LevelID toe
        elif selected_variable == 'Niveau Laadpaal':
            for type_value, color in [('Niveau 1 : Laag (Onder 2kW)', 'RGB(251,128,114)'), ('Niveau 2 : Medium (Tussen 2kW en 40kW)', 'RGB(179,222,105)'), ('Niveau 3:  Hoog (Meer dan 40kW)', 'purple'), ('Onbekend', 'grey')]:
                legend_html += f'<p><i style="background:{color}; border-radius:50%; width: 20px; height: 20px; display:inline-block;"></i> {type_value}</p>'
        # Voeg legenda voor andere variabelen toe zoals nodig
        legend_html += "</div>"

        return legend_html

    # Streamlit-frontend

    
    variable = st.selectbox('Selecteer een variable', ['Type Laadpaal', 'Snelladen', 'Niveau Laadpaal'])

    regio = st.selectbox('Selecteer een regio', ['Nederland', 'Amsterdam', 'Rotterdam', 'Utrecht', 'Groningen', 'Leeuwarden', 'Assen', 'Arnhem', 'Zwolle', "'s-Hertogenbosch", 'Middelburg', 'Maastricht'])
    long_lat = coordinaten(regio)
    zoom = zoomstart(regio)

    # Standaard zoom en centrum van de kaart (locatie Dam Amsterdam)
    m = folium.Map(location=long_lat, zoom_start=zoom)

    for index, row in Laadpalen.iterrows():
        folium.Circle(location= [row['AddressInfo.Latitude'], row['AddressInfo.Longitude']], 
        tooltip=row[variable],
        color=color_producer(row[variable]),
        fill=True,
        fill_color=color_producer(row[variable]),
        radius=100
                     ).add_to(m)

    folium.TileLayer(tiles='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', attr = 'CartoDB.Positron').add_to(m)


    # Voeg de kaart toe aan de Streamlit-app
    folium_static(m)


    legend_html = create_legend(variable)
    st.markdown(legend_html, unsafe_allow_html=True)

