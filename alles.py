#!/usr/bin/env python
# coding: utf-8

# In[36]:


# pip install streamlit-folium


# In[37]:


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


# In[38]:


tab1, tab2, tab3, tab4 = st.tabs(["Introductie", "API laadpalen", "Laadpalen dataset", "RDW datasets"])


# In[40]:


with tab1:
    Laadpalen = pd.read_csv("Laadpalen.csv")


# In[41]:


with tab1:
    Laadpalen['Type Laadpaal'] = Laadpalen['CurrentTypeID']
    Laadpalen['Snelladen'] = Laadpalen['Level.IsFastChargeCapable']
    Laadpalen['Niveau Laadpaal'] = Laadpalen['LevelID']


# In[42]:


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


# In[ ]:


with tab2:


    st.title("Kaart met bezetting per Laadpaal")
    # streamlit een titel geven
    
    # Folium map toevoegen aan streamlit.
    st.write('Om inzicht te krijgen in niet alleen de plek van de laadpaal, maar ook de bezetting per',
            'laadpaal is de volgende kaart gemaakt. Op deze kaart is elke kaart uit de dataset te zien.',
            'De grote van de cirkel bepaald hoe hoog de bezetting is; hoe groter de',
            'circkel hoe hoger de bezetting van die laadpaal. Om de specifieke bezetting te achterhalen',
            'is het mogelijk om op een bubbel te klikken en de bezetting als getal te zien.',
            'De kleur van de cirkel bepaald in welke provincie de paal zich bevindt. In totaal',
            'worden 1000 Laadpalen als voorbeeld gebruikt. Deze limitatie heeft te maken met de',
            'snelheid en performace van de applicatie.')

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

    st_map = st_folium(m, width=700)
  
    # Uitleg over de kaart.


# In[52]:


with tab3:
    import pandas as pd
    import streamlit as st
    import plotly.express as px
    import numpy as np
    import plotly.graph_objects as go
#     import seaborn as sns
    import matplotlib.pyplot as plt
    from plotly.subplots import make_subplots
    import math
    import plotly.figure_factory as ff

    df = pd.read_csv("laadpaaldata.csv")
    df['TimeNotCharging']=df['ConnectedTime']- df['ChargeTime']


    df['TimeNotCharging'] = df['TimeNotCharging'].apply(lambda x: np.nan if x < 0 else x)

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




    st.write("""
        in het onderstaande dropdown menu zijn histogrammen van verschillende variabelen te vinden.
        Met de sliders kunnen de ongewenste waardes weggefilterd worden verder kan ook het aantal bins worden veranderd.
    """)


    # haal negative laad tijden weg
    df['ChargeTime'] = df['ChargeTime'].apply(lambda x: np.nan if x < 0 else x)
    df.dropna(inplace=True)

    df2 = df[['TotalEnergy', 'ConnectedTime', 'ChargeTime', 'MaxPower', 'TimeNotCharging']]

    df2.dropna(inplace=True)

    # Voeg een dropdown-menu toe voor het selecteren van een variabele
    selected_variable = st.selectbox("Selecteer een variabele", df2.columns)

    # Veronderstel dat je ook een slider hebt voor het instellen van het bereik voor de geselecteerde variabele
    range_variable = st.slider(f"Bereik van {selected_variable}", min_value=df2[selected_variable].min(), max_value=df2[selected_variable].max(), value=(df2[selected_variable].min(), df2[selected_variable].max()))

    # Voeg een slider toe voor het aantal bins
    num_bins = st.slider("Aantal bins", min_value=1, max_value=20, value=20)

    # Bereken het aantal bins op basis van het huidige bereik en de sliderwaarde
    bin_width = (range_variable[1] - range_variable[0]) / num_bins

    # Filter de gegevens op basis van het geselecteerde bereik en variabele
    filtered_df = df2[(df2[selected_variable] >= range_variable[0]) & (df2[selected_variable] <= range_variable[1])]

    # Maak een ECDF-plot voor de gefilterde gegevens met Plotly Express
    fig = px.histogram(filtered_df, x=selected_variable, nbins=num_bins)

    fig.update_xaxes(title=selected_variable)

    fig.update_yaxes(title='Frequentie')

    fig.update_layout(bargap=0.05)

    # text
    if selected_variable == 'TotalEnergy':
        st.write("""
        In de onderstaande histogram wordt het totale energieverbruik weergegeven. 
        Wat opvallend is, is dat na het bereiken van 12 kWh het stroomverbruik bijna nihil wordt. 
        Dit fenomeen kan worden toegeschreven aan het feit dat de meeste auto's op dat moment niet langer zijn aangesloten op het laadstation of voledig zijn opgeladen. 
        Er zijn echter ook uitschieters naar boven, wat wordt veroorzaakt doordat sommige auto's volledig of bijna volledig leeg zijn wanneer ze aan het laadstation worden aangesloten. 
        Het hoogste gemeten waarde ligt rond de 83 kWh, wat nog steeds haalbaar is met de huidige stand van de accutechnologie.
    """)

    if selected_variable == 'ConnectedTime':
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

    if selected_variable == 'ChargeTime':
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

    if selected_variable == 'MaxPower':
        st.write("""
        In de onderstaande histogram is de frequentie te zien over het maximaal gevraagde vermogen per laadpaal. Wat als eerste opvalt
        is dat de variabelen veel verspreid zijn. Sommige waardes liggen dichtbij de nul en andere waadres liggen rond de twintig-duizend.
        Als de histogram wat verkleint wordt, is er al snel zichtbaar dat de meeste Maxpower tussen de drieduizend en vierduizend ligt.
        Dit kan twee redenen hebben; de eerste reden is dat de auto niet meer aankan dan tussen de drie en vierduizend watt. Dit zou betekenen
        dat de meeste auto's drie tot vierduizend watt per seconde kunnen opnemen. De tweede reden is dat de machine of de paal niet meer
        stroom kan leveren. Dit zou betekenen dat meeste machine niet meer watt per seconde kunnen lerveren, dan tussen drie en vierduizend watt.
    """)

    if selected_variable == 'TimeNotCharging':
        st.write("""
            In het onderstaande histogram wordt de tijd weergegeven dat auto's weliswaar nog verbonden zijn met het laadstation, maar niet meer aan het laden zijn. 
            Dit duidt erop dat de voertuigen volledig zijn opgeladen en dus onnodig de laadpaal bezet houden, wat ongewenst is omwille van 
            efficiëntie en beschikbaarheid voor andere gebruikers.
            Het is ook mogelijk dat de laadpaal op dat moment geen stroom kon leveren om een of andere reden, zoals een tijdelijke storing, 
            overbelasting van het laadnetwerk, of andere technische problemen. Dit kan leiden tot het langer verbonden blijven van de auto's zonder daadwerkelijk laden.
            Het is belangrijk om deze situaties te monitoren en aan te pakken om een effectief gebruik van de laadinfrastructuur te 
            waarborgen en de beschikbaarheid van laadpalen te maximaliseren voor alle gebruikers van elektrische voertuigen.
            mocht dit niet het geval zijn en er zijn veel mensen die de auto onnodig lang verbonden laten dan kan er worden geken om het vermogen 
            te verlagen zodat er minder belasting is op het elektriciteits net. 
            Dit kan onder andere worden bereikt door middel van slimme laadsystemen die de laadtijd automatisch beperken zodra een voertuig volledig is 
            opgeladen en door regelmatig onderhoud van laadpalen om technische storingen te minimaliseren.
    """)


    # Toon de plot
    st.plotly_chart(fig)



    # text

    st.title('kansverdeling laadtijden')

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

    fig = ff.create_distplot(hist_data, group_labels, show_rug= False)




    # Voeg lijnen toe voor het gemiddelde en de mediaan aan subplot 1
    fig.add_shape(
        type='line',
        x0=gemiddelde,
        x1=gemiddelde,
        y0=0,
        y1=1,
        xref='x',
        yref='paper',
        line=dict(color='red', dash='dash')
    )

    fig.add_shape(
        type='line',
        x0=mediaan,
        x1=mediaan,
        y0=0,
        y1=1,
        xref='x',
        yref='paper',
        line=dict(color='orange', dash='solid')
    )


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

    # Selecteer de numerieke kolommen voor correlatieanalyse

    numerical_columns = ['TotalEnergy', 'ConnectedTime', 'ChargeTime', 'MaxPower', 'TimeNotCharging']


    # Bereken de correlatiematrix

    correlation_matrix = df[numerical_columns].corr()


    fig1 = go.Figure(data=go.Heatmap(

                       z=correlation_matrix.values,

                       x=numerical_columns,

                       y=numerical_columns,

                       colorscale='Blues',

                       zmin=0, zmax=1,
                       text=correlation_matrix.values, 
                       hoverongaps=True))


    fig1.update_xaxes(tickangle=90)

    # text

    st.title('Correlatie Analyse')

    st.write("""
        Als we naar de onderstaande correlatiematrix kijken zien we een aantal interessante patronen:
        1. Totale energie en piekstroom vertonen een sterke correlatie. Dit is logisch omdat totale energie wordt uitgedrukt in wattuur (Wh),
        wat het product is van piekstroom (in watt) en laadtijd (in uur). 
        Met andere woorden, de totale energie die wordt verbruikt, is direct gerelateerd aan zowel de hoogste stroomsterkte als de duur van het laden.
        2. Verder zien we dat totale energie en laadtijd ook een sterke correlatie hebben. Dit komt omdat, zoals eerder vermeld, 
        de totale energie wordt bepaald door de hoeveelheid stroom (piekstroom) vermenigvuldigd met de tijd dat het laden plaatsvindt. 
        Dit bevestigt het verband tussen de totale energieconsumptie en de tijd die wordt besteed aan het laden.
        3. Connectietijd vertoont een sterke correlatie met niet-laadtijd. 
        Dit is begrijpelijk omdat wanneer een voertuig gedurende langere perioden is verbonden met het laadstation (connectietijd), 
        er een grotere kans is dat er tijdsperiodes zijn waarin het voertuig niet actief wordt opgeladen. Het omgekeerde geldt ook: 
        als er meer niet-laadtijd is, kan dit wijzen op langere periodes waarin het voertuig is verbonden, maar niet actief wordt geladen.
        4. Er is ook een sterke correlatie tussen laadtijd en totale energie. 
        Dit komt doordat er een maximale hoeveelheid energie is die een elektrisch voertuig kan opnemen, 
        en daarom zal een groter totaal energieverbruik (Wh) meer tijd (uren) vereisen om te worden geleverd.
        5. Ten slotte zien we een sterke correlatie tussen maximale stroom en totale energie.
        Dit is begrijpelijk omdat een hogere piekstroom het mogelijk maakt om een grotere hoeveelheid energie in een kortere tijd te leveren, 
        wat resulteert in een hoger totaal energieverbruik.
        Deze inzichten benadrukken de onderlinge relaties tussen verschillende variabelen in de context van elektrische voertuiglading, 
        wat nuttig kan zijn voor het begrijpen en optimaliseren van laadprocessen. 
    """)

    # Toon het bar plot in Streamlit

    st.plotly_chart(fig1)


# In[43]:


merken = pd.read_csv("merken.csv")
cumulatief = pd.read_csv("cumulatief.csv")


# In[44]:


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


# In[45]:


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


# In[46]:


with tab4:
    # Streamlit UI
    st.title("Aantal auto's per brandstof omschrijving")

    # Introductietekst voor deze specifieke plot
    intro_text = "Bekijk hieronder de visualisatie van het aantal auto's per brandstofomschrijving over de jaren. Met het dropdown menu kan de verschillende weergave types laten zien worden. Hierbij kan er gekeken worden naar de opties 'Aantal', 'Cumulatief' en 'Relatief cumulatief'. Bij de optie 'Aantal' wordt er gekeken naar het aantal auto's per jaar. Bij de optie 'Cumulatief' wordt er gekeken naar het cumulatieve aantal auto's per jaar. Hierbij worden de aantal auto's elk jaar opgeteld om te zien hoe het verloop over de jaren heen is. Bij de optie 'Relatief cumulatief' wordt er gekeken naar de relaieve cijfers. "

    st.write(intro_text)


# In[47]:


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


# In[48]:


with tab4:
    # Streamlit-app titel
    st.title("Voorspelling aantal auto's in 2023")

    # Introductietekst
    introductietekst = """
    Verken onze visualisatie van de voorspelde aantallen voertuigen voor het jaar 2023, gespecificeerd per brandstofcategorie. Deze grafiek biedt inzicht in de toekomstige ontwikkelingen van voertuigaantallen en helpt bij het begrijpen van de verwachte veranderingen op basis van historische gegevens en voorspellingsmodellen. Ontdek hoe benzine, diesel, elektriciteit en hybride voertuigen zich naar verwachting zullen ontwikkelen in het komende jaar. Deze grafiek is gebaseerd op nauwkeurige voorspellingen en biedt een overzicht van wat we kunnen verwachten in de autosector in 2023.
    """

    st.markdown(introductietekst)


# In[50]:


with tab4:
    voorspelling = pd.read_csv("voorspelling.csv")
    import plotly.graph_objects as go
    import numpy as np

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


# In[ ]:





# In[ ]:





# In[ ]:




