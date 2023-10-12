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


with tab2:
    
    st.title("Kaart met bezetting per Laadpaal")
    # streamlit een titel geven
    st.write('Om inzicht te krijgen in niet alleen de plek van de laadpaal, maar ook de bezetting per',
            'laadpaal is de volgende kaart gemaakt. Op deze kaart is elke kaart uit de dataset te zien.',
            'De grote van de cirkel bepaald hoe hoog de bezetting is; hoe groter de',
            'circkel hoe hoger de bezetting van die laadpaal. Om de specifieke bezetting te achterhalen',
            'is het mogelijk om op een bubbel te klikken en de bezetting als getal te zien.',
            'De kleur van de cirkel bepaald in welke provincie de paal zich bevindt. In totaal',
            'worden 1000 Laadpalen als voorbeeld gebruikt. Deze limitatie heeft te maken met de',
            'snelheid en performace van de applicatie.',
            'De bezetting is gebasseerd op gemeente. De bezetting is dus het aantal inwoners van de gemeente',
            'gedeeld door het aantal palen in die gemeente.')

    def color_producer(Provincie):
        """
        Een simpele functie die verderop gebruikt gaat worden
        om kleur te geven aan elke provincie op basis van provincie.
        Neemt als argument de provincie als string en geeft de naam
        van de kleur terug die bij die provincie hoort.
        """
        if Provincie == 'Groningen':
            return 'green'
        if Provincie == 'Friesland':
            return 'blue'
        if Provincie == 'Drenthe':
            return 'red'
        if Provincie == 'Noord-Holland':
            return 'orange'
        if Provincie == 'Overijssel':
            return 'yellow'
        if Provincie == 'Zuid-Holland':
            return 'maroon'
        if Provincie == 'Utrecht':
            return 'lime'
        if Provincie == 'Flevoland':
            return 'aqua'
        if Provincie == 'Gelderland':
            return 'darkblue'
        if Provincie == 'Zeeland':
            return 'purple'
        if Provincie == 'Noord-Brabant':
            return 'black'
        if Provincie == 'Limburg':
            return 'crimson'
        else:
            return 'white'

    Laadpalen = pd.read_csv('data.csv')
    # Laadpalen dataframe halen uit de data.csv. Als dit niet lukt run dan eerst in python stream.py.

    def coordinaten(regio):
        """
        Een simpele functie die later gebruikt gaat worden om
        In te zoomen op provincies via een dropdown menu.
        Neemt als argument een string (naam van provincie).
        Geeft als waarde de LAT en LONG van de provincie.
        """
        if regio == 'Nederland':
            return [52.1326, 5.2913]
        if regio == 'Noord-Holland':
            return [52.3702, 4.8952]
        if regio == 'Zuid-Holland':
            return [51.9225, 4.47917]
        if regio == 'Utrecht':
            return [52.0893191, 5.1101691]
        if regio == 'Groningen':
            return [53.2194, 6.5665]
        if regio == 'Gelderland':
            return [51.9851, 5.8987]
        if regio == 'Noord-Brabant':
            return [51.6998, 5.3049]
        if regio == 'Friesland':
            return [53.2014, 5.8086]
        if regio == 'Drenthe':
            return [52.9925, 6.5649]
        if regio == 'Overijssel':
            return [52.5159, 6.0836]
        if regio == 'Zeeland':
            return [51.4988, 3.6109]
        if regio == 'Limburg':
            return [50.8514, 5.6913]
        if regio == 'Flevoland':
            return [52.518537, 5.471422]

    def zoomstart(regio):
        """
        Functie om de zoom goed te zetten
        """
        if regio == 'Nederland':
            return 7
        else:
            return 9
            
    regio = st.selectbox('Selecteer een regio', ['Nederland', 'Groningen', 'Friesland', 'Drenthe', 'Noord-Holland', 'Flevoland', 'Overijssel', 'Zuid-Holland', 'Utrecht', 'Gelderland', 'Zeeland', 'Noord-Brabant', 'Limburg'])
    # Maken van een dropdown menu met daarin alle provincies.
    long_lat = coordinaten(regio)
    zoom = zoomstart(regio)
    # Klaarzetten van gegevens voor de kaart.
    m = folium.Map(location=long_lat, zoom_start=zoom)
    # Maken van een folium map en inzoomen en centeren op Nederland.  
    for i in Laadpalen.index:
        text = 'Bezetting:',round(Laadpalen['Radius'][i]*13.9)
        folium.Circle(location=[Laadpalen['AddressInfo.Latitude'][i],Laadpalen['AddressInfo.Longitude'][i]],      
                        popup=text,
                        tooltip='Gebruik om bezetting te zien',
                        color=color_producer(Laadpalen['AddressInfo.StateOrProvince'][i]),
                        fill=True,
                        fill_color=color_producer(Laadpalen['AddressInfo.StateOrProvince'][i]),
                        radius=Laadpalen['Radius'][i]
                                    ).add_to(m)

    folium.TileLayer(tiles='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', attr = 'CartoDB.Positron').add_to(m)

    st_map = st_folium(m, width=700)
    
    # Folium map toevoegen aan streamlit.    
    st.write("""
            Door te kijken naar de kaart is de volgende conclusie getrokken: De trend is dat in grote gemeentes
             zoals Amsterdam en Rotterdam de bezetting per paal relatief laag is. De druk per paal is dan ook goed
             verdeeld. In kleine gemeentes zoals Ameland en Vlieland is het aantal palen heel laag, maar is de bezetting laag
             door het lage aantal inwoners. Waar de druk per laadpaal niet goed verdeeld is, is in middel-grote gemeentes.
             Dit zijn gemeentes zoals Hilversum of Oss. In deze gemeentes zijn het aantal laadpalen heel laag, terwijl het
             aantal inwoners van deze gemeentes toch heel hoog zijn. De conclusie is dan ook dat in grote en kleine
             gemeentes de druk van laadpalen laag is, in middel-grote gemeentes is waar er te weinig palen zijn
             per inwoner.
         """)
    st.write("""
            Zoals eerder vermeld is het aantal palen wat is opgezocht via de API duizend. Door dit aantal zou het voor kunnen komen
             Dat in middel-grote gemeentes een vertekend beeld onstaat, doordat niet alle palen mee zijn genomen. Als er meer tijd zou
             zijn, zouden er volgende keer meer palen meegenomen kunnen worden voor een beter beeld.
    """)
    # Uitleg over de kaart.
    legend = """
    <div style="position: fixed; bottom: 25px; left: 50px; z-index: 1000; background-color: white; padding: 5px; border: 2px solid gray; border-radius: 5px;">
    <h4 style="font-size: 12px;">Legenda</h4>
    """

    for value, kleur in [('Groningen', 'green'), ('Friesland', 'blue'), ('Drenthe', 'red'), ('Noord-Holland', 'orange'), ('Overijssel', 'yellow'), ('Zuid-Holland', 'maroon'), ('Utrecht', 'lime'), ('Flevoland', 'aqua'), ('Gelderland', 'darkblue'), ('Zeeland', 'purple'), ('Noord-Brabant', 'black'), ('Limburg', 'crimson')]:
        legend += f'<p style="font-size: 11px;"><i style="background:{kleur}; border-radius:50%; width: 10px; height: 10px; display:inline-block;"></i> {value}</p>'

    st.markdown(legend, unsafe_allow_html=True)

# In[52]:

