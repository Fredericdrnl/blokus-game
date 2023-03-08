import json
import os
import datetime

class jsonManager():

    @staticmethod
    def writeJson(data:dict,outfile = './src/models/data.json')->None:
        with open(outfile,"w") as file:
            file.write(json.dumps(data,indent=4))
        file.close()

    @staticmethod
    def readJson(file = './src/models/data.json')->dict:
        with open(file,"r") as outfile:
            data = json.load(outfile)
        outfile.close()
        return data

class dataGame():

    def __init__(self) -> None:
        date = datetime.datetime.now()
        heure = str(date.hour) + "h" + str(date.minute)
        date = str(date.day) + "-" + str(date.month) + "-" + str(date.year)
        self.id = "1"

        if os.path.exists('./src/models/data.json'):
            self.data = jsonManager.readJson()
            self.id = str(int(list(self.data["parties"].keys())[-1]) + 1)
            self.data["parties"][self.id] = {'date': date, 'heure': heure, 'bleu': {'score': 0, 'historique_placement': []}, 'rouge': {'score': 0, 'historique_placement': []}, 'vert': {'score': 0, 'historique_placement': []}, 'jaune': {'score': 0, 'historique_placement': []}}
            jsonManager.writeJson(self.data)
        else:
            jsonManager.writeJson(jsonManager.readJson("./src/models/template_data.json"))
            self.data = jsonManager.readJson()
            self.data["parties"]["1"]["heure"] = heure
            self.data["parties"]["1"]["date"] = date
            jsonManager.writeJson(self.data)

    
    def addPoints(self,couleur:str,taillePiece:int)->None:
        self.data = jsonManager.readJson()
        self.data["parties"][self.id][couleur.lower()]["score"]+=taillePiece
        jsonManager.writeJson(self.data)

    def addToHistoriquePlayer(self,couleur,ligne,colonne,numPiece)->None:
        self.data = jsonManager.readJson()
        self.data["parties"][self.id][couleur.lower()]["historique_placement"].append([[ligne,colonne],numPiece])
        jsonManager.writeJson(self.data)
