import Pokemon
import csvreader

import csv
import tkinter as tk
from tkinter import font as tkfont
from tkinter.filedialog import asksaveasfile
from PIL import ImageTk, Image  
import random
from pathlib import Path

#encounter data from https://pokemondb.net/location#tab=loc-paldea

CaughtPokemon = [] #keeps track of Pokemon caught during nuzlocke
pkmnname = [] #keeps track of Pokemon caught during nuzlocke, but their names instead of the pokemon object
Encounters = [] #keeps track of route names
fileName = [] #keeps track of csv file names
PkmnRoutePairs = [] #keeps track of Pokemon/route pairs
LevelCaps = [] #keeps track of level caps
scarletExclusives = ["Larvitar", "Pupitar", "Tyranitar", "Drifloon", "Drifblim", "Stunky", "Skuntank", "Deino", "Zweilous", "Hydregion", "Skrelp", "Dragalge", "Oranguru", "Stonjourner", "Great Tusk", "Brute Bonnet", "Sandy Shocks", "Scream Tail", "Flutter Mane", "Slither Wing", "Roaring Moon", "Armarouge", "Koraidon"]
violetExclusives = ["Misdreavus", "Gulpin", "Swalot", "Bagon", "Shelgon", "Salamence", "Mismagius", "Clauncher", "Clawitzer", "Passimian", "Dreepy", "Drakloak", "Dragapult", "Eiscue", "Iron Treads", "Iron Moth", "Iron Hands", "Iron Jugulis", "Iron Thorns", "Iron Bundle", "Iron Valiant", "Ceruledge", "Miraidon"]
currentLevelCap=15
isScarlet = True
#G = Gym, T = Titan, S = Star, Cl = Clavell, Ne = Nemona, Ar = Arven, Pe = Penny, ST = Sada/Turo, E4 = Elite Four + Champion

#read list of routes
rpath = Path(".venv/csv_files/routes.csv")
with open(rpath, newline='') as csvfile:
    routeReader = csv.DictReader(csvfile)
    for row in routeReader:
        Encounters.append(row['routename'])
        fileName.append(row['filename'])

#import all level caps
lpath = Path(".venv/csv_files/levelcaps.csv")
with open(lpath, newline='') as csvfile:
    routeReader = csv.DictReader(csvfile)
    for row in routeReader:
        LevelCaps.append(row)
        
def rollEncounter(route, controller):
    pair = csvreader.getPokemon(route)
    PokemonChoices = pair[0]
    PokemonLevels = pair[1]
    randomChoice = "Unknown"
    #print(PokemonChoices)
    
    print(pkmnname)
    noDupes= [*set(PokemonChoices)]
    allCaught = True
    for pkmn in noDupes:
        if (pkmnname.count(pkmn) <= 0): 
            allCaught = False
            break
    if (allCaught): choice = Pokemon.Pokemon("NOCAPTURE") 
    else:
        while (randomChoice in pkmnname or randomChoice == "Unknown"):
            randomChoice = random.choice(PokemonChoices)
            index = [y[0] for y in PokemonLevels].index(randomChoice)
            if isScarlet:
                if randomChoice in violetExclusives or int(PokemonLevels[index][1]) > currentLevelCap: randomChoice = "Unknown"
            else:
                if randomChoice in scarletExclusives or int(PokemonLevels[index][1]) > currentLevelCap: randomChoice = "Unknown"
            
        choice = Pokemon.Pokemon(randomChoice)
        choice.setForms(randomChoice)
        CaughtPokemon.append(choice)
        pkmnname.append(randomChoice)
        if (choice.forms.__len__ != 0):
            for form in choice.forms:
                tempMon = Pokemon.Pokemon(form)
                tempMon.setForms(form)
                CaughtPokemon.append(tempMon)
                pkmnname.append(form)
    
    index = fileName.index(route)
    Route = Encounters[index]
    confirmPokemon(choice.name, route)
    controller.frames["RolledEncounter"] = RolledEncounter(parent=controller.container, Route=Route, Pokemon=choice, controller=controller)
    controller.frames["SuccessfulCatch"] = SuccessfulCatch(parent=controller.container, Route=Route, Pokemon=choice, controller=controller)
    controller.frames["FailedCatch"] = FailedCatch(parent=controller.container, Route=Route, Pokemon=choice, controller=controller)
    controller.frames["RolledEncounter"].grid(row=0, column=0, sticky="nsew")
    controller.frames["SuccessfulCatch"].grid(row=0, column=0, sticky="nsew")
    controller.frames["FailedCatch"].grid(row=0, column=0, sticky="nsew")
    controller.show_frame("RolledEncounter")
    return choice

def removePokemon(pokemonName):
    deletedPokemon = pokemonName
    pkmnname.remove(deletedPokemon.name)
    for forms in deletedPokemon.forms:
        pkmnname.remove(Pokemon.Pokemon(forms).name)
    print(pkmnname)
     
def confirmPokemon(pokemonName, routeName):
    PkmnRoutePairs.append([pokemonName, routeName])

#Pokemon has yet to be rolled
class UnknownPokemon(tk.Frame):
    def __init__(self, parent, controller, Route):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text=Route, font=controller.title_font, wraplength=200)
        label.pack(side="top", fill="x", pady=10)
        UnknownImage = Image.open(".venv/images/Unknown.png")
        resizeImage = UnknownImage.resize((75,75))
        img = ImageTk.PhotoImage(master=self, image=resizeImage)
        
        label1 = tk.Label(self, image=img)
        label1.image = img

        label1.pack()

        PokemonName = tk.Label(self, text="Pokemon not yet rolled")
        PokemonName.pack()
        index = Encounters.index(Route)
        roll = tk.Button(self, text="Roll Capture", command=lambda: [rollEncounter(fileName[index], controller)])
        roll.pack()
        
class RolledEncounter(tk.Frame):
    def __init__(self, parent, controller, Route, Pokemon):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text=Route, font=controller.title_font, wraplength=200)
        label.pack(side="top", fill="x", pady=10)
        print(Pokemon.name)
        PokemonImage = Image.open(".venv/images/" + Pokemon.name + ".png")
        resizeImage = PokemonImage.resize((75,75))
        img = ImageTk.PhotoImage(master=self, image=resizeImage)

        label1 = tk.Label(self, image=img)
        label1.image = img

        label1.pack()

        PokemonName = tk.Label(self, text=Pokemon.name)
        PokemonName.pack()

        successfulCapture = tk.Button(self, text = "Succesful Capture", command=lambda: controller.show_frame("SuccessfulCatch"))
        successfulCapture.pack()
        failedCapture = tk.Button(self, text="Failed Capture", command=lambda: [removePokemon(Pokemon), controller.show_frame("FailedCatch")])
        failedCapture.pack()
        
class SuccessfulCatch(tk.Frame):
    def __init__(self, parent, controller, Route, Pokemon):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text=Route, font=controller.title_font, wraplength=200)
        label.pack(side="top", fill="x", pady=10)
        PokemonImage = Image.open(".venv/images/" + Pokemon.name + ".png")
        PokemonImage = PokemonImage.convert("RGBA")
        d = PokemonImage.getdata()
        new_image = []
        for item in d:
            new_image.append((item[0], int(min(2*item[1], 255)), item[2], item[3]))
        PokemonImage.putdata(new_image)
        resizeImage = PokemonImage.resize((75,75))
        img = ImageTk.PhotoImage(master=self, image=resizeImage)
        label1 = tk.Label(self, image=img)
        label1.image = img

        label1.pack()

        PokemonName = tk.Label(self, text=Pokemon.name)
        PokemonName.pack()
        
class FailedCatch(tk.Frame):
    def __init__(self, parent, controller, Route, Pokemon):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text=Route, font=controller.title_font, wraplength=200)
        label.pack(side="top", fill="x", pady=10)
        PokemonImage = Image.open(".venv/images/" + Pokemon.name + ".png")
        PokemonImage = PokemonImage.convert("RGBA")
        d = PokemonImage.getdata()
        new_image = []
        for item in d:
            new_image.append((int(min(4*item[0], 255)), item[1], item[2], item[3]))
        PokemonImage.putdata(new_image)
        resizeImage = PokemonImage.resize((75,75))
        img = ImageTk.PhotoImage(master=self, image=resizeImage)
        label1 = tk.Label(self, image=img)
        label1.image = img

        label1.pack()

        PokemonName = tk.Label(self, text=Pokemon.name)
        PokemonName.pack()

#window = tk.Tk()
#window.title("Pokemon Scarlet and Violet Nuzlocke Assistant")





class Node(tk.Frame):
    def __init__(self, index, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        Route = Encounters[index]
        #pkmn = rollEncounter(fileName[index])
        self.title_font = tkfont.Font(family='sans', size=14, weight="bold", slant="italic")
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        self.frames["UnknownPokemon"] = UnknownPokemon(parent=self.container, Route=Route, controller=self)
        #self.frames["RolledEncounter"] = RolledEncounter(parent=container, Route=Route, Pokemon=pkmn, controller=self)
        #self.frames["SuccessfulCatch"] = SuccessfulCatch(parent=container, Route=Route, Pokemon=pkmn, controller=self)
        #self.frames["FailedCatch"] = FailedCatch(parent=container, Route=Route, Pokemon=pkmn, controller=self)
        self.frames["UnknownPokemon"].grid(row=0, column=0, sticky="nsew")
        #self.frames["RolledEncounter"].grid(row=0, column=0, sticky="nsew")
        #self.frames["SuccessfulCatch"].grid(row=0, column=0, sticky="nsew")
        #self.frames["FailedCatch"].grid(row=0, column=0, sticky="nsew")
        self.show_frame("UnknownPokemon")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

def switch():
    global isScarlet
    if isScarlet:
        on_button.config(image = off)
        isScarlet = False
    else:
        on_button.config(image = on)
        isScarlet = True
        
def save():
    file = asksaveasfile(initialfile='SaveData.csv', defaultextension=".csv",filetypes=[('All tyes(*.*)', '*.*'),("csv file(*.csv)","*.csv")])
    with open(file, 'w', newline='') as f:
        f.writerow(['Pokemon','Route'])
        for pair in PkmnRoutePairs:
            f.writerow(pair[0],pair[1])

def load():
    print("We need to implement this")
        
 
        
app = tk.Tk()
app.title("Pokemon Scarlet and Violet Nuzlocke Assistant")
#indicating which version
onresized = Image.open(".venv/images/isScarlet.png").resize((150,100))
on = ImageTk.PhotoImage(onresized)
offresized = Image.open(".venv/images/isViolet.png").resize((150,100))
off = ImageTk.PhotoImage(offresized)
on_button = tk.Button(app, image=on, bd=0, command=switch)
on_button.grid(row=0, column=2, sticky=(tk.N, tk.S, tk.E, tk.W))
scarletLabel = tk.Label(app, text="Scarlet", fg='#D81414', font=("sans 16 bold"), anchor="e").grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
violetLabel = tk.Label(app, text="Violet", fg='#8A14D8', font=("sans 16 bold"), anchor="w").grid(row=0, column=3, sticky=(tk.N, tk.S, tk.E, tk.W))
#save and load buttons
save_btn = tk.Button(app, text="Save", bg='#D81414', fg='#8A14D8', font=("sans 20 bold"), command=save).grid(row=0,column=4, sticky=(tk.N, tk.S, tk.E, tk.W))
load_btn = tk.Button(app, text="Load", bg='#8A14D8', fg='#D81414', font=("sans 20 bold"), command=load).grid(row=0,column=5, sticky=(tk.N, tk.S, tk.E, tk.W))
#level caps menu
clicked = tk.StringVar()
clicked.set(LevelCaps[0])
drop = tk.OptionMenu(app, clicked, *LevelCaps)
drop.grid(row=0, column=6, sticky=(tk.N, tk.S, tk.E, tk.W))


nodes = [[Node(8*r+c) for c in range(8)] for r in range(4)]
for r in range(4):
    for c in range(8):
        index = 8*r + c
        nodes[r][c] = Node(index).grid(row=r+1, column=c+1, sticky=(tk.N, tk.S, tk.E, tk.W))
#intended width = 1382
#intended height = 864
app.mainloop()

    
#TODO
"""
1. Fix duplicate logic and rolling logic so that rolls are not done prior to pressing the button to roll for the encounter (COMPLETE)
2. Get scrollbar working
3. Add saving and loading functionality
4. Download all Pokemon images (COMPLETE)
5. Input Encounters into csv files
6. Fix layout to make it look nice and symmetrical
7. Deal with version exclusives (Complete)
8. Add level caps
"""
    
        
    
        