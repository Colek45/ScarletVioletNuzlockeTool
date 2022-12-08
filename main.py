import Pokemon
import csvreader

import csv
import tkinter as tk
from tkinter import font as tkfont
from tkinter.filedialog import asksaveasfile, asksaveasfilename
from PIL import ImageTk, Image  
import random
import re
from pathlib import Path
import os
        
def rollEncounter(route, controller):
    global currentLevelCap
    tuple = csvreader.getPokemon(route)
    PokemonChoices = tuple[0]
    PokemonLevels = tuple[1]
    minlevel = tuple[2]
    randomChoice = "Unknown"
    #print(PokemonChoices)
    
    print(pkmnname)
    noDupes= [*set(PokemonChoices)]
    allCaught = True
    for pkmn in noDupes:
        if (pkmnname.count(pkmn) <= 0): 
            allCaught = False
            break
    if (allCaught or minlevel > currentLevelCap): choice = Pokemon.Pokemon("NOCAPTURE") 
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
    confirmPokemon(choice.name, route, "Rolled")
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
     
def confirmPokemon(pokemonName, routeName, status):
    if status == "Caught" or status == "Failed":
        for i, row in enumerate(PkmnRoutePairs):
            if str(row[0]) == str(pokemonName):
                PkmnRoutePairs[i] = ([PkmnRoutePairs[i][0], PkmnRoutePairs[i][1], status])
                return
    else:
        PkmnRoutePairs.append([pokemonName, routeName, status])
    
def loadPokemon(pokemonName, routeName, status, controller):
    choice = Pokemon.Pokemon(pokemonName)
    choice.setForms(pokemonName)
    CaughtPokemon.append(choice)
    pkmnname.append(pokemonName)
    if (choice.forms.__len__ != 0):
        for form in choice.forms:
            tempMon = Pokemon.Pokemon(form)
            tempMon.setForms(form)
            CaughtPokemon.append(tempMon)
            pkmnname.append(form)
    index = fileName.index(routeName)
    Route = Encounters[index]
    if status == "Starter":
        match pokemonName:
            case "Sprigatito":
                controller.frames["SprigatitoStarter"] = FuecocoStarter(parent=controller.container, Route=Route, controller=controller)
                controller.frames["SprigatitoStarter"].grid(row=0, column=0, sticky="nsew")
                controller.show_frame("SprigatitoStarter")
            case "Quaxly":
                controller.frames["QuaxlyStarter"] = FuecocoStarter(parent=controller.container, Route=Route, controller=controller)
                controller.frames["QuaxlyStarter"].grid(row=0, column=0, sticky="nsew")
                controller.show_frame("QuaxlyStarter")
            case "Fuecoco":
                controller.frames["FuecocoStarter"] = FuecocoStarter(parent=controller.container, Route=Route, controller=controller)
                controller.frames["FuecocoStarter"].grid(row=0, column=0, sticky="nsew")
                controller.show_frame("FuecocoStarter")

    else:
        controller.frames["RolledEncounter"] = RolledEncounter(parent=controller.container, Route=Route, Pokemon=choice, controller=controller)
        controller.frames["SuccessfulCatch"] = SuccessfulCatch(parent=controller.container, Route=Route, Pokemon=choice, controller=controller)
        controller.frames["FailedCatch"] = FailedCatch(parent=controller.container, Route=Route, Pokemon=choice, controller=controller)
        controller.frames["RolledEncounter"].grid(row=0, column=0, sticky="nsew")
        controller.frames["SuccessfulCatch"].grid(row=0, column=0, sticky="nsew")
        controller.frames["FailedCatch"].grid(row=0, column=0, sticky="nsew")
        match status:
            case "Rolled":
                controller.show_frame("RolledEncounter")
            case "Caught":
                controller.show_frame("SuccessfulCatch")
            case "Failed":
                controller.show_frame("FailedCatch")
    PkmnRoutePairs.append([pokemonName, routeName, status])
        

#Pokemon has yet to be rolled
class UnknownPokemon(tk.Frame):
    def __init__(self, parent, controller, Route):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text=Route, font=controller.title_font, wraplength=200)
        label.pack(side="top", fill="x", pady=10)
        UnknownImage = Image.open("images/Unknown.png")
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
        PokemonImage = Image.open("images/" + Pokemon.name + ".png")
        resizeImage = PokemonImage.resize((75,75))
        img = ImageTk.PhotoImage(master=self, image=resizeImage)

        label1 = tk.Label(self, image=img)
        label1.image = img

        label1.pack()

        PokemonName = tk.Label(self, text=Pokemon.name)
        PokemonName.pack()
        
        if(Pokemon.name != "NOCAPTURE"):
            successfulCapture = tk.Button(self, text = "Succesful Capture", command=lambda: [confirmPokemon(Pokemon, Route, "Caught"), controller.show_frame("SuccessfulCatch")])
            successfulCapture.pack()
            failedCapture = tk.Button(self, text="Failed Capture", command=lambda: [confirmPokemon(Pokemon, Route, "Failed"), removePokemon(Pokemon), controller.show_frame("FailedCatch")])
            failedCapture.pack()
        
class SuccessfulCatch(tk.Frame):
    def __init__(self, parent, controller, Route, Pokemon):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text=Route, font=controller.title_font, wraplength=200)
        label.pack(side="top", fill="x", pady=10)
        PokemonImage = Image.open("images/" + Pokemon.name + ".png")
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
        PokemonImage = Image.open("images/" + Pokemon.name + ".png")
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


class UnknownStarter(tk.Frame):
    def __init__(self, parent, controller, Route):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text=Route, font=controller.title_font, wraplength=200)
        label.pack(side="top", fill="x", pady=10)
        UnknownImage = Image.open("images/Unknown.png")
        resizeImage = UnknownImage.resize((75,75))
        img = ImageTk.PhotoImage(master=self, image=resizeImage)
        
        label1 = tk.Label(self, image=img)
        label1.image = img

        label1.pack()

        PokemonName = tk.Label(self, text="Select a starter Pokemon")
        PokemonName.pack()
        sprigButton = tk.Button(self, text="Sprigatito", command=lambda: [PkmnRoutePairs.append(["Sprigatito", "Starter", "Starter"]), controller.show_frame("SprigatitoStarter")])
        sprigButton.pack()
        cocoButton = tk.Button(self, text="Fuecoco", command=lambda: [PkmnRoutePairs.append(["Fuecoco", "Starter", "Starter"]), controller.show_frame("FuecocoStarter")])
        cocoButton.pack()
        quaxButton = tk.Button(self, text="Quaxly", command=lambda: [PkmnRoutePairs.append(["Quaxly", "Starter", "Starter"]), controller.show_frame("QuaxlyStarter")])
        quaxButton.pack()
        
class SprigatitoStarter(tk.Frame):
    def __init__(self, parent, controller, Route):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text=Route, font=controller.title_font, wraplength=200)
        label.pack(side="top", fill="x", pady=10)
        UnknownImage = Image.open("images/Sprigatito.png")
        resizeImage = UnknownImage.resize((75,75))
        img = ImageTk.PhotoImage(master=self, image=resizeImage)
        
        label1 = tk.Label(self, image=img)
        label1.image = img

        label1.pack()

        PokemonName = tk.Label(self, text="Sprigatito")
        PokemonName.pack()
        
class FuecocoStarter(tk.Frame):
    def __init__(self, parent, controller, Route):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text=Route, font=controller.title_font, wraplength=200)
        label.pack(side="top", fill="x", pady=10)
        UnknownImage = Image.open("images/Fuecoco.png")
        resizeImage = UnknownImage.resize((75,75))
        img = ImageTk.PhotoImage(master=self, image=resizeImage)
        
        label1 = tk.Label(self, image=img)
        label1.image = img

        label1.pack()

        PokemonName = tk.Label(self, text="Fuecoco")
        PokemonName.pack()
        
class QuaxlyStarter(tk.Frame):
    def __init__(self, parent, controller, Route):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text=Route, font=controller.title_font, wraplength=200)
        label.pack(side="top", fill="x", pady=10)
        UnknownImage = Image.open("images/Quaxly.png")
        resizeImage = UnknownImage.resize((75,75))
        img = ImageTk.PhotoImage(master=self, image=resizeImage)
        
        label1 = tk.Label(self, image=img)
        label1.image = img

        label1.pack()

        PokemonName = tk.Label(self, text="Quaxly")
        PokemonName.pack()
        


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
        if Route == "Starter":
            self.frames["UnknownStarter"] = UnknownStarter(parent=self.container, Route=Route, controller=self)
            self.frames["SprigatitoStarter"] = SprigatitoStarter(parent=self.container, Route=Route, controller=self)
            self.frames["FuecocoStarter"] = FuecocoStarter(parent=self.container, Route=Route, controller=self)
            self.frames["QuaxlyStarter"] = QuaxlyStarter(parent=self.container, Route=Route, controller=self)
            self.frames["UnknownStarter"].grid(row=0, column=0, sticky="nsew")
            self.frames["SprigatitoStarter"].grid(row=0, column=0, sticky="nsew")
            self.frames["FuecocoStarter"].grid(row=0, column=0, sticky="nsew")
            self.frames["QuaxlyStarter"].grid(row=0, column=0, sticky="nsew")
            self.show_frame("UnknownStarter")
        else: 
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
    
    def restore_pokemon(self, pokemonName, route, status):
        loadPokemon(pokemonName, route, status, self)
        
    def getNode(self):
        return self

def switch(on, off):
    global on_button
    global isScarlet
    if isScarlet:
        on_button.config(image = off)
        isScarlet = False
    else:
        on_button.config(image = on)
        isScarlet = True
        
def save():
    file = asksaveasfilename(initialfile='SaveData.csv', defaultextension=".csv",filetypes=[('All tyes(*.*)', '*.*'),("csv file(*.csv)","*.csv")])
    with open(file, 'w', newline='') as f:
        header=['Pokemon','Route','Status']
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for pair in PkmnRoutePairs:
            writer.writerow({'Pokemon' : pair[0], 'Route' : pair[1], 'Status' : pair[2]})
            
def load():
    with open("SaveData.csv", 'r', newline='') as reader:
        read = csv.DictReader(reader)
        for row in read:
            index = fileName.index(row['Route'])
            r = int(index/8)
            c = index%8
            nodes[r][c].restore_pokemon(row['Pokemon'], row['Route'], row['Status'])

def assignLevelCap(lc):
    global currentLevelCap
    currentLevelCap = int(re.search(r'\d+', clicked.get()[-9:]).group())
    print(currentLevelCap)
        
def main():
    #encounter data from https://pokemondb.net/location#tab=loc-paldea
    global CaughtPokemon
    global pkmnname
    global Encounters
    global fileName
    global PkmnRoutePairs
    global LevelCaps
    global scarletExclusives
    global violetExclusives
    global isScarlet
    global nodes
    global on_button
    CaughtPokemon = [] #keeps track of Pokemon caught during nuzlocke
    pkmnname = [] #keeps track of Pokemon caught during nuzlocke, but their names instead of the pokemon object
    Encounters = [] #keeps track of route names
    fileName = [] #keeps track of csv file names
    PkmnRoutePairs = [] #keeps track of Pokemon/route pairs
    LevelCaps = [] #keeps track of level caps
    scarletExclusives = ["Larvitar", "Pupitar", "Tyranitar", "Drifloon", "Drifblim", "Stunky", "Skuntank", "Deino", "Zweilous", "Hydregion", "Skrelp", "Dragalge", "Oranguru", "Stonjourner", "Great Tusk", "Brute Bonnet", "Sandy Shocks", "Scream Tail", "Flutter Mane", "Slither Wing", "Roaring Moon", "Armarouge", "Koraidon"]
    violetExclusives = ["Misdreavus", "Gulpin", "Swalot", "Bagon", "Shelgon", "Salamence", "Mismagius", "Clauncher", "Clawitzer", "Passimian", "Dreepy", "Drakloak", "Dragapult", "Eiscue", "Iron Treads", "Iron Moth", "Iron Hands", "Iron Jugulis", "Iron Thorns", "Iron Bundle", "Iron Valiant", "Ceruledge", "Miraidon"]
    global currentLevelCap
    isScarlet = True
    #G = Gym, T = Titan, S = Star, Cl = Clavell, Ne = Nemona, Ar = Arven, Pe = Penny, ST = Sada/Turo, E4 = Elite Four + Champion

    #read list of routes
    fileDirectory = os.path.dirname(os.path.abspath(__file__))
    print(fileDirectory)
    rpath = fileDirectory + "/csv_files/routes.csv"
    with open(rpath, newline='') as csvfile:
        routeReader = csv.DictReader(csvfile)
        for row in routeReader:
            Encounters.append(row['routename'])
            fileName.append(row['filename'])

    #import all level caps
    lpath = fileDirectory + "/csv_files/levelcaps.csv"
    with open(lpath, newline='') as csvfile:
        routeReader = csv.DictReader(csvfile)
        for row in routeReader:
            LevelCaps.append(row)
            
    app = tk.Tk()
    app.title("Pokemon Scarlet and Violet Nuzlocke Assistant")
    #indicating which version
    onresized = Image.open("images/isScarlet.png").resize((150,100))
    on = ImageTk.PhotoImage(onresized)
    offresized = Image.open("images/isViolet.png").resize((150,100))
    off = ImageTk.PhotoImage(offresized)
    on_button = tk.Button(app, image=on, bd=0, command=lambda: switch(on, off))
    on_button.grid(row=0, column=2, sticky=(tk.N, tk.S, tk.E, tk.W))
    scarletLabel = tk.Label(app, text="Scarlet", fg='#D81414', font=("sans 16 bold"), anchor="e").grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
    violetLabel = tk.Label(app, text="Violet", fg='#8A14D8', font=("sans 16 bold"), anchor="w").grid(row=0, column=3, sticky=(tk.N, tk.S, tk.E, tk.W))
    #save and load buttons
    save_btn = tk.Button(app, text="Save", bg='#D81414', fg='#8A14D8', font=("sans 20 bold"), command=save).grid(row=0,column=4, sticky=(tk.N, tk.S, tk.E, tk.W))
    load_btn = tk.Button(app, text="Load", bg='#8A14D8', fg='#D81414', font=("sans 20 bold"), command=load).grid(row=0,column=5, sticky=(tk.N, tk.S, tk.E, tk.W))
    #level caps menu
    clicked = tk.StringVar()
    clicked.set(LevelCaps[0])
    currentLevelCap = 15
    drop = tk.OptionMenu(app, clicked, *LevelCaps, command= assignLevelCap)
    drop.grid(row=0, column=7, sticky=(tk.N, tk.S, tk.E, tk.W))

    nodes = [[Node(8*r+c) for c in range(8)] for r in range(4)]
    for r in range(4):
        for c in range(8):
            index = 8*r + c
            node = Node(index)
            nodes[r][c] = node
            nodes[r][c].grid(row=r+1, column=c, sticky=(tk.N, tk.S, tk.E, tk.W))
    #intended width = 1382
    #intended height = 864
    for r in range(5):
        app.grid_rowconfigure(r, weight=1)
    for c in range(8):
        app.grid_columnconfigure(c, weight=1)
    app.mainloop()

if __name__ == "__main__":
    main()
    
#TODO
"""
1. Fix duplicate logic and rolling logic so that rolls are not done prior to pressing the button to roll for the encounter (COMPLETE)
2. Get scrollbar working (maybe) OR add resolution options [Alpha]
3. Add saving and loading functionality [Beta]
4. Download all Pokemon images (COMPLETE)
5. Input Encounters into csv files (COMPLETE)
6. Fix layout to make it look nice and symmetrical [Final Release]
7. Deal with version exclusives (COMPLETE)
8. Add level caps (COMPLETE)
"""
    
        
    
        