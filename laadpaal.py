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


with tab3:

    df = pd.read_csv("laadpaaldata.csv")
    df['Niet oplaadtijd']=df['ConnectedTime']- df['ChargeTime']


    df['Niet oplaadtijd'] = df['Niet oplaadtijd'].apply(lambda x: np.nan if x < 0 else x)

    df.dropna()


    # in regel 1731 en 1732 zit een datum van 29 februarie 2018. 2018 is geen schrikkel jaar dus deze rerel kunnen we niet verstouwen

    df['Ended'] = pd.to_datetime(df['Ended'], errors='coerce')
    df['Started'] = pd.to_datetime(df['Started'], errors='coerce')
    df.dropna(inplace=True)

    # op het einde van de dataset gaat de tellen niet door naar 2019 nu wel
    df['Started'] = pd.to_datetime(df['Started'])
    df['Ended'] = pd.to_datetime(df['Ended'])

    # Voeg een jaar toe aan 'Ended' wanneer 'Ended' kleiner is dan 'Started'
    mask = df['Ended'] < df['Started']
    df.loc[mask, 'Ended'] += pd.DateOffset(years=1)


    st.title("Histogram variabele laadpalen")

    st.write("""
        In het onderstaande dropdown menu zijn histogrammen van verschillende variabelen te vinden.
        Met de sliders kunnen de ongewenste waardes weggefilterd worden verder kan ook het aantal bins worden veranderd.
    """)


    # haal negative laad tijden weg
    df['ChargeTime'] = df['ChargeTime'].apply(lambda x: np.nan if x < 0 else x)
    df.dropna(inplace=True)
    df['Totaal Energie'] = df['TotalEnergy']
    df['Verbindingstijd'] = df['ConnectedTime']
    df['Oplaadtijd'] = df['ChargeTime']
    df['Maximaal Vermogen'] = df['MaxPower']
    
    df2 = df[['Totaal Energie', 'Verbindingstijd', 'Oplaadtijd', 'Maximaal Vermogen', 'Niet oplaadtijd']]

    df2.dropna(inplace=True)

    
    # Voeg een dropdown-menu toe voor het selecteren van een variabele
    selected_variable = st.selectbox("Selecteer een variabele", df2.columns)



    # text
    if selected_variable == 'Totaal Energie':

        st.write("""
        In de onderstaande histogram wordt het totale energieverbruik weergegeven. 
        Wat opvallend is, is dat na het bereiken van 12 kWh het stroomverbruik bijna nihil wordt. 
        Dit fenomeen kan worden toegeschreven aan het feit dat de meeste auto's op dat moment niet langer zijn aangesloten op het laadstation of voledig zijn opgeladen. 
        Er zijn echter ook uitschieters naar boven, wat wordt veroorzaakt doordat sommige auto's volledig of bijna volledig leeg zijn wanneer ze aan het laadstation worden aangesloten. 
        Het hoogste gemeten waarde ligt rond de 83 kWh, wat nog steeds haalbaar is met de huidige stand van de accutechnologie.
    """)

    if selected_variable == 'Verbindingstijd':

        st.write("""
        In de onderstaande histogram wordt de verbindingsduur weergegeven. Opvallend is dat er na 5 uur een daling te zien is. 
        Dit kan te wijten zijn aan mensen die ergens op bezoek zijn of aan het werk zijn en hun elektrische voertuigen gedurende die tijd aan het laadstation hebben aangesloten.
        Het overgrote deel van de verbindingen duurt minder dan 15 uur, 
        wat logisch is omdat de meeste voertuigen tegen die tijd volledig zijn opgeladen en de eigenaren vaak weer moeten vertrekken.
        Verder valt op dat er een uitschieter is met een duur van meer dan 167 uur. 
        Dit kan het gevolg zijn van een situatie waarin iemand op woensdag 21 februari is aangekomen en pas volgende woensdag is vertrokken, 
        waarbij de auto gedurende die hele periode maar liefst 163 uur niet aan het laden was.
        Bovendien is het interessant om te zien dat de voertuigen die bij deze laadstations worden opgeladen, regelmatig worden gebruikt, 
        aangezien de verbindingsduur niet constant hoog is, 
        wat suggereert dat de eigenaren hun auto's regelmatig inzetten. Dit kan wijzen op een actieve en betrokken gemeenschap van elektrische voertuigbezitters.
    """)

    if selected_variable == 'Oplaadtijd':

        st.write("""
            In de onderstaande histogram wordt de laadtijd weergegeven. Wat direct opvalt, is dat deze histogram sterk geconcentreerd is aan de linkerkant, 
            en na ongeveer 4 uur is er een aanzienlijke afname te zien. 
            Dit is waarschijnlijk te wijten aan het feit dat voertuigen op dat moment meestal lading hebben om naar de volgende bestemming te komen of niet 
            meer zijn aangesloten op het laadstation.
            De maximale laadtijd die we in deze gegevens zien is 52 uur, wat betekent dat een auto gedurende 58 uur is verbonden geweest met het laadstation. 
            Interessant is dat er gedurende deze lange periode slechts 11 kWh aan energie is verbruikt. Dit suggereert dat de laadsnelheid extreem langzaam was, 
            en dit komt overeen met een piek vermogen van ongeveer 207 watt gedurende die tijd.
            Een ander opvallend patroon is dat na ongeveer 9 uur laden bijna niemand meer aan het laden is. Dit kan worden verklaard doordat de voertuigen die regelmatig laden, 
            tegen die tijd meestal volledig zijn opgeladen en dus niet langer aan het laadstation zijn aangesloten.
            Deze trend wijst op een efficiënt gebruik van de laadinfrastructuur en suggereert dat voertuigen doorgaans snel worden opgeladen, 
            waardoor de beschikbaarheid van de laadpalen voor andere gebruikers wordt gemaximaliseerd.
        """)

    if selected_variable == 'Maximaal Vermogen':
        st.write("""
        In de onderstaande histogram is de frequentie te zien over het maximaal gevraagde vermogen per laadpaal. Wat als eerste opvalt
        is dat de variabelen veel verspreid zijn. Sommige waardes liggen dichtbij de nul en andere waadres liggen rond de twintig-duizend.
        Als de histogram wat verkleint wordt, is er al snel zichtbaar dat de meeste Maxpower tussen de drieduizend en vierduizend ligt.
        Dit kan twee redenen hebben; de eerste reden is dat de auto niet meer aankan dan tussen de drie en vierduizend watt. Dit zou betekenen
        dat de meeste auto's drie tot vierduizend watt per seconde kunnen opnemen. De tweede reden is dat de machine of de paal niet meer
        stroom kan leveren. Dit zou betekenen dat meeste machine niet meer watt per seconde kunnen lerveren, dan tussen drie en vierduizend watt.
    """)

    if selected_variable == 'Niet oplaadtijd':
        st.write("""
            In het onderstaande histogram wordt de tijd weergegeven dat auto's weliswaar nog verbonden zijn met het laadstation, maar niet meer aan het laden zijn. 
            Dit duidt erop dat de voertuigen volledig zijn opgeladen en dus onnodig de laadpaal bezet houden, wat ongewenst is omwille van 
            efficiëntie en beschikbaarheid voor andere gebruikers.
            Het is ook mogelijk dat de laadpaal op dat moment geen stroom kon leveren om een of andere reden, zoals een tijdelijke storing, 
            overbelasting van het laadnetwerk, of andere technische problemen. Dit kan leiden tot het langer verbonden blijven van de auto's zonder daadwerkelijk laden.
            Het is belangrijk om deze situaties te monitoren en aan te pakken om een effectief gebruik van de laadinfrastructuur te 
            waarborgen en de beschikbaarheid van laadpalen te maximaliseren voor alle gebruikers van elektrische voertuigen.
            Mocht dit niet het geval zijn en er zijn veel mensen die de auto onnodig lang verbonden laten dan kan er worden geken om het vermogen 
            te verlagen zodat er minder belasting is op het elektriciteits net. 
            Dit kan onder andere worden bereikt door middel van slimme laadsystemen die de laadtijd automatisch beperken zodra een voertuig volledig is 
            opgeladen en door regelmatig onderhoud van laadpalen om technische storingen te minimaliseren.
    """)


    # Veronderstel dat je ook een slider hebt voor het instellen van het bereik voor de geselecteerde variabele
    range_variable = st.slider(f"Bereik van {selected_variable}", min_value=df2[selected_variable].min(), max_value=df2[selected_variable].max(), value=(df2[selected_variable].min(), df2[selected_variable].max())
                              ,format="%d")

    # Voeg een slider toe voor het aantal bins
    num_bins = st.slider("Aantal groepen", min_value=1, max_value=20, value=20, format="", step=2)

    # Bereken het aantal bins op basis van het huidige bereik en de sliderwaarde
    bin_width = (range_variable[1] - range_variable[0]) / num_bins

    # Filter de gegevens op basis van het geselecteerde bereik en variabele
    filtered_df = df2[(df2[selected_variable] >= range_variable[0]) & (df2[selected_variable] <= range_variable[1])]

    costum_colors = ['rgb(128,177,211)', 'rgb(128,177,211)', 'rgb(128,177,211)', 'rgb(128,177,211)', 'rgb(128,177,211)']
    # Maak een ECDF-plot voor de gefilterde gegevens met Plotly Express
    fig = px.histogram(filtered_df, x=selected_variable, nbins=num_bins, color_discrete_sequence=costum_colors)

    fig.update_xaxes(title=selected_variable)

    fig.update_yaxes(title='Frequentie')

    fig.update_layout(bargap=0.05, title = f'Histogram {selected_variable}')
    # Toon de plot
    st.plotly_chart(fig)



    
    


# In[ ]:


with tab3:
    # text

    st.title('Kansverdeling laadtijden')

    st.write("""
        In het onderstande figuur is een histogram te zien van de laadtijden. Daarbij worden ook de mediaan, het gemiddelde en de kansverdeling functie weergegeven.
        Met de slider kan worden ingezoomd op de gewilde waardes hierbei zullen de mediaan en het gemiddelde mee veranderen.
    """)

    # Maak een subplots met één rij en twee kolommen
    fig = make_subplots(rows=1, cols=1, subplot_titles=("Histogram", "ECDF"), specs=[[{"secondary_y": True}]])

    # Voeg een double-sided slider toe voor het instellen van een bereik
    range_ChargeTime = st.slider("Bereik van laadtijd", min_value=df['ChargeTime'].min(), max_value=df['ChargeTime'].max(), value=(df['ChargeTime'].min()+0.01, df['ChargeTime'].max()), key="charge_time_range_2")

    # Filter de gegevens op basis van het geselecteerde bereik
    filtered_df_ChargeTime = df[(df['ChargeTime'] >= range_ChargeTime[0]) & (df['ChargeTime'] <= range_ChargeTime[1])]

    gemiddelde = filtered_df_ChargeTime['ChargeTime'].mean()
    mediaan = filtered_df_ChargeTime['ChargeTime'].median()

    # here you can choose your rounding method, I've chosen math.ceil
    bin_width= 1
    nbins1 = math.ceil(((filtered_df_ChargeTime["ChargeTime"].max() - filtered_df_ChargeTime["ChargeTime"].min()) / bin_width))

    # Voeg een histogram toe aan subplot 1
    x = filtered_df_ChargeTime["ChargeTime"]
    hist_data = [x]
    group_labels = ['distplot'] # name of the dataset

    fig = ff.create_distplot(hist_data, group_labels, show_rug= False, histnorm='probability density', colors=['rgba(128,177,211,0.5)'])
    fig['data'][1]['line']['color'] = 'rgb(128,177,211)'  # Kleur van Groep B histogramlijn


    # Voeg lijnen toe voor het gemiddelde en de mediaan aan subplot 1
    fig.add_shape(
        type='line',
        x0=gemiddelde,
        x1=gemiddelde,
        y0=0,
        y1=1,
        xref='x',
        yref='paper',
        line=dict(color='rgb(251,128,114)', dash='dash')
    )

    fig.add_shape(
        type='line',
        x0=mediaan,
        x1=mediaan,
        y0=0,
        y1=1,
        xref='x',
        yref='paper',
        line=dict(color='rgb(188,128,189)', dash='solid')
    )

    fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', line=dict(color='rgb(251,128,114)', dash='dash'), name=f'Gemiddelde: {gemiddelde:.2f}'))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', line=dict(color='rgb(188,128,189)', dash='solid'), name=f'Mediaan: {mediaan:.2f}'))

    # Stel de lay-out van de figuren in
    fig.update_layout(
        title='Histogram en kansverdeling van Laadtijd ',
        xaxis_title='Laadtijd [uur]',
        yaxis_title='Frequentie / CDF',
        legend=dict(x=0.7, y=0.9),
        bargap=0.05
    )



    # Toon de figuren in Streamlit
    st.plotly_chart(fig)

