import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
import csv
from pathlib import Path

page = requests.get("https://pokemondb.net/location/paldea-west-province-area-three")
soup = BeautifulSoup(page.content, 'html.parser')
data = {}

pokemontables = soup.find_all('tr')
for row in pokemontables:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    
    #Doesn't parse empty rows
    if len(cols) != 0:
        pokemonName = row.find('a')
        pokemonName = pokemonName.text.strip()
        #If the pokemon is in the dict
        if pokemonName in data:
            data[pokemonName][3] += 1
            data[pokemonName][0] += int(cols[4][:-1])
            minLevel, maxLevel = [int(result) for result in cols[5].split('-')]
            #Find the highest max and the lowest min
            if data[pokemonName][1] > minLevel:
                data[pokemonName][1] = minLevel
            if data[pokemonName][2] < maxLevel:
                data[pokemonName][2] = maxLevel
        #If the pokemon is not in the dict
        elif pokemonName != "Gimmighoul":
            minLevel, maxLevel = cols[5].split('-')
            data[pokemonName] = [int(cols[4][:-1]), int(minLevel), int(maxLevel), 1]
        #int(cols[4][:-1]) removes the percent value and turn the sting into an integer
        #this allows for averaging as the next step
f = open('output.csv', 'w')
f.write('Pokemon,Frequency,MinLevel,MaxLevel\n')


PokemonList = []
path = Path("csv_files/WP3.csv")
with open(path, newline='') as csvfile:
    Pokereader = csv.DictReader(csvfile)
    for row in Pokereader:
        PokemonList.append(row['Pokemon'])
        
for key in data:
    data[key][0] = data[key][0]//data[key][3]
    if (key in PokemonList):
        f.write(unidecode(key) + ',' + str(data[key][0]) + ',' + str(data[key][1]) + ',' + str(data[key][2]) + '\n')
f.close()


