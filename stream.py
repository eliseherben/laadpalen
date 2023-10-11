import requests
# Importeren van requests om API calls te maken.
import pandas as pd
# Importeren van pandas om dataframes op te zetten.
import folium
# Importeren van folium om kaarten te maken.
import pgeocode
# Importen van pgeocode om informatie op te halen via postcodes.

def color_producer(Provincie):
    """
    Een simpele functies die verderop gebruikt gaat worden
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

response = requests.get("https://api.openchargemap.io/v3/poi/?output=json&countrycode=NL&maxresults=1000&compact=true&verbose=false&key=93b912b5-9d70-4b1f-960b-fb80a4c9c017")
# Een response vragen en opslaan in 'response'.
responsejson  = response.json()
responsejson
response.json()
# De response omzetten in een json format.
Laadpalen = pd.json_normalize(responsejson)
df4 = pd.json_normalize(Laadpalen.Connections)
df5 = pd.json_normalize(df4[0])
df5.head()
Laadpalen = pd.concat([Laadpalen, df5], axis=1)
# De response in json format omzetten naar een pandas framework. 
Laadpalen.head()
# De colomnamen opvragen om te kijken wat er allemaal in het dataframe zit.
Laadpalen.columns

Laadpalen.dropna(subset = ['AddressInfo.Postcode'], inplace=True)
# Alle data zonder postcode verwijderen uit de dataframe en index resetten.

Laadpalen['Kleur'] = ''

for i in Laadpalen.index:
    Laadpalen.at[i,'AddressInfo.Postcode'] = Laadpalen['AddressInfo.Postcode'][i].replace(" ","")
# Een for-loop om de postcodes klaar te maken voor gebruik
for i, row in Laadpalen.iterrows():
    nomi = pgeocode.Nominatim('NL')
    zip_info = nomi.query_postal_code(Laadpalen['AddressInfo.Postcode'][i][0:4])
    Laadpalen.at[i,'AddressInfo.StateOrProvince'] = zip_info['state_name']
    Laadpalen.at[i,'Kleur'] = color_producer(zip_info['state_name'])

# Door middel van de pgeocode is bij elke rij nu de juiste porvincie ingevuld

Laadpalen['Inwoners gemeente'] = 0
Laadpalen['Gemeente'] = ''
Laadpalen['Radius'] = 0 
# Toevoegen van kolommen die later gebruikt gaan worden.
Laadpalen['AddressInfo.StateOrProvince'].value_counts()
# Checken of het is gelukt om alle provincies te vinden.

pop_gem = pd.read_excel('voorlopige-bevolkings-gegevens-20230101.xlsx', sheet_name='Data')
# Inladen van data over inwoners per gemeente en in een dataframe zetten.
pop_gem.head()

for i in Laadpalen.index:
    nomi = pgeocode.Nominatim('NL')
    zip_info = nomi.query_postal_code(Laadpalen['AddressInfo.Postcode'][i][0:4])
    for x in pop_gem.index:
        if pop_gem['Gemeentenaam'][x] == zip_info['county_name']:
            Laadpalen.at[i,'Inwoners gemeente'] = pop_gem['Aantal inwoners'][x]
            Laadpalen.at[i,'Gemeente'] = pop_gem['Gemeentenaam'][x]
# Een for-loop om inwoners per gemeente en de naam van de gemeente te te voegen.
    
Laadpalen[['Inwoners gemeente', 'Gemeente']]
# Checken of het is gelukt.

Laadpalen.drop(Laadpalen[Laadpalen['Inwoners gemeente'] == 0].index, inplace = True)
# Bij de gemeentes waar de data niet goed is ingevuld (waardes zijn '' of 0) worden verwijdert

for i in Laadpalen.index:
    Palen_Per_Gemeente = (Laadpalen['Inwoners gemeente'][i] / Laadpalen['Gemeente'].value_counts()[Laadpalen['Gemeente'][i]]) / 13.9
    Laadpalen.at[i,'Radius'] = Palen_Per_Gemeente
# Een for-loop om te bepalen hoeveel inwoners er zijn per specifieke laadpaal.
Laadpalen[['Gemeente','Radius']].head(30)
# Checken of het is gelukt

Laadpalen.to_csv('data.csv')
Laadpalen = pd.read_csv('data.csv')
# Met deze for-loop worden alle cirkels geplaats op de kaart.
# De grote van de cirkel is gebasseerd op het aantal inwoners per gemeente gedeeld door het aantal laadpalen.
# De kleur wordt bepaald door de color_producer gebasseerd op gemeente.
######### DIT IS NIET DE FILE DIE GERUNT MOET WORDEN VIA STREAMLIT!!! #########