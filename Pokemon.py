import csv

class Pokemon:
    def __init__(self, name):
        
        self.name = name
        self.forms = []
        
    def setForms(self, name):
        with open('csv_files/Pokemon.csv', newline='') as csvfile:
            Pokereader = csv.DictReader(csvfile)
            for row in Pokereader:
                if (row['Name'] == name):
                    if (row['Forms'] is not None):
                        forms = row['Forms']
                        forms = forms.split('.')
                        self.forms = forms
                    return
        
    def __str__(self):
        return f"{self.name}"
