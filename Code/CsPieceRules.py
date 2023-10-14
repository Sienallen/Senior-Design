"""
File: CsPieceRules.py
Author: Ian Poremba (iporemba@uci.edu)
Author: Devin Reyes (devinnr@uci.edu)
Author: Allen Sien (siena@uci.edu)
Description: Contains the implementation of the validations of moves for pieces
Start date: 09/04/2022
Updated: 02/19/2023
"""



# ------------------------- Dependencies -------------------------

from CsConversions import IndexToCol, IndexToRow

# ------------------------- Definitions --------------------------



"""
Description: Selects which pieces move validation to check
Parameter: board: GameBoard class object
Parameter: pieceStartIndex: Integer
Parameter: pieceEndIndex: Integer
Parameter: currentPlayer: Player class object
Parameter: nextPlayer: Player class object
Parameter: moveList: List class object
Returns: Boolean
"""
def IsValidMove(board, pieceStartIndex, pieceEndIndex, currentPlayer, nextPlayer, moveList):
    if (pieceStartIndex == 64):  # if the start is not on the board
        return (False)
        
    if (pieceEndIndex >= 64 or pieceEndIndex < 0):  # if the end is not on the board
        return (False)

    pieceVal = board.GetPieceVal(pieceStartIndex)  # gets the pieces value
    white = board.board[pieceStartIndex].IsPieceWhite()  # checks if the piece is white

    if (pieceEndIndex == pieceStartIndex or (board.board[pieceEndIndex].IsPiece() and white == board.board[pieceEndIndex].IsPieceWhite())):  # if the piece ends the same place it starts or it is a piece and is ending on another of its own pieces
        return (False)

    if (WhichPiece(pieceVal, "pawn")):  # if the piece is a pawn
        return (IsValidPawnMove(white, board, pieceStartIndex, pieceEndIndex, moveList))

    elif (WhichPiece(pieceVal, "rook")):  # if the piece is a rook
        return (IsValidRookMove(board, pieceStartIndex, pieceEndIndex))

    elif (WhichPiece(pieceVal, "knight")):  # if the piece is a knight
        return (IsValidKnightMove(pieceStartIndex, pieceEndIndex))

    elif (WhichPiece(pieceVal, "bishop")):  # if the piece is a bishop
        return (IsValidBishopMove(board, pieceStartIndex, pieceEndIndex))

    elif (WhichPiece(pieceVal, "queen")):  # if the piece is a queen
        return (IsValidQueenMove(board, pieceStartIndex, pieceEndIndex))

    elif (WhichPiece(pieceVal, "king")):  # if the piece is a king
        return (IsValidKingMove(board, pieceStartIndex, pieceEndIndex, currentPlayer, nextPlayer, moveList))



"""
Description: Verifies if the piece is the desired piece
Parameter: val: Integer
Parameter: name: String
Returns: Boolean
"""
def WhichPiece(val, name):
    if (name == "pawn" and val & 2):
        return (True)

    elif (name == "rook" and val & 4):
        return (True)

    elif (name == "knight" and val & 8):
        return (True)

    elif (name == "bishop" and val & 16):
        return (True)

    elif (name == "queen" and val & 32):
        return (True)

    elif (name == "king" and val & 64):
        return (True)

    else:
        return (False)



"""
Description: Checks if it is a valid queen rook or bishop move
Parameter: board: GameBoard class object
Parameter: pieceStartIndex: Integer
Parameter: pieceEndIndex: Integer
Returns: Boolean
"""
def IsValidQRBMove(board, pieceStartIndex, pieceEndIndex):
    if (pieceStartIndex == 64):  # if the start is not on the board
        return (False)

    if (pieceEndIndex >= 64 or pieceEndIndex < 0):  # if the end is not on the board
        return (False)

    white = board.board[pieceStartIndex].IsPieceWhite()  # checks if the piece is white

    if (pieceEndIndex == pieceStartIndex or (board.board[pieceEndIndex].IsPiece() and white == board.board[pieceEndIndex].IsPieceWhite())):  # if the piece ends the same place it starts or it is a piece and is ending on another of its own pieces
        return (False)

    return (True)



"""
Description: Checks if it is a valid pawn move
Parameter: white: Boolean
Parameter: board: GameBoard class object
Parameter: pieceStartIndex: Integer
Parameter: pieceEndIndex: Integer
Parameter: moveList: List class object
Returns: Boolean
"""
def IsValidPawnMove(white, board, pieceStartIndex, pieceEndIndex, moveList):
    rowStart = IndexToRow(pieceStartIndex)
    colStart = IndexToCol(pieceStartIndex)
    rowEnd = IndexToRow(pieceEndIndex)
    colEnd = IndexToCol(pieceEndIndex)
    rowDif = rowEnd - rowStart
    colDif = colEnd - colStart
    
    if ((rowDif > 0 and not white) or (rowDif < 0 and white)):  # if it is moving in the correct direction
        return (False)

    if (1 == abs(rowDif)):  # if it is moving one row
        if (1 == abs(colDif)):  # if it is moving one column
            if (board.board[pieceEndIndex].IsPiece()):  # if there is a piece at the end of the move
                return (True)

            elif (moveList.lastMove != None):  # if there was a previous move
                if (abs(moveList.lastMove.endIndex - moveList.lastMove.startIndex) == 16):  # if the previous piece moved 2 rows
                    if (WhichPiece(board.board[moveList.lastMove.endIndex].value, "pawn")):  # if the last piece that was moved was a pawn
                        if (IndexToRow(pieceStartIndex) == IndexToRow(moveList.lastMove.endIndex)):  # if the last row the last pawn moved to was the same row that the current pawn moved to
                            if (IndexToCol(pieceEndIndex) == IndexToCol(moveList.lastMove.endIndex)):  # if the column the last pawn was on is the same as the column the current pawn
                                return (True)

        elif (0 == abs(colDif)):  # if the pawn is not moving horizontally
            if (not board.board[pieceEndIndex].IsPiece()):  # if there is no piece at the end of the move
                return (True)

    elif (2 == abs(rowDif) and 0 == abs(colDif)):  # if the pawn is moving 2 rows
        if ((white and rowStart == 1) or (not white and rowStart == 6)):  # if the pawn is on the starting position
            if (not board.board[pieceEndIndex].IsPiece()):  # if there is no piece at the end of the move
                if ((white and not board.board[pieceStartIndex + 8].IsPiece()) or (not white and not board.board[pieceStartIndex - 8].IsPiece())):  # if there is no piece blocking the pawn
                    return (True)

    return (False)



"""
Description: Checks if it is a valid rook move
Parameter: board: GameBoard class object
Parameter: pieceStartIndex: Integer
Parameter: pieceEndIndex: Integer
Returns: Boolean
"""
def IsValidRookMove(board, pieceStartIndex, pieceEndIndex):
    rowStart = IndexToRow(pieceStartIndex)
    colStart = IndexToCol(pieceStartIndex)
    rowEnd = IndexToRow(pieceEndIndex)
    colEnd = IndexToCol(pieceEndIndex)

    if (rowStart != rowEnd and colStart != colEnd):  # if both the column and row do not equal their original
        return (False)

    if (rowStart != rowEnd):  # if the starting and ending row do not equal
        dif = rowEnd - rowStart
        col = 0
        row = 1 if (dif > 0) else -1  # sets the vertical direction

    elif (colStart != colEnd):  # if the starting and ending column do not equal
        dif = colEnd - colStart
        row = 0
        col = 1 if (dif > 0) else -1  # sets the horizontal direction

    dif = int(abs(dif) - 1)

    for x in range(dif):  # for the distance it travels between the start and end
        if (board.board[pieceStartIndex + col * (x + 1) + 8 * row * (x + 1)].IsPiece()):  # check if there is a piece in the way
            return (False)

    return (True)



"""
Description: Checks if it is a valid knight move
Parameter: pieceStartIndex: Integer
Parameter: pieceEndIndex: Integer
Returns: Boolean
"""
def IsValidKnightMove(pieceStartIndex, pieceEndIndex):
    dif = pieceEndIndex - pieceStartIndex
    rowStart = IndexToRow(pieceStartIndex)
    colStart = IndexToCol(pieceStartIndex)

    if (dif == 17):
        if (rowStart > 5 or colStart > 6):
            return (False)

        return (True)

    elif (dif == 10):
        if (rowStart > 6 or colStart > 5):
            return (False)

        return (True)

    elif (dif == -6):
        if (rowStart < 1 or colStart > 5):
            return (False)

        return (True)

    elif (dif == -15):
        if (rowStart < 2 or colStart > 6):
            return (False)

        return (True)

    elif (dif == -17):
        if (rowStart < 2 or colStart < 1):
            return (False)

        return (True)

    elif (dif == -10):
        if (rowStart < 1 or colStart < 2):
            return (False)

        return (True)

    elif (dif == 6):
        if (rowStart > 6 or colStart < 2):
            return (False)

        return (True)

    elif (dif == 15):
        if (rowStart > 5 or colStart < 1):
            return (False)

        return (True)

    else:
        return (False)



"""
Description: Checks if it is a valid bishop move
Parameter: board: GameBoard class object
Parameter: pieceStartIndex: Integer
Parameter: pieceEndIndex: Integer
Returns: Boolean
"""
def IsValidBishopMove(board, pieceStartIndex, pieceEndIndex):
    rowStart = IndexToRow(pieceStartIndex)
    colStart = IndexToCol(pieceStartIndex)
    rowEnd = IndexToRow(pieceEndIndex)
    colEnd = IndexToCol(pieceEndIndex)
    rowDif = abs(rowEnd - rowStart)
    colDif = abs(colEnd - colStart)

    if (rowDif != colDif):  # if the piece did not move the same amount vertically as horizontally
        return (False)

    row = 1 if (rowEnd > rowStart) else -1  # sets the vertical direction
    col = 1 if (colEnd > colStart) else -1  # sets the horizontal direction
    dif = int(abs(rowDif) - 1)

    for x in range(dif):  # for the distance it travels between the start and end
        if (board.board[pieceStartIndex + col * (x + 1) + 8 * row * (x + 1)].IsPiece()):  # check if there is a piece in the way
            return (False)

    return (True)



"""
Description: Checks if it is a valid queen move
Parameter: board: GameBoard class object
Parameter: pieceStartIndex: Integer
Parameter: pieceEndIndex: Integer
Returns: Boolean
"""
def IsValidQueenMove(board, pieceStartIndex, pieceEndIndex):
    if (IsValidBishopMove(board, pieceStartIndex, pieceEndIndex) or IsValidRookMove(board, pieceStartIndex, pieceEndIndex)):  # if it is a valid rook or bishop move
        return (True)

    return (False)



"""
Description: Checks if it is a valid king move
Parameter: board: GameBoard class object
Parameter: pieceStartIndex: Integer
Parameter: pieceEndIndex: Integer
Parameter: currentPlayer: Player class object
Parameter: nextPlayer: Player class object
Parameter: moveList: List class object
Returns: Boolean
"""
def IsValidKingMove(board, pieceStartIndex, pieceEndIndex, currentPlayer, nextPlayer, moveList):
    from CsGameRules import InCheck, canThreaten

    dif = pieceEndIndex - pieceStartIndex
    rowStart = IndexToRow(pieceStartIndex)
    colStart = IndexToCol(pieceStartIndex)

    if (dif == 8):
        if (rowStart > 6):
            return (False)

        return (True)

    elif (dif == 9):
        if (rowStart > 6 or colStart > 6):
            return (False)

        return (True)

    elif (dif == 1):
        if (colStart > 6):
            return (False)

        return (True)

    elif (dif == -7):
        if (rowStart < 1 or colStart > 6):
            return (False)

        return (True)

    elif (dif == -8):
        if (rowStart < 1):
            return (False)

        return (True)

    elif (dif == -9):
        if (rowStart < 1 or colStart < 1):
            return (False)

        return (True)

    elif (dif == -1):
        if (colStart < 1):
            return (False)

        return (True)

    elif (dif == 7):
        if (rowStart > 6 or colStart < 1):
            return (False)

        return (True)

    elif (dif == -2):
        if (currentPlayer.canCastleLeft):
            if (not InCheck(board, currentPlayer, nextPlayer, moveList)):  # if the player is not in check
                if (not canThreaten(board, currentPlayer, nextPlayer, pieceStartIndex - 1, moveList)):  # if the opponent can not threaten the tile between where the player moves the king
                    if (not board.board[pieceStartIndex - 1].IsPiece() and not board.board[pieceStartIndex - 2].IsPiece() and not board.board[pieceStartIndex - 3].IsPiece()):  # if there is no piece in the way
                        return (True)

    elif (dif == 2):
        if (currentPlayer.canCastleRight):
            if (not InCheck(board, currentPlayer, nextPlayer, moveList)):  # if the player is not in check
                if (not canThreaten(board, currentPlayer, nextPlayer, pieceStartIndex + 1, moveList)):  # if the opponent can not threaten the tile between where the player moves the king
                    if (not board.board[pieceStartIndex + 1].IsPiece() and not board.board[pieceStartIndex + 2].IsPiece()):  # if there is no piece in the way
                        return (True)



# End of File