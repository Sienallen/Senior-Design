"""
File: CsPlayer.py
Author: Ian Poremba (iporemba@uci.edu)
Author: Devin Reyes (devinnr@uci.edu)
Author: Allen Sien (siena@uci.edu)
Description: Contains the implementation of the players
Start date: 09/04/2022
Updated: 02/18/2023
"""



# ------------------------- Dependencies -------------------------

from CsPieces import BoardPiece

# ------------------------- Definitions --------------------------



"""
Description: Class containing all important data for each player
Parameter: color: Boolean
Function: CreatePieces: Creates the BoardPiece class objects for each player
Function: IsLackOfMaterial: Checks the player if they have mating material
"""
class Players():
    def __init__(self, color):
        self.pawn = [None for i in range(8)]  # the pawn array for BoardPiece class objects
        self.rook = [None for i in range(2)]  # the rook array for BoardPiece class objects
        self.knight = [None for i in range(2)]  # the knight array for BoardPiece class objects
        self.bishop = [None for i in range(2)]  # the bishop array for BoardPiece class objects
        self.queen = None  # the queen BoardPiece class objects
        self.king = None  # the king BoardPiece class objects
        self.color = color  # boolean for player color
        self.canCastleRight = True  # boolean for castling right
        self.canCastleLeft = True  # boolean for castling left
        self.CreatePieces()  # initializes pieces



    """
    Description: Creates the BoardPiece class objects for each player
    """
    def CreatePieces(self):
        let = "W" if self.color else "B"  # sets the correct piece name based off color
        val = 0 if self.color else 1  # initial value based on color

        for x in range(8):  # parses through the pawn array
            self.pawn[x] = BoardPiece(let + "P", 64, val + 2)

        self.rook[0] = BoardPiece(let + "R", 64, val + 4)
        self.rook[1] = BoardPiece(let + "R", 64, val + 4)
        self.knight[0] = BoardPiece(let + "N", 64, val + 8)
        self.knight[1] = BoardPiece(let + "N", 64, val + 8)
        self.bishop[0] = BoardPiece(let + "B", 64, val + 16)
        self.bishop[1] = BoardPiece(let + "B", 64, val + 16)
        self.queen = BoardPiece(let + "Q", 64, val + 32)
        self.king = BoardPiece(let + "K", 64, val + 64)



    """
    Description: Checks the player if they have mating material
    Returns: Boolean
    """
    def IsLackOfMaterial(self):
        for x in range(8):  # parses through the pawn array
            if (self.pawn[x].index != 64):  # if on the board
                return (False)

        for x in range(2):
            if (self.rook[x].index != 64):  # if on the board
                return (False)

        if (self.queen.index != 64):  # if on the board
            return (False)

        count = 0  # counting the knights and bishops

        for x in range(2):
            if (self.knight[x].index != 64):  # if on the board
                count += 1

        for x in range(2):
            if (self.bishop[x].index != 64):  # if on the board
                count += 1

        if (count > 1):
            return (False)

        return (True)



# End of File