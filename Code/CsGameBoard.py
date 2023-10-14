"""
File: CsGameBoard.py
Author: Ian Poremba (iporemba@uci.edu)
Author: Devin Reyes (devinnr@uci.edu)
Author: Allen Sien (siena@uci.edu)
Description: Contains the implementation of the game board
Start date: 08/27/2022
Updated: 02/18/2023
"""



# ------------------------- Dependencies -------------------------

from CsPieces import BoardPiece

# ------------------------- Definitions --------------------------



"""
Description: Class for the game board containing the board
Parameter: whitePlayer: Players class object
Parameter: blackPlayer: Players class object
Function: GetBoardPiece: Returns the piece at the inputted index
Function: GetPieceVal: Returns the value of the piece at the inputted index
Function: GetBoardSituation: Returns the value of the current board situation
Function: SetPieceLocations: Sets the index of the pieces on the board
"""
class GameBoard():
    def __init__(self, whitePlayer, blackPlayer):
        self.board = [whitePlayer.rook[0], whitePlayer.knight[0], whitePlayer.bishop[0], whitePlayer.queen, whitePlayer.king, whitePlayer.bishop[1], whitePlayer.knight[1], whitePlayer.rook[1],
                        whitePlayer.pawn[0], whitePlayer.pawn[1], whitePlayer.pawn[2], whitePlayer.pawn[
                        3], whitePlayer.pawn[4], whitePlayer.pawn[5], whitePlayer.pawn[6], whitePlayer.pawn[7],
                        BoardPiece(None, 64, 0), BoardPiece(None, 64, 0), BoardPiece(None, 64, 0), BoardPiece(None, 64, 0), BoardPiece(
                        None, 64, 0), BoardPiece(None, 64, 0), BoardPiece(None, 64, 0), BoardPiece(None, 64, 0),
                        BoardPiece(None, 64, 0), BoardPiece(None, 64, 0), BoardPiece(None, 64, 0), BoardPiece(None, 64, 0), BoardPiece(
                        None, 64, 0), BoardPiece(None, 64, 0), BoardPiece(None, 64, 0), BoardPiece(None, 64, 0),
                        BoardPiece(None, 64, 0), BoardPiece(None, 64, 0), BoardPiece(None, 64, 0), BoardPiece(None, 64, 0), BoardPiece(
                        None, 64, 0), BoardPiece(None, 64, 0), BoardPiece(None, 64, 0), BoardPiece(None, 64, 0),
                        BoardPiece(None, 64, 0), BoardPiece(None, 64, 0), BoardPiece(None, 64, 0), BoardPiece(None, 64, 0), BoardPiece(
                        None, 64, 0), BoardPiece(None, 64, 0), BoardPiece(None, 64, 0), BoardPiece(None, 64, 0),
                        blackPlayer.pawn[0], blackPlayer.pawn[1], blackPlayer.pawn[2], blackPlayer.pawn[
                        3], blackPlayer.pawn[4], blackPlayer.pawn[5], blackPlayer.pawn[6], blackPlayer.pawn[7],
                        blackPlayer.rook[0], blackPlayer.knight[0], blackPlayer.bishop[0], blackPlayer.queen, blackPlayer.king, blackPlayer.bishop[1], blackPlayer.knight[1], blackPlayer.rook[1]]



    """
    Description: Returns the piece at the inputted index
    Parameter: index: Integer
    Returns: piece: BoardPiece class object
    """
    def GetBoardPiece(self, index):
        piece = self.board[index]  # sets the piece to the piece at the index

        return (piece)



    """
    Description: Returns the value of the piece at the inputted index
    Parameter: index: Integer
    Returns: val: Integer
    """
    def GetPieceVal(self, index):
        val = self.board[index].value  # sets val to the value of the piece at the index

        return (val)



    """
    Description: Returns the value of the current board situation
    Returns: boardArray: 1d integer array
    """
    def GetBoardSituation(self):
        index = 0
        boardArray = [0, 0, 0, 0, 0, 0, 0, 0]  # base array to store board information

        for row in range(8):
            val = 0

            for col in range(8):
                val += self.board[index].value  # adds the value for each piece
                val *= 100
                index += 1

            boardArray[row] = val

        return (boardArray)



    """
    Description: Sets the index of the pieces on the board
    """
    def SetPieceLocations(self):
        for index in range(64):  # for each of the slots on the board
            if (self.board[index].value != 0):
                self.board[index].index = index



# End of File
