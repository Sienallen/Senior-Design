"""
File: CsGameRules.py
Author: Ian Poremba (iporemba@uci.edu)
Author: Devin Reyes (devinnr@uci.edu)
Author: Allen Sien (siena@uci.edu)
Description: Contains the implementation of the overall games rules like check
Start date: 09/06/2022
Updated: 03/02/2023
"""



# ------------------------- Dependencies -------------------------

from CsConversions import IndexToCol, IndexToRow
from CsPieceRules import IsValidMove, WhichPiece

# ------------------------- Definitions --------------------------



"""
Description: Checks if the current player is in check
Parameter: board: GameBoard class object
Parameter: currentPlayer: Player class object
Parameter: nextPlayer: Player class object
Parameter: moveList: List class object
Returns: Boolean
"""
def InCheck(board, currentPlayer, nextPlayer, moveList):
    endIndex = currentPlayer.king.index  # the current players king location
    startIndex = nextPlayer.king.index  # the next players king location

    if (IsValidMove(board, startIndex, endIndex, nextPlayer, currentPlayer, moveList)):  # if the move from the next players king to your king is valid
        return (True)

    startIndex = nextPlayer.queen.index  # the next players queen location

    if (IsValidMove(board, startIndex, endIndex, nextPlayer, currentPlayer, moveList)):  # if the move from the next players queen to your king is valid
        return (True)

    for x in range(2):
        startIndex = nextPlayer.rook[x].index  # the next players rook location

        if (IsValidMove(board, startIndex, endIndex, nextPlayer, currentPlayer, moveList)):  # if the move from the next players rook to your king is valid
            return (True)

    for x in range(2):
        startIndex = nextPlayer.knight[x].index  # the next players knight location

        if (IsValidMove(board, startIndex, endIndex, nextPlayer, currentPlayer, moveList)):  # if the move from the next players knight to your king is valid
            return (True)

    for x in range(2):
        startIndex = nextPlayer.bishop[x].index  # the next players bishop location
        
        if (IsValidMove(board, startIndex, endIndex, nextPlayer, currentPlayer, moveList)):  # if the move from the next players bishop to your king is valid
            return (True)

    for x in range(8):
        startIndex = nextPlayer.pawn[x].index  # the next players pawn location

        if (IsValidMove(board, startIndex, endIndex, nextPlayer, currentPlayer, moveList)):  # if the move from the next players pawn to your king is valid
            return (True)

    return (False)



"""
Description: Checks if the next player can threaten an index
Parameter: board: GameBoard class object
Parameter: currentPlayer: Player class object
Parameter: nextPlayer: Player class object
Parameter: endIndex: Integer
Parameter: moveList: List class object
Returns: Boolean
"""
def canThreaten(board, currentPlayer, nextPlayer, endIndex, moveList):
    white = nextPlayer.color  # next players color
    rowEnd = IndexToRow(endIndex)
    colEnd = IndexToCol(endIndex)
    startIndex = nextPlayer.king.index  # the next players king location

    if (IsValidMove(board, startIndex, endIndex, nextPlayer, currentPlayer, moveList)):  # if the move from the next players king to your king is valid
        return (True)

    startIndex = nextPlayer.queen.index  # the next players queen location

    if (IsValidMove(board, startIndex, endIndex, nextPlayer, currentPlayer, moveList)):  # if the move from the next players queen to your king is valid
        return (True)

    for x in range(2):
        startIndex = nextPlayer.rook[x].index  # the next players rook location

        if (IsValidMove(board, startIndex, endIndex, nextPlayer, currentPlayer, moveList)):  # if the move from the next players rook to your king is valid
            return (True)

    for x in range(2):
        startIndex = nextPlayer.knight[x].index  # the next players knight location

        if (IsValidMove(board, startIndex, endIndex, nextPlayer, currentPlayer, moveList)):  # if the move from the next players knight to your king is valid
           return (True)

    for x in range(2):
        startIndex = nextPlayer.bishop[x].index  # the next players bishop location

        if (IsValidMove(board, startIndex, endIndex, nextPlayer, currentPlayer, moveList)):  # if the move from the next players bishop to your king is valid
            return (True)

    for x in range(8):
        startIndex = nextPlayer.pawn[x].index  # the next players pawn location
        rowStart = IndexToRow(startIndex)
        colStart = IndexToCol(startIndex)
        rowDif = rowEnd - rowStart
        colDif = colEnd - colStart
      
        if ((rowDif > 0 and not white) or (rowDif < 0 and white)):  # if the pawn is moving the correct direction
            return (False)

        if (1 == abs(rowDif)):  # if the pawn is moving vertically
            if (1 == abs(colDif)):  # if the pawn is moving horizontally
                return (True)

    return (False)



"""
Description: Checks if the current player is in checkmate
Parameter: board: GameBoard class object
Parameter: currentPlayer: Player class object
Parameter: nextPlayer: Player class object
Parameter: moveList: List class object
Parameter: clock: Clock object
parameter: sm: The screenmanager class object
parameter: client: The client object
Returns: Boolean
"""
def Checkmate(board, currentPlayer, nextPlayer, moveList, clock, sm, client):
    from CsGame import MakeMove

    ep = False  # sets en passant to be false

    for x in range(64):  # for all the tiles on the board
      
        if (board.board[x].IsPiece() and currentPlayer.color == board.board[x].IsPieceWhite()):  # if it is a piece and it is the current players piece
            for y in range(64):  # for all the rest of the tiles on the board
                if (IsValidMove(board, int(x), int(y), currentPlayer, nextPlayer, moveList)):  # if if is a valid move
                    if (WhichPiece(board.board[x].value, "pawn")):  # if the piece is a pawn
                        if (IndexToCol(y) != IndexToCol(x)):  # if the columns are different
                            if (board.board[y].value == 0):  # if the pawn isn't capturing a piece
                                ep = True

                    moveList.AddMove(x, y, board, ep)  # adds the move to the movelist
                    MakeMove(board, x, y, currentPlayer, nextPlayer, currentPlayer.color, ep, moveList, False, "none", clock, sm, client)  # makes the move on the board

                    if (not InCheck(board, currentPlayer, nextPlayer, moveList)):  # checks if the move does not put the current player in check
                        moveList.DeleteMove(board, currentPlayer, ep)  # deletes the move from the list

                        return (False)

                    else:
                        moveList.DeleteMove(board, currentPlayer, ep)  # deletes the move from the list

    return (True)



# End of File
