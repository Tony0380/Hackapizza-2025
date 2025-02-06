import csv

class LettoreDomande:
    def __init__(self, file):
        self.domande = []
        self.file = file

    def leggi(self):
        with open(self.file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.domande.append(row)
        return self.domande