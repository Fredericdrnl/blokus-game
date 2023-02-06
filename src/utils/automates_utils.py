from random import randint
from models.Player import Player
from models.Plateau import Plateau
from utils.game_utils import validPlacement,coordsBlocs,getDiagonals,getAdjacents
from copy import deepcopy

def managePiece(joueur:Player,plateau:Plateau,positions:list )->list:
    if len( positions ) < 1:
        return -1

    score: int = joueur.score
    pieces: list = joueur.pieces.pieces_joueurs

    possMin: dict = { 'score': 0 }
    
    for pos in positions:
        for pieceID in pieces:            
            for i in range( 4 ):
                joueur.pieces.rotate( pieceID )

                for j in range( 2 ):
                    joueur.pieces.reverse( pieceID )
                    piece: list = joueur.jouerPiece( pieceID )
                    canPlace = validPlacement( piece, pos[ 0 ], pos[ 1 ], plateau, joueur )

                    if canPlace:
                        valPiece: int = 0

                        for row in piece:
                            valPiece += row.count( 1 )

                        if possMin[ "score" ] < abs( score + valPiece ):
                            possMin = { 'x': pos[ 0 ], 'y': pos[ 1 ], 'score': score + valPiece, 'pieceID': pieceID }
                            
                        break
                    joueur.pieces.resetRotation( pieceID )

    if len( possMin ) == 1:
        return -1
    else:
        idPiece: int = possMin[ 'pieceID' ]
        x: int = possMin[ 'x' ]
        y: int = possMin[ 'y' ]

        joueur.hasPlayedPiece( idPiece )
        joueur.pieces.resetRotation( idPiece )
        return coordsBlocs( joueur.jouerPiece( idPiece ), y, x )

def adjacents( x, y, plateau: Plateau, indexJoueur: int ) -> list:
    adjs = [ [ x - 1, y ], [ x, y - 1 ], [ x, y + 1 ], [ x + 1, y ] ]

    possibilites = []
    grille = plateau.getTab()
    lg_grille: int = len( grille )
    
    if adjs[ 0 ][ 0 ] <= lg_grille and adjs[ 0 ][ 1 ] <= lg_grille and adjs[ 0 ][ 0 ] >= 0 and adjs[ 0 ][ 1 ] > 0:
        if adjs[ 1 ][ 0 ] <= lg_grille and adjs[ 1 ][ 1 ] <= lg_grille and adjs[ 1 ][ 0 ] >= 0 and adjs[ 1 ][ 1 ] >= 0:
            if grille[ adjs[ 0 ][ 0 ] ][ adjs[ 0 ][ 1 ] ] != indexJoueur and grille[ adjs[ 1 ][ 0 ] ][ adjs[ 1 ][ 1 ] ] != indexJoueur:
                possibilites.append( [ adjs[ 0 ][ 0 ], adjs[ 1 ][ 1 ] ] )
        
        if adjs[ 0 ][ 0 ] <= lg_grille and adjs[ 1 ][ 1 ] <= lg_grille and adjs[ 0 ][ 0 ] >= 0 and adjs[ 1 ][ 1 ] >= 0:
            if grille[ adjs[ 0 ][ 0 ] ][ adjs[ 2 ][ 1 ] ] != indexJoueur and grille[ adjs[ 2 ][ 0 ] ][ adjs[ 2 ][ 1 ] ] != indexJoueur:
                possibilites.append( [ adjs[ 0 ][ 0 ], adjs[ 2 ][ 1 ] ] )

    if adjs[ 3 ][ 0 ] <= lg_grille and adjs[ 3 ][ 1 ] <= lg_grille and adjs[ 3 ][ 0 ] >= 0 and adjs[ 3 ][ 1 ] >= 0:
        if adjs[ 1 ][ 0 ] <= lg_grille and adjs[ 1 ][ 1 ] <= lg_grille and adjs[ 1 ][ 0 ] >= 0 and adjs[ 1 ][ 1 ] >= 0:
            if grille[ adjs[ 3 ][ 0 ] ][ adjs[ 3 ][ 1 ] ] != indexJoueur and grille[ adjs[ 1 ][ 0 ] ][ adjs[ 1 ][ 1 ] ] != indexJoueur:
                possibilites.append( [ adjs[ 3 ][ 0 ], adjs[ 1 ][ 1 ] ] )
 
        if adjs[ 2 ][ 0 ] <= lg_grille and adjs[ 2 ][ 1 ] <= lg_grille and adjs[ 2 ][ 0 ] >= 0 and adjs[ 2 ][ 1 ] >= 0:
            if grille[ adjs[ 3 ][ 0 ] ][ adjs[ 3 ][ 1 ] ] != indexJoueur and grille[ adjs[ 2 ][ 0 ] ][ adjs[ 2 ][ 1 ] ] != indexJoueur:
                possibilites.append( [ adjs[ 3 ][ 0 ], adjs[ 2 ][ 1 ] ] )

    return list( filter( lambda coords: grille[ coords[ 0 ] ][ coords[ 1 ] ] != indexJoueur, possibilites ) )

def getPossibilities(indexJoueur:int,plateau:Plateau,joueur:Player)->list:
    p = []
    grille = plateau.getTab()
    for i,ligne in enumerate(grille):
        for j,col in enumerate(ligne):
            if col == indexJoueur:
                possibilities = adjacents(i,j,plateau,indexJoueur)
                if len(possibilities):
                    for _pos in possibilities:
                        p.append(_pos)
    if not len(p):
        return [joueur.getPositionDepart()]
    return p

def easy_automate(joueurActuel : Player,plateau : Plateau,index:int,view):

    cheminFichierPiece = "./media/pieces/" + joueurActuel.getCouleur().upper()[0] + "/1.png"

    possibilities = getPossibilities(index,plateau,joueurActuel)
    pieceBlokus = managePiece(joueurActuel,plateau,possibilities)

    if pieceBlokus != -1:
        for xpos,ypos in pieceBlokus:
            view._addToGrid(cheminFichierPiece,ypos,xpos)
            plateau.setColorOfCase(xpos,ypos,index)