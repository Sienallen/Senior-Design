"""
File: CsPieces.py
Author: Ian Poremba (iporemba@uci.edu)
Author: Devin Reyes (devinnr@uci.edu)
Author: Allen Sien (siena@uci.edu)
Description: Contains the implementation of the pieces
Start date: 08/27/2022
Updated: 02/18/2023
"""



# ------------------------- Dependencies -------------------------



# ------------------------- Definitions --------------------------



"""
Description: Class containing the important values for each piece
Function: GetPieceIndex: Gets the pieces index on the board
Function: IsPieceWhite: Checks if the piece is black or white
Function: IsPiece: Checks if the piece is a piece
"""
class BoardPiece():
    def __init__(self, name, index, value):
        self.name = name  # name of the piece on the board
        self.index = index  # index of the piece on the board
        self.value = value  # value of the piece



    """
    Description: Gets the pieces index on the board
    Returns: index: Integer
    """
    def GetPieceIndex(self):  # for returning the pieces value
        return (self.index)



    """
    Description: Checks if the piece is black or white
    Returns: Boolean
    """
    def IsPieceWhite(self):
        bool = False if (self.value & 1) else True

        return (bool)



    """
    Description: Checks if the piece is a piece
    Returns: Boolean
    """
    def IsPiece(self):
        bool = True if (self.value > 0) else False

        return (bool)



# End of File