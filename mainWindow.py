import sys
sys.path.append('./controller/')

from tkinter import BOTH, Canvas
from tkinter import Tk
import tkinter
from tkinter.messagebox import YES
from typing_extensions import Self
from PIL import Image,ImageTk
import customtkinter
from PIL import ImageGrab
import customtkinter
from tkinter import Canvas, filedialog,PhotoImage

from controller.plateau import Plateau
from controller.player import Player
from controller.checkIn import validPlacement,coordsBlocs,playerCanPlay

from testMap import MAP1
from VuePiece import VuePiece
from VueGrilleJeu import VueGrilleJeu
from VueTourJoueur import VueTourJoueur
from VueNbPieceJoueur import VueNbPieceJoueur
from VueStatsPlayer import VueStatsPlayer

class VueBlokus():

    def __init__(self,master,menu_window :customtkinter.CTk,plateau:Plateau):

        self.master = master
        self.joueurs : list[Player] = [Player("Bleu"),Player("Jaune"),Player("Vert"),Player("Rouge")]
        self.index : int = 0
        self.actualPlayer : Player = self.joueurs[self.index]
        self.plateau = plateau       
        self.window = menu_window
        self.window.geometry("1300x800")
        self.window.title("Jeu Blokus")
        self.window.iconbitmap('./Icon/icon.ico')
        self.window.resizable(width=False, height=False)

        self.UI()
        self.window.mainloop()

    def UI(self):



        self.backgroundImage = Image.open("./assets/background_game.png")
        self.background = ImageTk.PhotoImage(self.backgroundImage)

        self.label = tkinter.Label(self.window, image = self.background, bd = 0)
        self.label.place(x = 0,y = 0)

        
        self.grilleJeu = VueGrilleJeu(self.window, 600, 600)
    
        self.vuePiece = VuePiece(self.window,Player('Bleu'),self)

        self.backgroundButtonSave = PhotoImage(file="./assets/button_save.png")
        
        self.button = tkinter.Button(
            master=self.window, 
            text='', 
            image = self.backgroundButtonSave, 
            command = self.callbackSave, 
            borderwidth=0, 
            bd=0,
            highlightthickness=0,  
            anchor="nw")
        self.button.place(x=1000,y=665)

        self.statsPlayer = VueStatsPlayer(self.window,self.actualPlayer)
        # self.window.wm_attributes("-topmost", True)

        
        self.loadMap()

    def loadMap(self:Self):
        
        indexJoueur = 0
        for couleur,pieces in MAP1.items():
            cheminFichierPiece = "./Pieces/" + couleur.upper()[0] + "/1.png"
            for piece in pieces :

                p = self.joueurs[indexJoueur].jouerPiece(piece[0]) 
                p = coordsBlocs(p,piece[1][1],piece[1][0])
                for coordx,coordy in p:
                    self.grilleJeu.addPieceToGrille(cheminFichierPiece,coordy,coordx)
                    self.plateau.setColorOfCase(coordx,coordy,indexJoueur)
                
                self.joueurs[indexJoueur].hasPlayedPiece(piece[0])
                self.joueurs[indexJoueur].removePiece(piece[0])

            indexJoueur +=1

        self.displayPiecesPlayer()

    def callbackPiece(self:Self,file:str,x:int,y:int,rotation:int):
        
        numPiece = int(file.split("/")[3].split(".")[0])
        # -1 car c'est une liste, ici c'est pas des png.

        piece = self.actualPlayer.jouerPiece(numPiece-1)
        couleurJoueur = self.actualPlayer.getCouleur()
        indexJoueur = self.joueurs.index(self.actualPlayer)

        print("----------------------------")
        print(self.actualPlayer.pieces.pieces_joueurs)
        # ----- Partie rotation
        nb_rotation = abs(rotation)//90
        for i in range(nb_rotation):
            self.actualPlayer.pieces.rotate(numPiece-1)
            piece = self.actualPlayer.jouerPiece(numPiece-1)

        pieceBlokus = coordsBlocs(piece,x//30,y//30)
        cheminFichierPiece = "./Pieces/" + couleurJoueur.upper()[0] + "/1.png"
        
        # ---- Vérification du placement
        if validPlacement(piece,y//30,x//30,self.plateau,self.actualPlayer):
            self.actualPlayer.removePiece(numPiece-1)

            for coordY,coordX in pieceBlokus:
                self.grilleJeu.addPieceToGrille(cheminFichierPiece,coordX,coordY)
                self.plateau.setColorOfCase(coordY,coordX,indexJoueur)

            self.actualPlayer.hasPlayedPiece(numPiece-1)    
            self.nextPlayer()
            self.displayPiecesPlayer()
            self.statsPlayer.tourJoueur.setNewColor()
            self.statsPlayer.nbPiecesPlayer.nextPlayer(self.actualPlayer)        
        # Partie reset rotation
        if nb_rotation>0:    
            self.actualPlayer.pieces.resetRotation(numPiece-1)
        
    

    def displayPiecesPlayer(self:Self):
        self.vuePiece.frame.destroy()
        self.vuePiece = VuePiece(self.window,self.actualPlayer,self)

    def nextPlayer(self:Self)->None:

        playedPlayer = self.actualPlayer.getCouleur()
        self.index= (self.index+1)%4
        self.actualPlayer =  self.joueurs[self.index]
        playable = False
        for i in range(0,2):
            if playerCanPlay(self.actualPlayer,self.plateau): 
                playable = True
                break
            self.index= (self.index+1)%4
            self.actualPlayer =  self.joueurs[self.index]
        
        # print(playedPlayer,self.actualPlayer.getCouleur())
        if not playable:
            self.label.destroy()
            self.vuePiece.frame.destroy()
            self.grilleJeu.canvas.destroy()
            self.button.destroy()
            self.statsPlayer.frame.destroy()
            self.master.emitFinishGame(self.joueurs)

    


    def callbackSave(self):
        x = Canvas.winfo_rootx(self.grilleJeu.canvas)
        y = Canvas.winfo_rooty(self.grilleJeu.canvas)
        w = Canvas.winfo_width(self.grilleJeu.canvas) 
        h = Canvas.winfo_height(self.grilleJeu.canvas)
        directory = filedialog.asksaveasfilename(defaultextension="png", filetypes=[("PNG", ".png"), ("JPG", ".jpg"), ("JPEG", ".jpeg")])
        ImageGrab.grab((x, y, x+w, y+h)).save(directory)



if __name__ ==  "__main__":
    window = customtkinter.CTk()
    app = VueBlokus(window) 


    # a=customtkinter.CTk()
    # a.geometry('800x500+275+100')
    # a.title('HOME PAGE')


    # load=Image.open('./Pieces/B/21.png')
    # render=ImageTk.PhotoImage(load)
    # img=customtkinter.CTkLabel(a,image=render)
    # img.pack()

    # a.mainloop()





