import csv
from pathlib import Path

def getPokemon(route):
    PokemonList = []
    path = Path(".venv/csv_files/" + route + ".csv")
    with open(path, newline='') as csvfile:
        Pokereader = csv.DictReader(csvfile)
        for row in Pokereader:
            for x in range(int(row['Frequency'])):
                PokemonList.append(row['Pokemon'])
    return PokemonList