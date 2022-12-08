import csv
from pathlib import Path

def getPokemon(route):
    PokemonList = []
    PokemonLevelList = []
    TrueMinLevel = 100
    path = Path("csv_files/" + route + ".csv")
    with open(path, newline='') as csvfile:
        Pokereader = csv.DictReader(csvfile)
        for row in Pokereader:
            for x in range(int(row['Frequency'])):
                PokemonList.append(row['Pokemon'])
            PokemonLevelList.append([row['Pokemon'], row['MinLevel'], row['MaxLevel']])
            if (int(row['MinLevel']) < TrueMinLevel): TrueMinLevel = int(row['MinLevel'])
    
    return (PokemonList, PokemonLevelList, TrueMinLevel)