from pypdf import PdfReader
import os

class Lettore:
    def __init__(self, path):
        self.path = path
        self.reader = PdfReader
        self.file_list = []

    def EstraiFile(self):
        for nome_file in os.listdir(self.path):
            percorso_completo = os.path.join(self.path, nome_file)
            if os.path.isfile(percorso_completo):
                self.file_list.append(nome_file)
        return self.file_list




a = Lettore("../Hackapizza Dataset/Menu")
h = a.EstraiFile()
print(h)


