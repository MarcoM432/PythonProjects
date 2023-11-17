import pygame as p

class gameState ():
    def __init__ (self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]

        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves, 'B': self.getBishopMoves, 'N': self.getKnightMoves, 'R': self.getRookMoves}
        self.whiteToMove = True
        self.movelog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.checkMate = False
        self.staleMate = False
        self.enPassantPossible = () #coordenadas donde la captura al paso sea hecha.
        #condiciones o entorno en el que el erroque se hace.
        self.wCastleKingside = True
        self.wCastleQueenside = True
        self.bCastleKingside = True
        self.bCastleQueenside = True
        self.castleRightsLog = [CastleRights(self.wCastleKingside, self.bCastleKingside, self.wCastleQueenside, self.bCastleQueenside)]

        """
        Permite hacer los movimientos quye son ya procesados en la clase move (no sirve para los movimientos especiales como el enroque, las promociones
        de los peones o las capturas al paso de los mismos
        """

    def makeMove(self, move):
            self.board[move.startRow][move.starCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.movelog.append(move) #registra en el log los movimientos, permitiendo deshacerlos luego.
            self.whiteToMove = not self.whiteToMove #cambia el turno
            #actualizacion de ambos reyes, el rey negro y el blanco
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.endRow, move.endCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.endRow, move.endCol)
            #si el peon se mueve dos veces, en el siguiente movimiento puede capturar al paso
            if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
                self.enPassantPossible = ((move.endRow + move.startRow) // 2, move.endCol)
            else: self.enPassantPossible = ()
            #si se realiza la captura al paso, entonces se debe actualizar el tablero para la captura
            if move.enPasssant:
                self.board[move.startRow][move.endCol] = '--'
            #promocion del peon
            if move.pawnPromotion == True:
                promotedPiece = input('\nPromocion del peon a: \nReina (Q), Alfil (B), Caballo (N) o Torre (R). \nIngresa la letra que esta entre el parentesis pero en minuscula. \nElijo: ')
                if (promotedPiece == 'q') or (promotedPiece == 'b') or (promotedPiece == 'n') or (promotedPiece == 'r'):
                    self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotedPiece.upper()
                else:
                    error = True
                    while (error == True):
                     print('\nCodigo erroneo')
                     promotedPiece = input('Promocion del peon a: \nReina (Q), Alfil (B), Caballo (N) o Torre (R). \nIngresa la letra que esta entre el parentesis pero en minuscula. \nElijo: ')
                     if (promotedPiece == 'q') or (promotedPiece == 'b') or (promotedPiece == 'n') or (promotedPiece == 'r'):
                        self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotedPiece.upper()
                        error = False
            #actualizacion de los enroques y su condicion
            self.updateCastleRights(move)
            self.castleRightsLog.append(CastleRights(self.wCastleKingside, self.wCastleQueenside, self.bCastleKingside, self.bCastleQueenside))
            #movimientos del enroque
            if move. castle:
                if move.endCol - move.startCol == 2: #enroque corto.
                    self.board[move.endRow][move.endCol -1] = self.board[move.endRow][move.endCol + 1] #movimiento de la torre
                    self.board[move.endRow][move.endCol +1] = '--' #la casilla vacia dejada por la torre
                else: #enroque largo.
                    self.board[move.endRow][move.endCol +1] = self.board[move.endRow][move.endCol - 2] #movimiento de la torre
                    self.board[move.endRow][move.endCol -2] = '--' #la casilla vacia dejada por la torre
    """
    permite regresar un movimiento
    """
    def undoMove(self):
        if len(self.moveLog) != 0: #se asegura de que se haya hecho algun movimiento con anterioridad
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            #actualizacion de ambos reyes, el rey negro y el blanco
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            #deshaciendo la captura al paso.
            if move.enPassant:
                self.board[move.endRow][move.endCol] = '--' #regresa al peon a su sitio original 
                self.board[move.startRow][move.endCol] = move.pieceCaptured #regresa el peon que haya sido capturado
                self.enPassantPossible = (move.endRow, move.endCol) #habilita la captura al paso para que se realice nuevamente
            #retrocede el avance de dos casillas del peon
            if move.pieceMoved[1] =='P' and abs(move.startRow - move.endRow) == 2:
                self.enPassantPossible = ()

            #restablece las condiciones originales de 1 torre en caso de haberse movido
            self.castleRightsLog.pop() #remueve la ultima actualizacion de los movimientos
            castleRights = self.castleRightsLog[-1]
            self.wCastleKingside = castleRights.wks
            self.wCastleQueenside = castleRights.wqs
            self.bCastleKingside = castleRights.bks
            self.bCastleQueenside = castleRights.bqs

            #restableciendo el enroque.
            if move.castle:
                if move.endCol - move.startCol == 2: #flanco de rey
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1] #movimientos de la torre
                    self.board[move.endRow][move.endCol - 1] = '--' #la casilla vacia dejada por la torre
                else: #flanco de dama
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1] #movimientos de la torre
                    self.board[move.endRow][move.endCol + 1] = '--' #la casilla vacia dejada por la torre 

            self.checkMate = False
            self.staleMate = False
    
    """
    Chequeo de los movimientos considerando los jaques
    """

    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1: #al haber un jaque, se bloquea el jaque o se mueve el rey
                moves = self.getAllPossibleMoves()
                #para garantizar que se pueda poner una pieza cuyo movimiento pueda bloquear un jaque.
                check = self.checks[0] #revision de la info del jaque
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol] #la pieza que genera el jaque
                validSquares = [] #las casillas libres para el movimiento del rey
                #en caso de que sea el caballo, el rey se mueve o se captura al caballo
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol: #cuando una pieza termina clavada
                            break
                # se cuentan todos los movimientos que protegen al rey de jaque o donde el rey pueda moverse para librarse
                for i in range(len(moves)-1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow):
                           moves.remove(moves[i])
            else: #jaque por partida doble, a fuerza se debe mover el rey
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getAllPossibleMoves()
        if len(moves) == 0:
            if self.inCheck:
                self.checkMate = True
            else:
                 self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        return moves

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]

        directions = ((-1, 0), (0, -1), (1, 0), (0,1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = () #se reinician las piezas clavadas
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor:
                        if possiblePin == (): #cuando hay una pieza que esta clavada
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else: #cuando hay dos piezas
                            break 
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        if (0 <= j <= 3 and type == 'R') or \
                                (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'P' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                                (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == (): #el jaque al haber espacio libre
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break 
                            else: #se clava una pieza cuando esta en medio de un jaque
                                pins.append(possiblePin)
                                break
                        else: #en caso de no haber de jaque o amenaza de uno
                            break
                else: #fuera de limites
                    break
            #jaques del caballo
            knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
            for m in knightMoves:
                endRow = startRow + m[0]
                endCol = startCol + m[1]
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == enemyColor and endPiece[1] == 'N': #cuando el caballo ataca al rey 
                        inCheck = True
                        checks.append((endRow, endCol, m[0], m[1]))
            return inCheck, pins, checks

        """
        chequeo de todos los movimientos posibles.
        """

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #filas
            for c in range(len(self.board[r])): #columnas
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove): #el bando que tenga el turno
                    piece =  self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) #llama la funcion correspondiente al movimiento de la pieza en turno, Por ejemplo:
                        #si la pieza es el caballo (N), llamara la funcion que fue asociada al ID
        return moves

        """
        Los movimientos de las piezas, peon, torre, caballo, bishop, reyna, rey, en ese orden
        """

    def getPawnMoves(self, r, c, moves):
            """
            Esto lo que hace es verificar el estado de la pieza y si detecta que por encima de ella hay un posible jaque al rey, entonces la bloquea
            """
            piecePinned = False
            pinDirection = ()
            for i in range(len(self.pins)-1, -1, -1):
                if self.pins[i][0] == r and self.pins[i][1] == c:
                    piecePinned = True
                    pinDirection = (self.pins[i][2], self.pins[i][3])
                    self.pins.remove(self.pins[i])
                    break
            
            if self.whiteToMove:
                moveAmount = -1
                startRow = 6
                backRow = 0
                enemyColor = 'b'
            else:
                moveAmount = 1
                startRow = 1
                backRow = 7
                enemyColor = 'w'
            pawnPromotion = False

            if self.board[r + moveAmount][c] == '--': #movimientos de una casilla
                if not piecePinned or pinDirection == (moveAmount, 0):
                    if r + moveAmount == backRow:
                        pawnPromotion = True
                    moves.append(Move((r, c), (r + moveAmount, c), self.board, pawnPromotion = pawnPromotion))
                    if r == startRow and self.board[r + 2 *moveAmount][c] == "--": #movimiento en dos casillas
                        moves.append(Move((r,c), (r + 2 * moveAmount, c), self.board))
            
            if c - 1 >= 0: #captura a la izquierda
                if not piecePinned or pinDirection == (moveAmount, -1):
                    if self.board[r + moveAmount][c - 1][0] == enemyColor:
                        if r + moveAmount == backRow:
                            pawnPromotion = True
                        moves.append(Move((r, c), (r + moveAmount, c - 1), self.board, pawnPromotion = pawnPromotion))
                    if (r + moveAmount, c - 1) == self.enPassantPossible:
                        moves.append(Move((r, c), (r + moveAmount, c, -1), self.board, enPassant = True))

            if c + 1 <= 7: #captura a la derecha
                if not piecePinned or pinDirection == (moveAmount, 1):
                    if self.board[r + moveAmount][c + 1][0] == enemyColor:
                        if r + moveAmount == backRow:
                            pawnPromotion = True
                        moves.append(Move((r, c), (r + moveAmount, c + 1), self.board, pawnPromotion = pawnPromotion))
                    if (r + moveAmount, c + 1) == self.enPassantPossible:
                        moves.append(Move((r, c), (r + moveAmount, c + 1), self.board, enPassant = True))

    def getRookMoves(self, r, c, moves):
        """
        Esto lo que hace es verificar el estado de la peiza y si detecta que por encima de ella hay un posible jaque al rey, entonces la bloquea
        """
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break
        # los movimientos naturales de la pieza
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #Dentro del tablero
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], - d[1]): #evita mover la pieza en caso de que este clavado
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--": #espacio libre y valido
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor: #captura legal
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else: #evitar el fuego alidado
                            break
                else: #fuera del trablero
                    break
    def getKnightMoves(self, r, c, moves):
        """
        esto lo que hace es verificar el estado de la pieza y si detecta que por encima de ella hay un posible jaque al rey,
        entonces la bloquea
        """
        piecePinned = False
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        #los movimientos naturales de la pieza
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor: #tanto para el desplazamiento como para la captura
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        """
        Esto lo que hace es verificar el estado de la pieza y si detecta que por encima de ella hay un posible
        jaque al rey, entonces la bloquea
        """
        piecePinned = False
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        #los movimientos naturales de la pieza
        directions = ((-1, -1), (1, -1), (-1, 1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #dentro del tablero
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]): #evitar mover la pieza en caso de que este clavada.
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--": #Espacio libre y valido
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor: #captura legal
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else: #evitar el fuego aliado
                            break
                    else: ##fuera del tablero
                        break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whiteToMove else "b"
        for m in range(8):
            endRow = r + rowMoves[m]
            endCol = c + colMoves[m]
            if 0 <= endRow < 8 and 0 <=endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #tanto para el desplazamiento como para la captura
                    if allyColor == 'w': #actualizacion de las coordenadas del rey blanco
                        self.whiteKingLocation = (endRow, endCol)
                    else: #actualizacion de las coordenadas del rey negro
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    if allyColor == 'w':
                        self.whiteKingLocation = (r, c)
                    else: 
                        self.blackKingLocation = (r, c)
        self.getCastleMoves(r, c, moves, allyColor)

    def getCastleMoves(self, r, c, moves, allyColor):
        inCheck = self.sqUnderAttack(r, c, allyColor)
        if inCheck: #evita el enroque por amenaza de jaque
            return
        if (self.whiteToMove and self.wCastleKingside) or (not self.whiteToMove and self.bCastleKingside): #enroque corto
            self.getKingsideCastleMoves(r, c, moves, allyColor)
        if (self.whiteToMove and self.wCastleQueenside) or (not self.whiteToMove and self.bCastleQueenside): #enroque largo
            self.getQueensideCastleMoves(r, c, moves, allyColor)
    
    def getKingsideCastleMoves(self, r, c, moves, allycolor): #enroque corto
        if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--' and not self.sqUnderAttack(r, c + 1, allycolor) and not self.sqUnderAttack(r, c + 2, allycolor):
            moves.append(Move((r, c), (r, c + 2), self.board, castle = True))

    def getQueensideCastleMoves(self, r, c, moves, allyColor): #enroque largo
        if self.board[r][c + 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c -3] == '--' and not self.sqUnderAttack(r, c - 1, allyColor) and not self.sqUnderAttack(r, c - 2, allyColor):
            moves.append(Move((r, c), (r, c - 2), self.board, castle = True))

    def sqUnderAttack(self, r, c, allyColor):
        enemyColor = 'w' if allyColor == 'b' else 'b'
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor: # no atacar por esa direccion
                        break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        if (0 <= j <= 3 and type == 'R') or \
                            (4 <= j <= 7 and type == 'B') or \
                            (i == 1 and type == 'P' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                            (type == 'Q') or \
                            (i == 1 and type == 'K'):
                            return True
                        else: #en caso de no haber de jaque o amenaza de uno
                            break
                else: #fuera de limites
                    break
        
        #jaques del caballo
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N': #cuando el caballo ataca al rey
                    return True
        return False 

    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK': #si se mueve el rey blanco, se cancela todo enroque
            self.wCastleKingside = False
            self.wCastleQueenside = False
        elif move.pieceMoved == 'bk': # si se mueve el rey negro, se cancela todo enroque
            self.bCastleKingside = False
            self.bCastleQueenside = False
        elif move.pieceMoved == 'wR': #si se mueve la torre negra
            if move.startRow == 7:
                if move.startCol == 7: #se cancela el enroque corto
                    self.wCastleKingside = False
                elif move.startCol == 0: #se cancela el enroque largo
                    self.wCastleQueenside = False
        elif move.pieceMoved == 'bR': #si se meuve la torre negra
            if move.startRow == 0:
                if move.startCol == 7: #se cancela el enroque corto
                    self.bCastleKingside = False
                elif move.startCol == 0: #se cancela el enroque largo
                    self.bCastleQueenside = False

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.wqs = wqs
        self.bks = bks
        self.bqs = bqs
    
class Move():
    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, enPassant = False, pawnPromotion = False, castle = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.enPassant = enPassant
        self.pawnPromotion = pawnPromotion
        self.castle = castle
        if enPassant:
            self.pieceCaptured = 'bP' if self.pieceMoved == 'wP' else 'wP' #la captura al paso capturando el peon contrario
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False 

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + ', ' + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]














