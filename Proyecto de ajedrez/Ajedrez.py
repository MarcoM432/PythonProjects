import pygame as p
from pygame import draw
import engine, IntArt, time

width = height = 512
dimension = 8 #dimension del tablero
sq_Size = 512 // dimension #dimensiones de las casillas
max_fps = 15 #para las animaciones
images = {}

"""
Para incializar las iamgenes de las piezas
"""
def loadImage():
    pieces = ['bP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'wP', 'wR', 'wN', 'wB', 'wQ', 'wK']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (sq_Size, sq_Size))

def main():
    p.init()
    screen = p.display.set_mode((width,height))
    clock = p.time.Clock()
    screen.fill(p.Color("White"))
    gs = engine.gameState()
    validMoves = gs.getValidMoves()
    moveMade = False #Para cuando un movimiento sea hecho
    loadImage()
    run = True
    sqSelect = ()
    playerClick = [] #conteo de los clicks por parejas
    gameOver = False
    playerOne = True #Si el juador juega blancas, sera true, si no, no.
    playerTwo = False #igual que con playerone, pero orientado a las negras
    while run:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                run = False
            elif e.type == p.MOUSEBUTTONDOWN: #todo esto es para hacer click y que las piezas se muevan
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos() #la posicion del mouse en el eje x, y 
                    col = location[0] // sq_Size
                    row = location[1] // sq_Size
                    if sqSelect ==(row, col): #el usuario hace click dos veces en el mismo sitio y se limpian
                        sqSelect = ()
                        playerClick = []
                    else:
                        sqSelect = (row, col)
                        playerClick.append(sqSelect)
                    if len(playerClick) == 2: #despues de 2 clicks
                        move = engine.Move(playerClick[0], playerClick[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]: #Para verificar la validez de un movimiento
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                sqSelect = ()
                                playerClick = []
                        if not moveMade:
                            playerClick = [sqSelect]
            elif e.type == p.KEYDOWN: #Se deshace el movimiento hecho de pulsarse Z.
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    gameOver = False
        #Movimientos de la I.A
        if not gameOver and not humanTurn:
            time.sleep(2)
            AIMove = IntArt.findBestMove(gs, validMoves)
            if AIMove is None:
                AIMove = IntArt.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameStage(screen, gs, validMoves, sqSelect)
        #Cuando termine la partida en empate con un jaque mate.
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Victoria de las negras por jaque mate')
            else:
                drawText(screen, 'Victoria de las blancas por jaque mate')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Empate por rey ahogado')
        
        clock.tick(max_fps)
        p.display.flip()

"""
Resalte de las casillas disponibles conforme al movimiento de las piezas 
"""
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #Pieza seleccionada.
            #Resalte de las casillas elegidas.
            s = p.Surface((sq_Size, sq_Size))
            s.set_alpha(100)
            s.fill(p.color('orange'))
            screen.blit(s, (c * sq_Size, r * sq_Size))
            #resalte de los movimientos desde aquella casilla
            s.fill(p.color('blue'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (sq_Size * move.endCol, sq_Size * move.endRow))
"""
esto dibuja todos los elementos del juego, el tablero entero con piezas, el tablero y las piezas, respectivamente. el ultimo ejecuta el programa
"""
def drawGameStage(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    global colors
    colors = [p.Color("White"), p.Color("dark green")]
    for r in range(dimension): #para las filas
        for c in range(dimension): #para las columnas
            """
            esto es para pintar las casillas
            """
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * sq_Size, r * sq_Size, sq_Size, sq_Size))

def drawPieces(screen, board):
    for r in range(dimension): #Para las filas
        for c in range(dimension): #Para las columnas
            piece = board[r][c]
            if piece != "--": #para cuando la casilla no esta vacia.
                screen.blit(images[piece], p.Rect(c * sq_Size, r * sq_Size, sq_Size, sq_Size))
        
def drawText(screen, text):
    font = p.font.SysFont("Times New Roman", 28, True, False)
    textObj = font.render(text, 0, p.color('Black'))
    textLocation = p.Rect(0, 0, width, height).move(width/2 - textObj.get_width()/2, height/2 - textObj.get_height()/2)
    screen.blit(textObj, textLocation)
    textObj = font.render(text, 0, p.Color('Gray'))
    screen.blit(textObj, textLocation.move(2, 2))

if __name__ == "__main__":
    print("\n--------------------------------------------------------------------------------\nSi tienes cualquier duda respecto al juego, mira dentro de los archivos\n")
    main()



