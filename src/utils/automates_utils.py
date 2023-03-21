from random import randint
from models.Player import Player
from models.Plateau import Plateau
from utils.game_utils import validPlacement,coordsBlocs,getDiagonals,getAdjacents
from copy import deepcopy
from utils.tree import Tree
from utils.tree import evaluateGame
import math

def medium_automate(joueurActuel : Player, plateau : Plateau, index : int, view):

    tree = Leaf(index,joueurActuel,plateau)
    tree.makeMove(view)

class Position:

    def __init__(self,x,y) -> None:
        self.left = [x,y-1]
        self.right = [x,y+1]
        self.top = [x-1,y]
        self.bottom = [x+1,y]

class Leaf():
    
    def __init__(self,indexJoueur,joueur,plateau:Plateau,parent=None) -> None:
        self.parent : Leaf|None = parent
        self.plateau : Plateau = plateau
        self.indexJoueur : int = indexJoueur 
        self.joueur : Player = joueur
        # self.score = gameManager.evaluateGame(self.plateau, self.indexJoueur,self.plateau)


        # print(self,self.parent,self.score)

    def makeMove(self,view):

        bestScore = -math.inf
        bestMove = None
        pos = gameManager.getBestPossibilities(self.plateau,self.indexJoueur,self.joueur)
        print('Possibilité ----> ',pos)

        for i in range(len(pos)):
            # plateau = deepcopy(self.plateau)
            # index = deepcopy(self.indexJoueur)
            joueur = deepcopy(self.joueur)
            score = self.minmax(False,self.plateau,joueur)
            if score>bestScore:
                bestScore=score
                bestMove = pos[i]
        
        print(bestScore)
        print("Meilleur position à jouer : ",bestMove)
        cheminFichierPiece = "./media/pieces/" + self.joueur.getCouleur().upper()[0] + "/1.png"
        
        # for xpos,ypos in bestMove:
        xpos,ypos= bestMove
        self.plateau.setColorOfCase(xpos,ypos,self.indexJoueur)
        view._addToGrid(cheminFichierPiece,ypos, xpos)



    def minmax(self,isMaxTurn,plateau:Plateau,joueur:Player,depth=0,maxDepth=2):

        if depth>maxDepth:
            return gameManager.evaluateGame(plateau,self.indexJoueur,joueur)
        
        scores = []
        pos = gameManager.getBestPossibilities(plateau,self.indexJoueur,joueur)
        for piece in joueur.pieces.pieces_joueurs:
            for i in range(len(pos)):
                check = gameManager.canPlacePiece(piece,plateau,pos[i][0],pos[i][1],joueur)
                if check[0]!=-1:
                    x,y = pos[i]
                    pieceBlokus = coordsBlocs(joueur.jouerPiece(piece),x,y)
                    for xpos,ypos in pieceBlokus:
                        plateau.setColorOfCase(xpos,ypos,self.indexJoueur)               
                    plateau.undoMove()   
                scores.append(self.minmax(not isMaxTurn,plateau,joueur,depth+1,maxDepth))

        return max(scores) if isMaxTurn else min(scores)       
    
TAILLE = 19
class gameManager:

    @staticmethod
    def isInGrid(side:list)->bool:
        if side[0] <= TAILLE and side[1] <= TAILLE and side[0] >= 0 and side[1] >= 0:
            return True
        return False
    
    @staticmethod
    def iterateGrid(plateau:Plateau,indexJoueur:int):
        for i in range(len(plateau.getTab())):
            for j in range(len(plateau.getTab()[0])):
                if plateau.getTab()[i][j] == indexJoueur:
                    yield i,j

    @staticmethod
    def getBestPossibilities(plateau:Plateau, indexJoueur:int, joueur:Player):
        startPos = joueur.getPositionDepart()
        grid = plateau.getTab()
        if grid[startPos[0]][startPos[1]]!=indexJoueur:
            return [startPos]
        
        possibilites = []
        for cell in gameManager.iterateGrid(plateau,indexJoueur):
            state = gameManager.getAdjacents(cell[0],cell[1],plateau,indexJoueur)
            if len(state):
                for pos in state:
                    possibilites.append(pos)
        return possibilites

    @staticmethod
    def evaluateGame(plateau:Plateau,indexJoueur:int,joueur:Player):

        def iterateGrid(grid):
            for row in grid:
                for cell in row:
                    yield cell

        grid = plateau.getTab()
        score = 0
        for cell in iterateGrid(grid):
            if cell == indexJoueur:
                score += 1
        # print("------> Evaluation : ", score + len(gameManager.getBestPossibilities(plateau,indexJoueur,joueur)))
        return score + len(gameManager.getBestPossibilities(plateau,indexJoueur,joueur))


    @staticmethod
    def canPlacePiece(numPiece:int, plateau:Plateau, x, y, joueur:Player) -> list:

        piece = joueur.jouerPiece(numPiece)
        checkIf = validPlacement(piece,x,y,plateau,joueur)

        if checkIf:
            return coordsBlocs(piece,x,y)
        return [-1, -1]
               


    @staticmethod
    def getAdjacents(x:int , y:int, plateau:Plateau, indexJoueur:int) ->list:
        possibilites = []
        grid = plateau.getTab()
        pos = Position(x,y)

        if gameManager.isInGrid(pos.left) and gameManager.isInGrid(pos.top):
            if grid[pos.left[0]][pos.left[1]] != indexJoueur and grid[pos.top[0]][pos.top[1]] != indexJoueur:
                possibilites.append([pos.top[0],pos.left[1]])

        if gameManager.isInGrid(pos.left) and gameManager.isInGrid(pos.bottom):
            if grid[pos.left[0]][pos.left[1]] != indexJoueur and grid[pos.bottom[0]][pos.bottom[1]] != indexJoueur:
                possibilites.append([pos.bottom[0], pos.left[1]])

        if gameManager.isInGrid(pos.right) and gameManager.isInGrid(pos.top):
            if grid[pos.right[0]][pos.right[1]] != indexJoueur and grid[pos.top[0]][pos.top[1]] != indexJoueur:
                possibilites.append([pos.top[0], pos.right[1]])
    
        if gameManager.isInGrid(pos.right) and gameManager.isInGrid(pos.bottom):
            if grid[pos.bottom[0]][pos.bottom[1]] != indexJoueur and grid[pos.right[0]][pos.right[1]] != indexJoueur:
                possibilites.append([pos.bottom[0],pos.right[1]])

        return list( filter( lambda coords: grid[coords[0]][coords[1]] != indexJoueur, possibilites ) )
    
