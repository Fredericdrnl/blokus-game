from views.View import View
from utils.window_utils import _resizeWindow
from tkinter import Frame
from customtkinter import CTkImage,CTkLabel
from PIL import Image
from components.game.grille import grille
from components.game.score import score
from components.game.piecesManager import piecesManager
from models.Player import Player


class GameView(View):

    def __init__(self,controller,window,width=1300,heigth=800):

        super().__init__()
        self.gameController = controller
        self.window = window
        _resizeWindow(self.window,width,heigth)

        self._callComponents()
        self.bg.place(x = 0,y = 0)
    

    def _makeFrame(self):
        self.mainFrame = Frame(self.window,width= 1300,height=800)
        self.mainFrame.pack()
        self.mainFrame.pack_propagate(0)

    def _callComponents(self):
        self._makeFrame()
        self._makeBackground()

        self.grille = grille(self.window,600,600)
        self.score = score(self.window,Player('Bleu'))
        self.piecesManager = piecesManager(self.window,Player('Bleu'),self)

    def _makeBackground(self):
        self.bgImage = CTkImage(Image.open("./media/assets/background_game.png"),size=(1300,800))
        self.bg = CTkLabel(self.window,text="",image = self.bgImage)

    def _callbackOnDrop(self,file:str,x:int,y:int,rotation:int,inversion:int):
        self.gameController.callback(file,x,y,rotation,inversion)

    def _addToGrid(self,chemin,x,y):
        self.grille._addPieceToGrille(chemin,x,y)

    def update(self,player):
        self.score.nextPlayer(player)
        self.piecesManager.frame.destroy()
        self.piecesManager = piecesManager(self.window,player,self)

    def main(self):
        pass

    def close(self):
        return