import MoveFunctions
from checks import isCheck
from Move import Move

class GameState():
    def __init__(self, player):
        self.board = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                      ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
                      ['__', '__', '__', '__', '__', '__', '__', '__'],
                      ['__', '__', '__', '__', '__', '__', '__', '__'],
                      ['__', '__', '__', '__', '__', '__', '__', '__'],
                      ['__', '__', '__', '__', '__', '__', '__', '__'],
                      ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
                      ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
        self.player = player
        self.enemy = "b" if player == "w" else "w"
        if player == 'b':
         self.board.reverse()
         for row in self.board:
             row.reverse()
        self.playerToMove = True if player == "w" else False
        self.moveLogs = []
        self.moveFunctions = {"p": MoveFunctions.getPawnMoves, "R": MoveFunctions.getRookMoves,
                              "N": MoveFunctions.getKnightMoves, "B": MoveFunctions.getBishopMoves,
                              "K": MoveFunctions.getKingMoves, "Q": MoveFunctions.getQueenMoves}
        self.playerKingLocation = (7, 4)
        self.enemyKingLocation = (0, 4)
        self.playerKingMoved = 0
        self.enemyKingMoved = 0
        self.playerCastle = False
        self.enemyCastle = False

    def makeMove(self, move : Move):
        if move.pieceMoved == '__':
            pass
        else:

            #en-passant
            if move.pieceMoved == self.player+"p" and self.board[move.endRow][move.endCol] == "__" and (
                move.endRow == move.startRow-1 and (move.endCol == move.startCol-1) or (move.endCol == move.startCol+1)
            ):
                self.board[move.endRow+1][move.endCol] = "__"
                move.enPassant = True

            elif move.pieceMoved == self.enemy+"p" and self.board[move.endRow][move.endCol] == "__" and (
                move.endRow == move.startRow+1 and (move.endCol == move.startCol-1) or (move.endCol == move.startCol+1)
            ):
                self.board[move.endRow-1][move.endCol] = "__"
                move.enPassant = True

            self.moveLogs.append(move)
            self.board[move.startRow][move.startCol] = '__'
            self.board[move.endRow][move.endCol] = move.pieceMoved

            #pawn-promotion
            if move.pieceMoved == self.player+"p" or move.pieceMoved == self.enemy+"p":
                if move.endRow == 0 and self.playerToMove or move.endRow == 7 and not self.playerToMove:
                  move.pawnPromotion = True

            # right-Castling
            if move.pieceMoved == self.player+"K" and move.endCol == move.startCol+2:
                move1 = Move((7, 7), (7, move.endCol-1), self.board)
                self.board[7][7] = '__'
                self.board[7][move.endCol-1] = self.player+"R"
                self.playerCastle = True
                move.ksCastling = True
                self.moveLogs.append(move1)
            elif move.pieceMoved == self.enemy+"K" and move.endCol == move.startCol+2:
                move1 = Move((0, 7), (0, move.endCol-1), self.board)
                self.board[0][7] = '__'
                self.board[0][move.endCol-1] = self.enemy+"R"
                self.enemyCastle = True
                move.ksCastling = True
                self.moveLogs.append(move1)

            # Left-Castling
            if move.pieceMoved == self.player+"K" and move.endCol == move.startCol-2:
                move1 = Move((7, 0), (7, move.endCol+1), self.board)
                self.board[7][0] = '__'
                self.board[7][move.endCol+1] = self.player+"R"
                self.playerCastle = True
                move.qsCastling = True
                self.moveLogs.append(move1)
            elif move.pieceMoved == self.enemy+"K" and move.endCol == move.startCol-2:
                move1 = Move((0, 0), (0, move.endCol+1), self.board)
                self.board[0][7] = '__'
                self.board[0][move.endCol+1] = self.enemy+"R"
                self.enemyCastle = True
                move.qsCastling = True
                self.moveLogs.append(move1)

            self.playerToMove = not self.playerToMove
            if move.pieceMoved == self.player+"K":
                self.playerKingLocation = (move.endRow, move.endCol)
                self.playerKingMoved+=1

            if move.pieceMoved == self.enemy+"K":
                self.enemyKingLocation = (move.endRow, move.endCol)
                self.enemyKingMoved+=1



    def undoMove(self):
        if len(self.moveLogs) != 0:
            move = self.moveLogs.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.playerToMove = not self.playerToMove

            if move.enPassant:
                if self.playerToMove:
                    self.board[move.endRow+1][move.endCol] = self.enemy+"p"
                else:
                    self.board[move.endRow-1][move.endCol] = self.player+"p"

            #Left-Castling
            if move.pieceMoved == self.player+"R" and move.endCol == self.playerKingLocation[1]-1:
                move1 = self.moveLogs[-1]
                if move1.pieceMoved == self.player+"K" and move1.endCol == move1.startCol+2:
                    move = self.moveLogs.pop()
                    self.playerCastle = False
                    self.board[move.startRow][move.startCol] = move.pieceMoved
                    self.board[move.endRow][move.endCol] = move.pieceCaptured
            elif move.pieceMoved == self.enemy+"R" and move.endCol == self.enemyKingLocation[1]-1:
                move1 = self.moveLogs[-1]
                if move1.pieceMoved == self.enemy+"K" and move1.endCol == move1.startCol+2:
                    move = self.moveLogs.pop()
                    self.enemyCastle = False
                    self.board[move.startRow][move.startCol] = move.pieceMoved
                    self.board[move.endRow][move.endCol] = move.pieceCaptured

            #Right-Castling
            if move.pieceMoved == self.player+"R" and move.endCol == self.playerKingLocation[1]+1:
                move1 = self.moveLogs[-1]
                if move1.pieceMoved == self.player+"K" and move1.endCol == move1.startCol-2:
                    move = self.moveLogs.pop()
                    self.playerCastle = False
                    self.board[move.startRow][move.startCol] = move.pieceMoved
                    self.board[move.endRow][move.endCol] = move.pieceCaptured
            elif move.pieceMoved == self.enemy+"R" and move.endCol == self.enemyKingLocation[1]+1:
                move1 = self.moveLogs[-1]
                if move1.pieceMoved == self.enemy+"K" and move1.endCol == move1.startCol-2:
                    move = self.moveLogs.pop()
                    self.enemyCastle = False
                    self.board[move.startRow][move.startCol] = move.pieceMoved
                    self.board[move.endRow][move.endCol] = move.pieceCaptured

            if move.pieceMoved == self.player+"K":
                self.playerKingLocation = (move.startRow, move.startCol)
                self.playerKingMoved-=1

            if move.pieceMoved == self.enemy+"K":
                self.enemyKingLocation = (move.startRow, move.startCol)
                self.enemyKingMoved-=1

    def getValidMoves(self, gs):
        moves = self.getAllPossibleMoves(gs)
        if gs.playerToMove:
            ally = self.player
            (Kr, Kc) = self.playerKingLocation
        else:
            ally = self.enemy
            (Kr, Kc) = self.enemyKingLocation
        if  isCheck(gs, ally, self.player, Kr, Kc):
            toBeRemoved = []
            for move in moves:
                self.makeMove(move)
                (Kr, Kc) = self.getKingLocation(ally)
                if isCheck(gs, ally, self.player, Kr, Kc):
                    toBeRemoved.append(move)
                self.undoMove()
            for move in toBeRemoved:
                moves.remove(move)
        return moves

    def getAllPossibleMoves(self, gs):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if gs.playerToMove and self.player == turn or not gs.playerToMove and self.enemy == turn:
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](gs, r, c, moves, self.player)
        return moves

    def displayPossibleMoves(self, r, c, moves):
        cells_to_be_highlighted = []
        for move in moves:
            if (r, c) == (move.startRow, move.startCol):
                cells_to_be_highlighted.append((move.endRow, move.endCol))
        return cells_to_be_highlighted

    def getKingLocation(self, ally):
        if ally == self.player:
            (Kr, Kc) = self.playerKingLocation
        else:
            (Kr, Kc) = self.enemyKingLocation

        return (Kr, Kc)
