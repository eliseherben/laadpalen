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


with tab4:
    merken = pd.read_csv("merken.csv")
    cumulatief = pd.read_csv("cumulatief.csv")


# In[ ]:


with tab4:
    # Titel voor de Streamlit-app
    st.title('Populaire Automerken')

    # Introductietekst
    intro_text = """
    Deze grafiek biedt inzicht in de meest populaire automerken. De gegevens zijn gegroepeerd op basis van verschillende brandstoffen. Voor deze visualisatie hebben we de belangrijkste brandstofcategorieën uit onze dataset geselecteerd. Een voertuig wordt als hybride beschouwd als het zowel elektriciteit als een andere brandstof gebruikt.

    Met de selectieopties kun je de grafiek aanpassen aan de specifieke brandstoffen. 

    """

    # Plaats de introductietekst in de Streamlit-app
    st.markdown(intro_text)


# In[ ]:


with tab4:
    # Sorteer de resultaten op basis van het aantal voertuigen in aflopende volgorde
    merken = merken.sort_values(by="Aantal auto's", ascending=False)

    # Haal de beschikbare brandstofcategorieën op
    available_fuels = merken['Brandstof omschrijving'].unique()

    # Definieer kleuren voor elke brandstofcategorie
    fuel_colors = {
        'Benzine': 'rgb(141,211,199)',
        'Diesel': 'rgb(190,186,218)',
        'Elektriciteit': 'rgb(251,128,114)',
        'Hybride': 'rgb(128,177,211)',
        # Voeg hier meer brandstofcategorieën en kleuren toe indien nodig
    }

    # Multiselect-widget voor brandstofcategorieën
    selected_fuels = st.multiselect('Selecteer brandstofcategorieën', available_fuels, default=available_fuels)

    # Filter de resultaten op basis van de geselecteerde brandstofcategorieën en bijbehorende kleuren
    filtered_result = merken[merken['Brandstof omschrijving'].isin(selected_fuels)]
    filtered_result['Brandstof kleur'] = filtered_result['Brandstof omschrijving'].map(fuel_colors)

    # Selecteer de top 10 merken
    top_10_merken = filtered_result.groupby('Merk')["Aantal auto's"].sum().nlargest(10).index
    filtered_result = filtered_result[filtered_result['Merk'].isin(top_10_merken)]

    # Maak de barplot met Plotly Express
    fig = px.bar(filtered_result, x='Merk', y="Aantal auto's", color='Brandstof omschrijving', 
                 title=f'Top 10 populairste automerken', color_discrete_map=fuel_colors)

    # Stel de modus van de balken in op 'group' voor naast elkaar geplaatste balken
    fig.update_layout(barmode='group')

    # Toon de plot met Streamlit
    st.plotly_chart(fig)


# In[ ]:


with tab4:
    # Streamlit UI
    st.title("Aantal auto's per brandstof omschrijving")

    # Introductietekst voor deze specifieke plot
    intro_text = "Bekijk hieronder de visualisatie van het aantal auto's per brandstofomschrijving over de jaren. Met het dropdown menu kan de verschillende weergave types laten zien worden. Hierbij kan er gekeken worden naar de opties 'Aantal', 'Cumulatief' en 'Relatief cumulatief'. Bij de optie 'Aantal' wordt er gekeken naar het aantal auto's per jaar. Bij de optie 'Cumulatief' wordt er gekeken naar het cumulatieve aantal auto's per jaar. Hierbij worden de aantal auto's elk jaar opgeteld om te zien hoe het verloop over de jaren heen is. Bij de optie 'Relatief cumulatief' wordt er gekeken naar de relaieve cijfers. "

    st.write(intro_text)


# In[ ]:


with tab4:
    # Definieer kleuren voor elke brandstofcategorie
    fuel_colors = {
        'Benzine': 'rgb(141,211,199)',
        'Diesel': 'rgb(190,186,218)',
        'Elektriciteit': 'rgb(251,128,114)',
        'Hybride': 'rgb(128,177,211)',
        # Voeg hier meer brandstofcategorieën en kleuren toe indien nodig
    }

    # Dropdown-menu voor het selecteren van het weergavetype
    display_type = st.selectbox('Weergavetype', ['Aantal', 'Cumulatief', 'Relatief Cumulatief'])

    if display_type == 'Aantal':
        # Maak een cumulatief lijndiagram voor alle brandstofcategorieën met Plotly
        fig = px.line(cumulatief, x='Bouwjaar', y="Aantal auto's", color='Brandstof omschrijving', color_discrete_map=fuel_colors, title="Aantal auto's per brandstof omschrijving")

    elif display_type == 'Cumulatief':
        # Maak een cumulatief lijndiagram voor alle brandstofcategorieën met Plotly
        fig = px.line(cumulatief, x='Bouwjaar', y="Aantal auto's cumulatief", color='Brandstof omschrijving', color_discrete_map=fuel_colors, title="Aantal auto's per brandstof omschrijving cumulatief")

    elif display_type == 'Relatief Cumulatief':
      # Maak een lijndiagram voor relatief cumulatieve gegevens voor alle brandstofcategorieën met Plotly
        fig = px.line(cumulatief, x='Bouwjaar', y='Relatief Cumulatief', color='Brandstof omschrijving', color_discrete_map=fuel_colors, title="Aantal auto's per brandstof omschrijving relatief cumulatief")

    # Voeg stippen toe op de meetpunten
    fig.update_traces(mode='markers+lines', marker=dict(size=5), line=dict(shape='linear'))

    # Configureer de legenda om brandstoffen in- en uit te schakelen (showlegend=True)
    fig.update_layout(showlegend=True)

    # Toon de plot met Streamlit
    st.plotly_chart(fig)


# In[ ]:


with tab4:
    # Streamlit-app titel
    st.title("Voorspelling aantal auto's in 2023")

    # Introductietekst
    introductietekst = """
    In onderstaande grafiek zijn het aantal hybride en elektrische auto's voorspelt in de jaren 2023 tm 2030. Bij de voorspelling is onder andere de informatie van voorgaande jaren gebruikt. Daarnaast is voor de voorspelling ook het aantal laadpalen in voorgaande jaren gebruikt. Er is voorspelt op basis van een lineair regressie model. De voorspelling is getoond in een donkere kleur en de informatie over het aantal auto's in de voorgaande jaren is aangegeven in een lichtere kleur. 
    """

    st.markdown(introductietekst)


# In[ ]:


with tab4:
    voorspelling = pd.read_csv("voorspelling.csv")


#     diesel = voorspelling[(voorspelling['Brandstof omschrijving'] == 'Diesel') & (voorspelling['Bouwjaar'] > 2018)]
#     benzine = voorspelling[(voorspelling['Brandstof omschrijving'] == 'Benzine') & (voorspelling['Bouwjaar'] > 2018)]
    hybride = voorspelling[(voorspelling['Brandstof omschrijving'] == 'Hybride') & (voorspelling['Bouwjaar'] >= 2018)]
    elektriciteit = voorspelling[(voorspelling['Brandstof omschrijving'] == 'Elektriciteit') & (voorspelling['Bouwjaar'] >= 2018)]

    # Voorbeeldgegevens
    x = elektriciteit['Bouwjaar'].tolist()
#     diesel = diesel["Aantal auto's"].tolist()
#     benzine = benzine["Aantal auto's"].tolist()
    hybride = hybride["Aantal auto's"].tolist()
    elektriciteit = elektriciteit["Aantal auto's"].tolist()

    # Bepaal de drempelwaarde voor de x-as
    drempelwaarde_x = 2022  # Pas deze waarde aan

    # Maak een lijst van kleuren op basis van de x-waarde voor de sinuslijn
#     colors_diesel = ['blue' if xi <= drempelwaarde_x else 'red' for xi in x]
#     colors_benzine = ['green' if xi <= drempelwaarde_x else 'red' for xi in x]
    colors_hybride = ['yellow' if xi <= drempelwaarde_x else 'red' for xi in x]
    colors_elektriciteit = ['pink' if xi <= drempelwaarde_x else 'red' for xi in x]

    # Maak een Plotly figuur
    fig = go.Figure()

    # Voeg een lijntrace toe voor de sinuslijn met kleurverandering
#     for i in range(1, len(x)):
#         show_legend = i == 1  # Alleen de eerste trace voor de sinuslijn wordt in de legenda weergegeven
#         if x[i] > drempelwaarde_x:
#             fig.add_trace(go.Scatter(x=[x[i - 1], x[i]], y=[diesel[i - 1], diesel[i]], mode='lines', line=dict(color='rgb(190,186,218)', width=2), showlegend=show_legend, name='Diesel'))
#         else:
#             fig.add_trace(go.Scatter(x=[x[i - 1], x[i]], y=[diesel[i - 1], diesel[i]], mode='lines', line=dict(color='rgba(190,186,218,0.3)', width=2), showlegend=show_legend, name='Diesel'))

#     for i in range(1, len(x)):
#         show_legend = i == 1  # Alleen de eerste trace voor de sinuslijn wordt in de legenda weergegeven
#         if x[i] > drempelwaarde_x:
#             fig.add_trace(go.Scatter(x=[x[i - 1], x[i]], y=[benzine[i - 1], benzine[i]], mode='lines', line=dict(color='rgb(141,211,199)', width=2), showlegend=show_legend, name='Benzine'))
#         else:
#             fig.add_trace(go.Scatter(x=[x[i - 1], x[i]], y=[benzine[i - 1], benzine[i]], mode='lines', line=dict(color='rgba(141,211,199,0.3)', width=2), showlegend=show_legend, name='Benzine'))

    for i in range(1, len(x)):
        show_legend = i == 1  # Alleen de eerste trace voor de sinuslijn wordt in de legenda weergegeven
        if x[i] > drempelwaarde_x:
            fig.add_trace(go.Scatter(x=[x[i - 1], x[i]], y=[hybride[i - 1], hybride[i]], mode='lines', line=dict(color='rgb(128,177,211)', width=2), showlegend=show_legend, name='Hybride'))
        else:
            fig.add_trace(go.Scatter(x=[x[i - 1], x[i]], y=[hybride[i - 1], hybride[i]], mode='lines', line=dict(color='rgba(128,177,211,0.3)', width=2), showlegend=show_legend, name='Hybride'))


    for i in range(1, len(x)):
        show_legend = i == 1  # Alleen de eerste trace voor de sinuslijn wordt in de legenda weergegeven
        if x[i] > drempelwaarde_x:
            fig.add_trace(go.Scatter(x=[x[i - 1], x[i]], y=[elektriciteit[i - 1], elektriciteit[i]], mode='lines', line=dict(color='rgb(251,128,114)', width=2), showlegend=show_legend, name='Elektriciteit'))
        else:
            fig.add_trace(go.Scatter(x=[x[i - 1], x[i]], y=[elektriciteit[i - 1], elektriciteit[i]], mode='lines', line=dict(color='rgba(251,128,114,0.3)', width=2), showlegend=show_legend, name='Elektriciteit'))


    # Pas de lay-out van het figuur aan
    fig.update_layout(
        xaxis_title='Jaar',
        yaxis_title="Aantal auto's",
        title="Voorspellingen per brandstofcategorie voor 2023"
    )

    # Toon het Plotly-figuur
    st.plotly_chart(fig)
    
    fig.show()

