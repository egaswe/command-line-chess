from Pawn import Pawn
from Rook import Rook
from King import King
from Bishop import Bishop
from Knight import Knight
from Queen import Queen
from Piece import Piece
from Coordinate import Coordinate as C
from termcolor import colored
import copy


WHITE = True
BLACK = False

class Board :

    def __init__(self, simple = False) :
        if not simple :
            backRowBlack = [Rook(self, BLACK), Knight(self, BLACK), Bishop(self, BLACK), King(self, BLACK), Queen(self, BLACK), Bishop(self, BLACK), Knight(self, BLACK), Rook(self, BLACK)]
            frontRowBlack = []
            for _ in range(8) :
                frontRowBlack.append(Pawn(self, BLACK))

            frontRowWhite = []
            for _ in range(8) :
                frontRowWhite.append(Pawn(self, WHITE))

            backRowWhite = [Rook(self, WHITE), Knight(self, WHITE), Bishop(self, WHITE), King(self, WHITE), Queen(self, WHITE), Bishop(self, WHITE), Knight(self, WHITE), Rook(self, WHITE)]
            self.boardArray = []
            self.boardArray.append(backRowBlack)
            self.boardArray.append(frontRowBlack)
            for _ in range(4) :
                self.boardArray.append([None] * 8)
            self.boardArray.append(frontRowWhite)
            self.boardArray.append(backRowWhite)

            self.history = []
            self.pieces = list(filter(None, [piece for sublist in self.boardArray for piece in sublist]))
            for piece in self.pieces :
                piece.updatePosition()

            self.points = 0
        elif simple :
            backRowBlack = [None, None, None, King(self, BLACK), None, None, None, None]
            frontRowBlack = [None, None, None, None, None, None, None, None]

            frontRowWhite = [None, None, None, None, None, None, None, None]

            backRowWhite = [None, None, None, King(self, WHITE), None, None, None, None]
            self.boardArray = []
            self.boardArray.append(backRowBlack)
            self.boardArray.append(frontRowBlack)
            for _ in range(4) :
                self.boardArray.append([None] * 8)
            self.boardArray.append(frontRowWhite)
            self.boardArray.append(backRowWhite)
            

            self.history = []
            self.pieces = list(filter(None, [piece for sublist in self.boardArray for piece in sublist]))
            for piece in self.pieces :
                piece.updatePosition()
            print(self.pieces)

            self.points = 0



    def __str__(self) :
        return self.makeStringRep(self.boardArray)

    def undoLastMove(self) :
        lastMove, pieceTaken = self.history.pop()
        pieceToMoveBack = self.pieceAtPosition(lastMove.newPos)
        self.movePieceToPosition(pieceToMoveBack, lastMove.oldPos)
        if pieceTaken :
            #pieceTaken.board = self
            if pieceTaken.side == WHITE :
                self.points += pieceTaken.value
            if pieceTaken.side == BLACK :
                self.points -= pieceTaken.value
            self.addPieceToPosition(pieceTaken, lastMove.newPos)
            self.pieces.append(pieceTaken)
            pieceTaken.updatePosition()

    def addMoveToHistory(self, move) :
        #self.history.append([move, copy.deepcopy(self.pieceAtPosition(move.newPos))])
        
        pieceAtNewPos = self.pieceAtPosition(move.newPos)
        if pieceAtNewPos :
            self.history.append([move, pieceAtNewPos.copy()])
            self.pieces.remove(pieceAtNewPos)
        else :
            self.history.append([move, None])

    def getCurrentSide(self) :
        return self.pieceAtPosition(self.history[-1][0].newPos).side
            
    def makeStringRep(self, boardArray) :
        stringRep = ''
        for x in range(8) :
            for y in range(8) :
                piece =  boardArray[x][y]
                if piece is not None :
                    side = piece.side
                    color = 'blue' if side == WHITE else 'red'
                pieceRep = ''
                if isinstance(piece, Pawn) :
                    pieceRep = colored('P', color)

                elif isinstance(piece, Rook) :
                    pieceRep = colored('R', color)

                elif isinstance(piece, Knight) :
                    pieceRep = colored('N', color)

                elif isinstance(piece, Bishop) :
                    pieceRep = colored('B', color)

                elif isinstance(piece, King) :
                    pieceRep = colored('K', color)

                elif isinstance(piece, Queen) :
                    pieceRep = colored('Q', color)

                else :
                    pieceRep = 'x'
                stringRep += pieceRep + ' '
            stringRep += '\n'
        return stringRep

    def rankOfPiece(self, piece) :
        return str(piece.position[1] + 1)


    def fileOfPiece(self, piece) :
        transTable = str.maketrans('01234567', 'abcdefgh')
        return str(piece.position[0]).translate(transTable)


    def getShortNotationOfMove(self, move) :
        notation = ""
        pieceToMove = self.pieceAtPosition(move.oldPos)
        pieceToTake = self.pieceAtPosition(move.newPos)

        if pieceToMove.stringRep != 'p' :
            notation += pieceToMove.stringRep

        if pieceToTake is not None :
            if pieceToMove.stringRep == 'p' :
                notation += self.fileOfPiece(pieceToMove)
            notation += 'x'

        notation += self.positionToHumanCoord(move.newPos)
        return notation
    
    def getShortNotationOfMoveWithFile(self, move) :
        #TODO: Use self.getShortNotationOfMove instead of repeating code
        notation = ""
        pieceToMove = self.pieceAtPosition(move.oldPos)
        pieceToTake = self.pieceAtPosition(move.newPos)

        if pieceToMove.stringRep != 'p' :
            notation += pieceToMove.stringRep
            notation += self.fileOfPiece(pieceToMove)

        if pieceToTake is not None :
            notation += 'x'

        notation += self.positionToHumanCoord(move.newPos)
        return notation
    
    def getShortNotationOfMoveWithRank(self, move) :
        #TODO: Use self.getShortNotationOfMove instead of repeating code
        notation = ""
        pieceToMove = self.pieceAtPosition(move.oldPos)
        pieceToTake = self.pieceAtPosition(move.newPos)

        if pieceToMove.stringRep != 'p' :
            notation += pieceToMove.stringRep
            notation += self.rankOfPiece(pieceToMove)

        if pieceToTake is not None :
            notation += 'x'

        notation += self.positionToHumanCoord(move.newPos)
        return notation

    def getShortNotationOfMoveWithFileAndRank(self, move) :
        #TODO: Use self.getShortNotationOfMove instead of repeating code
        notation = ""
        pieceToMove = self.pieceAtPosition(move.oldPos)
        pieceToTake = self.pieceAtPosition(move.newPos)

        if pieceToMove.stringRep != 'p' :
            notation += pieceToMove.stringRep
            notation += self.fileOfPiece(pieceToMove)
            notation += self.rankOfPiece(pieceToMove)
            

        if pieceToTake is not None :
            notation += 'x'

        notation += self.positionToHumanCoord(move.newPos)
        return notation
        return 



    def humanCoordToPosition(self, coord) :
        transTable = str.maketrans('abcdefgh', '12345678')
        coord = coord.translate(transTable)
        coord = [int(c)-1 for c in coord]
        pos = C(coord[0], coord[1])
        return pos
        
    def positionToHumanCoord(self, pos) :
        transTable = str.maketrans('01234567', 'abcdefgh')
        notation = str(pos[0]).translate(transTable) + str(pos[1]+1) 
        return notation

    def isValidPos(self, pos) :
        if 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7 :
            return True
        else :
            return False

    def getSideOfMove(self, move) :
        return self.pieceAtPosition(move.oldPos).side

    def getPositionOfPiece(self, piece) :
        for y in range(8) :
            for x in range(8) :
                if self.boardArray[y][x] is piece :
                    return C(x, 7-y)

    def pieceAtPosition(self, pos) :
        x, y = self.coordToLocationInArray(pos)
        return self.boardArray[x][y]

    def movePieceToPosition(self, piece, pos) :
        oldPos = piece.position
        self.addPieceToPosition(piece, pos)
        self.clearPosition(oldPos)

    def addPieceToPosition(self, piece, pos) :
        x, y = self.coordToLocationInArray(pos)
        self.boardArray[x][y] = piece
        piece.position = pos

    def clearPosition(self, pos) :
        x, y = self.coordToLocationInArray(pos)
            #self.pieces.remove(self.boardArray[x][y])
        self.boardArray[x][y] = None

        
    def coordToLocationInArray(self, pos) :
        return (7-pos[1], pos[0])

    def locationInArrayToCoord(self, loc) :
        return (loc[1], 7-loc[0])

    def makeMove(self, move) :
        self.addMoveToHistory(move)
        pieceToMove = self.pieceAtPosition(move.oldPos)
        pieceToTake = self.pieceAtPosition(move.newPos)

        if pieceToTake :
            if pieceToTake.side == WHITE :
                self.points -= pieceToTake.value
            if pieceToTake.side == BLACK :
                self.points += pieceToTake.value
            
        self.movePieceToPosition(pieceToMove, move.newPos)

    def getPointValueOfSide(self, side) :
        points = 0
        for piece in self.pieces :
            if piece.side == side :
                points += piece.value
        return points

    def getPointAdvantageOfSide(self, side) :
        if side == WHITE :
            return self.points
        if side == BLACK :
            return -self.points
        #mySideValue = self.getPointValueOfSide(side)
        #otherSideValue = self.getPointValueOfSide(not side)
        #return mySideValue - otherSideValue
        

    def checkForKings(self) :
        kingsFound = 0
        for piece in self.pieces :
            if piece.stringRep == 'K' :
                kingsFound += 1
        if kingsFound == 2 :
            return True
        else :
            return False

    def getAllMovesUnfiltered (self, side) :
        for piece in self.pieces :
            if piece.side == side :
                for move in piece.getPossibleMoves() :
                    yield move


    def testIfLegalBoard(self, side) :
        for move in self.getAllMovesUnfiltered(side) :
            self.makeMove(move)
            kingsPresent = self.checkForKings()
            self.undoLastMove()
            if kingsPresent == False :
                return False
        return True


    def moveIsLegal(self, move) :
        side = self.pieceAtPosition(move.oldPos).side 
        self.makeMove(move)
        isLegal = self.testIfLegalBoard(not side)
        self.undoLastMove()
        return isLegal  


    def getAllMovesLegal (self, side) :
        unfilteredMoves = list(self.getAllMovesUnfiltered(side))
        #print(list(unfilteredMoves))
        #print("UNFILTERED MOVES LENGTH : " + str(len(list(unfilteredMoves))))
        legalMoves = []
        for move in unfilteredMoves :
            #print("CHECKING MOVE : " + str(move))
            if self.moveIsLegal(move) :
                #print("MOVE IS LEGAL")
                legalMoves.append(move)
            #else :
                #print("MOVE IS NOT LEGAL")
        #print("RETURNING LEGAL MOVES : " + str(legalMoves))
        return legalMoves


