

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
                            print("hola")