#!/usr/bin/env python
# coding: utf-8

# In[19]:


# pip install streamlit-folium


# In[20]:


import pandas as pd
import plotly.express as px
import streamlit as st
import requests
import plotly.graph_objects as go
import matplotlib.pyplot as plt
# import ipywidgets as widgets
from ipywidgets import interact
from IPython.display import display
import folium
from streamlit_folium import folium_static


# In[21]:


tab1, tab2, tab3, tab4 = st.tabs(["Introductie", "API laadpalen", "Laadpalen dataset", "RDW datasets"])


# In[22]:


with tab1:
    ###Inladen API - kijk naar country code en maxresults
    response = requests.get("https://api.openchargemap.io/v3/poi/?output=json&countrycode=NL&maxresults=8000&verbose=false&key=93b912b5-9d70-4b1f-960b-fb80a4c9c017")


# In[23]:


with tab1:
    responsejson  = response.json()

    ###Dataframe bevat kolom die een list zijn. 
    #Met json_normalize zet je de eerste kolom om naar losse kolommen
    Laadpalen = pd.json_normalize(responsejson)
    #Daarna nog handmatig kijken welke kolommen over zijn in dit geval Connections
    #Kijken naar eerst laadpaal op de locatie
    #Kan je uitpakken middels:
    df4 = pd.json_normalize(Laadpalen.Connections)
    df5 = pd.json_normalize(df4[0])
    df5.head()
    ###Bestanden samenvoegen
    Laadpalen = pd.concat([Laadpalen, df5], axis=1)


# In[24]:


with tab1:
    Laadpalen['Type Laadpaal'] = Laadpalen['CurrentTypeID']
    Laadpalen['Snelladen'] = Laadpalen['Level.IsFastChargeCapable']
    Laadpalen['Niveau Laadpaal'] = Laadpalen['LevelID']


# In[25]:


with tab1:

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
            return 'RGB(141,211,199)' 
        if type == 2.0:
            return 'cyan'
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
            for type_value, color in [('AC (Single-Phase)', 'pink'), ('AC (Three-Phase)', 'RGB(255,255,179)'), ('DC', 'RGB(128,177,211)'), ('Onbekend', 'grey')]:
                legend_html += f'<p><i style="background:{color}; border-radius:50%; width: 20px; height: 20px; display:inline-block;"></i> {type_value}</p>'
        elif selected_variable == 'Snelladen':
            for type_value, color in [('Snelladen', 'red'), ('Niet snelladen', 'RGB(128,177,211)'), ('Onbekend', 'grey')]:
                legend_html += f'<p><i style="background:{color}; border-radius:50%; width: 20px; height: 20px; display:inline-block;"></i> {type_value}</p>'    
            # Voeg legenda voor LevelID toe
        elif selected_variable == 'Niveau Laadpaal':
            for type_value, color in [('Niveau 1 : Laag (Onder 2kW)', 'red'), ('Niveau 2 : Medium (Tussen 2kW en 40kW)', 'cyan'), ('Niveau 3:  Hoog (Meer dan 40kW)', 'purple'), ('Onbekend', 'grey')]:
                legend_html += f'<p><i style="background:{color}; border-radius:50%; width: 20px; height: 20px; display:inline-block;"></i> {type_value}</p>'
        # Voeg legenda voor andere variabelen toe zoals nodig
        legend_html += "</div>"

        return legend_html

    # Streamlit-frontend
    st.title('Laadpalen Kaart')
    st.write('Hier is een interactieve kaart met laadpalen.')
    
    regio = st.selectbox('Selecteer een regio', ['Nederland', 'Amsterdam', 'Rotterdam', 'Utrecht', 'Groningen', 'Leeuwarden', 'Assen', 'Arnhem', 'Zwolle', "'s-Hertogenbosch", 'Middelburg', 'Maastricht'])
    variable = st.selectbox('Selecteer een variable', ['Type Laadpaal', 'Snelladen', 'Niveau Laadpaal'])
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


# In[26]:


merken = pd.read_csv("merken.csv")
cumulatief = pd.read_csv("cumulatief.csv")


# In[27]:


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


# In[28]:


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


# In[29]:


with tab4:
    # Streamlit UI
    st.title("Aantal auto's per brandstof omschrijving")

    # Introductietekst voor deze specifieke plot
    intro_text = "Bekijk hieronder de visualisatie van het aantal auto's per brandstofomschrijving over de jaren. Met het dropdown menu kan de verschillende weergave types laten zien worden. Hierbij kan er gekeken worden naar de opties 'Aantal', 'Cumulatief' en 'Relatief cumulatief'. Bij de optie 'Aantal' wordt er gekeken naar het aantal auto's per jaar. Bij de optie 'Cumulatief' wordt er gekeken naar het cumulatieve aantal auto's per jaar. Hierbij worden de aantal auto's elk jaar opgeteld om te zien hoe het verloop over de jaren heen is. Bij de optie 'Relatief cumulatief' wordt er gekeken naar de relaieve cijfers. "

    st.write(intro_text)


# In[30]:


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
        # Voeg een cumulatieve somkolom toe
        cumulatief["Aantal auto's cumulatief"] = cumulatief.groupby('Brandstof omschrijving')["Aantal auto's"].cumsum()

        # Maak een cumulatief lijndiagram voor alle brandstofcategorieën met Plotly
        fig = px.line(cumulatief, x='Bouwjaar', y="Aantal auto's cumulatief", color='Brandstof omschrijving', color_discrete_map=fuel_colors, title="Aantal auto's per brandstof omschrijving cumulatief")

    elif display_type == 'Relatief Cumulatief':
        # Voeg een cumulatieve somkolom toe
        cumulatief["Aantal auto's cumulatief"] = cumulatief.groupby('Brandstof omschrijving')["Aantal auto's"].cumsum()

        # Bereken de relatief cumulatieve waarden (percentage van de totale cumulatieve waarde)
        cumulatief['Relatief Cumulatief'] = cumulatief.groupby('Brandstof omschrijving')["Aantal auto's cumulatief"].transform(lambda x: x / x.max() * 100)

        # Maak een lijndiagram voor relatief cumulatieve gegevens voor alle brandstofcategorieën met Plotly
        fig = px.line(cumulatief, x='Bouwjaar', y='Relatief Cumulatief', color='Brandstof omschrijving', color_discrete_map=fuel_colors, title="Aantal auto's per brandstof omschrijving relatief cumulatief")

    # Voeg stippen toe op de meetpunten
    fig.update_traces(mode='markers+lines', marker=dict(size=5), line=dict(shape='linear'))

    # Configureer de legenda om brandstoffen in- en uit te schakelen (showlegend=True)
    fig.update_layout(showlegend=True)

    # Toon de plot met Streamlit
    st.plotly_chart(fig)


# In[31]:


with tab4:
    # Streamlit-app titel
    st.title("Voorspelling aantal auto's in 2023")

    # Introductietekst
    introductietekst = """
    Verken onze visualisatie van de voorspelde aantallen voertuigen voor het jaar 2023, gespecificeerd per brandstofcategorie. Deze grafiek biedt inzicht in de toekomstige ontwikkelingen van voertuigaantallen en helpt bij het begrijpen van de verwachte veranderingen op basis van historische gegevens en voorspellingsmodellen. Ontdek hoe benzine, diesel, elektriciteit en hybride voertuigen zich naar verwachting zullen ontwikkelen in het komende jaar. Deze grafiek is gebaseerd op nauwkeurige voorspellingen en biedt een overzicht van wat we kunnen verwachten in de autosector in 2023.
    """

    st.markdown(introductietekst)


# In[34]:


with tab4:
    voorspelling = pd.read_csv("voorspelling.csv")
    import plotly.graph_objects as go
    import numpy as np

    diesel = voorspelling[(voorspelling['Brandstof omschrijving'] == 'Diesel') & (voorspelling['Bouwjaar'] > 2018)]
    benzine = voorspelling[(voorspelling['Brandstof omschrijving'] == 'Benzine') & (voorspelling['Bouwjaar'] > 2018)]
    hybride = voorspelling[(voorspelling['Brandstof omschrijving'] == 'Hybride') & (voorspelling['Bouwjaar'] > 2018)]
    elektriciteit = voorspelling[(voorspelling['Brandstof omschrijving'] == 'Elektriciteit') & (voorspelling['Bouwjaar'] > 2018)]

    # Voorbeeldgegevens
    x = diesel['Bouwjaar'].tolist()
    diesel = diesel["Aantal auto's"].tolist()
    benzine = benzine["Aantal auto's"].tolist()
    hybride = hybride["Aantal auto's"].tolist()
    elektriciteit = elektriciteit["Aantal auto's"].tolist()

    # Bepaal de drempelwaarde voor de x-as
    drempelwaarde_x = 2022  # Pas deze waarde aan

    # Maak een lijst van kleuren op basis van de x-waarde voor de sinuslijn
    colors_diesel = ['blue' if xi <= drempelwaarde_x else 'red' for xi in x]
    colors_benzine = ['green' if xi <= drempelwaarde_x else 'red' for xi in x]
    colors_hybride = ['yellow' if xi <= drempelwaarde_x else 'red' for xi in x]
    colors_elektriciteit = ['pink' if xi <= drempelwaarde_x else 'red' for xi in x]

    # Maak een Plotly figuur
    fig = go.Figure()

    # Voeg een lijntrace toe voor de sinuslijn met kleurverandering
    for i in range(1, len(x)):
        show_legend = i == 1  # Alleen de eerste trace voor de sinuslijn wordt in de legenda weergegeven
        if x[i] > drempelwaarde_x:
            fig.add_trace(go.Scatter(x=[x[i - 1], x[i]], y=[diesel[i - 1], diesel[i]], mode='lines', line=dict(color='rgb(190,186,218)', width=2), showlegend=show_legend, name='Diesel'))
        else:
            fig.add_trace(go.Scatter(x=[x[i - 1], x[i]], y=[diesel[i - 1], diesel[i]], mode='lines', line=dict(color='rgba(190,186,218,0.3)', width=2), showlegend=show_legend, name='Diesel'))

    for i in range(1, len(x)):
        show_legend = i == 1  # Alleen de eerste trace voor de sinuslijn wordt in de legenda weergegeven
        if x[i] > drempelwaarde_x:
            fig.add_trace(go.Scatter(x=[x[i - 1], x[i]], y=[benzine[i - 1], benzine[i]], mode='lines', line=dict(color='rgb(141,211,199)', width=2), showlegend=show_legend, name='Benzine'))
        else:
            fig.add_trace(go.Scatter(x=[x[i - 1], x[i]], y=[benzine[i - 1], benzine[i]], mode='lines', line=dict(color='rgba(141,211,199,0.3)', width=2), showlegend=show_legend, name='Benzine'))

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


# In[ ]:




