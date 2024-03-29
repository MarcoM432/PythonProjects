import random

pieceScore = {"K":0, "Q":10, "R":5, "B":3, "N":3, "P":1}
checkmate = 1000
stalemate = 0
DEPTH = 2

"""
Realiza un movimiento aleatorio
"""
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)- 1)]

"""
Busca el mejor movimiento posible
"""
def findBestMove(gs, validMoves):
    turnMultiplayer = 1 if gs.whiteToMove else - 1
    oppMinMaxScore = checkmate
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        oppMoves = gs.getValidMoves()
        if gs.staleMate: #si hay empate o tablas
            oppMinMaxScore = stalemate
        elif gs.checkMate: #si hay jaque mate
            oppMaxScore = -checkmate
        else:
            oppMaxScore = -checkmate
            for oppMove in oppMoves:
                gs.makeMove(oppMove)
                gs.getValidMoves()
                if gs.checkMate: #si hay empate o tablas
                    score = checkmate
                elif gs.staleMate: #si hay empate o tablas
                    score = stalemate
                else:
                    score = -turnMultiplayer * scoreMaterial(gs.board)
                if score > oppMaxScore:
                    oppMaxScore = score
                gs.undoMove()
        if oppMaxScore < oppMinMaxScore:
            oppMinMaxScore = oppMaxScore
            bestPlayerMove = playerMove
            gs.undoMove()
    return bestPlayerMove

def findBestMoveMinMax(gs, validMoves):
    global nextMove
    nextMove = None
    findBestMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    return nextMove

"""
Busca el mejor rendimiento en base al valor. Si el proximo movimiento da un mejor valor, ese sera el nuevo mejor movimiento
"""

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    if whiteToMove:
        maxScore = -checkmate
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore == score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = checkmate
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findBestMoveMinMax(gs, nextMoves, depth, -1, True)
            if score < minScore:
                minScore == score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore
"""
Un puntaje positivo si es bueno para el blanco, negativo si es bueno para el negro
"""
def scoreBoard(gs):
    if gs.checkMate: #en caso de jaque mate
        if gs.WhiteToMove:
            return -checkmate
        else: #en turno de negras.
            return checkmate #victoria para las blancas
    elif gs.staleMate: #si hay tablas
        return stalemate #empate por rey ahogado
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score = pieceScore[square[1]]
    return score

def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score
