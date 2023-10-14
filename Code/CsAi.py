"""
File: CsAi.py
Author: Ian Poremba (iporemba@uci.edu)
Author: Devin Reyes (devinnr@uci.edu)
Author: Allen Sien (siena@uci.edu)
Description: Contains the implementation of the AI
Start date: 10/26/2022
Updated: 03/02/2023
"""


# ------------------------- Dependencies -------------------------

import time
from json.encoder import INFINITY
from CsPieceRules import WhichPiece, IsValidMove, IsValidQRBMove
from CsGameRules import InCheck
from CsConversions import IndexToCol, IndexToRow, RowColtoIndex
from CsGame import MakeMove

# ------------------------- Definitions --------------------------


"""
Description: Stores the values for each piece at each location
Function: SetValues: sets the values for each piece in their array
Function: ReturnPawnValues: Returns the value of the specific piece at the specific location for the specific player
Function: ReturnKnightValues: Returns the value of the specific piece at the specific location for the specific player
Function: ReturnBishopValues: Returns the value of the specific piece at the specific location for the specific player
Function: ReturnRookValues: Returns the value of the specific piece at the specific location for the specific player
Function: ReturnQueenValues: Returns the value of the specific piece at the specific location for the specific player
Function: ReturnKingValues: Returns the value of the specific piece at the specific location for the specific player
"""
class BoardPositionalVlues():
    def __init__(self):
        self.pawnValues = [None for i in range(64)]
        self.knightValues = [None for i in range(64)]
        self.bishopValues = [None for i in range(64)]
        self.rookValues = [None for i in range(64)]
        self.queenValues = [None for i in range(64)]
        self.kingValues = [None for i in range(64)]
        self.SetValues()


    """
    Description: sets the values for each piece in their array
    """
    def SetValues(self):
        self.pawnValues = [160, 160, 160, 160, 160, 160, 160, 160,
                            10,  10,  10,  10,  10,  10,  10,  10,
                            2,   2,   4,   6,   6,   4,   2,   2,
                            1,   1,   2,   5,   5,   2,   1,   1,
                            0,   0,   0,   4,   4,   0,   0,   0,
                            1,   4,  -2,   0,   0,  -2,   4,   1,
                            1,   2,   2,  -4,  -4,   2,   2,   1,
                            0,   0,   0,   0,   0,   0,   0,   0]

        self.knightValues = [-10,  -8,  -6,  -6,  -6,  -6,  -8, -10,
                            -8,  -4,   0,   0,   0,   0,  -4,  -8,
                            -6,   0,   2,   3,   3,   2,   0,  -6,
                            -6,   1,   3,   4,   4,   3,   1,  -6,
                            -6,   0,   3,   4,   4,   3,   0,  -6,
                            -6,   1,   2,   3,   3,   2,   1,  -6,
                            -8,  -4,   0,   1,   1,   0,  -4,  -8,
                            -10,  -8,  -6,  -6,  -6,  -6,  -8, -10]

        self.bishopValues = [-4,  -2,  -2,  -2,  -2,  -2,  -2,  -4,
                            -2,   0,   0,   0,   0,   0,   0,  -2,
                            -2,   0,   1,   2,   2,   1,   0,  -2,
                            -2,   1,   1,   2,   2,   1,   1,  -2,
                            -2,   0,   2,   2,   2,   2,   0,  -2,
                            -2,   2,   2,   2,   2,   2,   2,  -2,
                            -2,   1,   0,   0,   0,   0,   1,  -2,
                            -4,  -2,  -2,  -2,  -2,  -2,  -2,  -4]

        self.rookValues = [0,   0,   0,   0,   0,   0,   0,   0,
                            1,   2,   2,   2,   2,   2,   2,   1,
                            -1,   0,   0,   0,   0,   0,   0,  -1,
                            -1,   0,   0,   0,   0,   0,   0,  -1,
                            -1,   0,   0,   0,   0,   0,   0,  -1,
                            -1,   0,   0,   0,   0,   0,   0,  -1,
                            -1,   0,   0,   0,   0,   0,   0,  -1,
                            0,   0,   0,   1,   1,   0,   0,   0]

        self.queenValues = [-4,  -2,  -2,  -1,  -1,  -2,  -2,  -4,
                            -2,   0,   0,   0,   0,   0,   0,  -2,
                            -2,   0,   1,   1,   1,   1,   0,  -2,
                            -1,   0,   1,   1,   1,   1,   0,  -1,
                            -1,   0,   1,   1,   1,   1,   0,  -1,
                            -2,   0,   1,   1,   1,   1,   0,  -2,
                            -2,   0,   0,   0,   0,   0,   0,  -2,
                            -4,  -2,  -2,  -1,  -1,  -2,  -2,  -4]

        self.kingValues = [-6,  -8,  -8, -10, -10,  -8,  -8,  -6,
                            -6,  -8,  -8, -10, -10,  -8,  -8,  -6,
                            -6,  -8,  -8, -10, -10,  -8,  -8,  -6,
                            -6,  -8,  -8, -10, -10,  -8,  -8,  -6,
                            -4,  -6,  -6,  -8,  -8,  -6,  -6,  -4,
                            -2,  -4,  -4,  -4,  -4,  -4,  -4,  -2,
                            4,   4,   0,   0,   0,   0,   4,   4,
                            4,   6,   2,   0,   0,   2,   6,   4]



    """
    Description: Returns the value of the specific piece given the change in location for the specific player
    Parameter: start: Integer
    Parameter: end: Integer
    Parameter: color: boolean
    Parameter: change: boolean
    Returns: newvalue: integer
    """
    def ReturnPawnValues(self, start, end, color, change):
        if (change):
            startRow = (7 - IndexToRow(start)) if (color) else IndexToRow(start)  # swaps the row depending on the players color to get the correct orientation
            startCol = IndexToCol(start)
            startIndex = RowColtoIndex(startRow, startCol)
            endRow = (7 - IndexToRow(end)) if (color) else IndexToRow(end)  # swaps the row depending on the players color to get the correct orientation
            endCol = IndexToCol(end)
            endIndex = RowColtoIndex(endRow, endCol)
            newvalue = self.pawnValues[endIndex] - self.pawnValues[startIndex]
        else:
            endRow = (7 - IndexToRow(end)) if (color) else IndexToRow(end)  # swaps the row depending on the players color to get the correct orientation
            endCol = IndexToCol(end)
            endIndex = RowColtoIndex(endRow, endCol)
            newvalue = self.pawnValues[endIndex]
            
        return(newvalue)



    """
    Description: Returns the value of the specific piece given the change in location for the specific player
    Parameter: start: Integer
    Parameter: end: Integer
    Parameter: color: boolean
    Parameter: change: boolean
    Returns: newvalue: integer
    """
    def ReturnKnightValues(self, start, end, color, change):
        if (change):
            startRow = (7 - IndexToRow(start)) if (color) else IndexToRow(start)  # swaps the row depending on the players color to get the correct orientation
            startCol = IndexToCol(start)
            startIndex = RowColtoIndex(startRow, startCol)
            endRow = (7 - IndexToRow(end)) if (color) else IndexToRow(end)  # swaps the row depending on the players color to get the correct orientation
            endCol = IndexToCol(end)
            endIndex = RowColtoIndex(endRow, endCol)
            newvalue = self.knightValues[endIndex] - self.knightValues[startIndex]
        else:
            endRow = (7 - IndexToRow(end)) if (color) else IndexToRow(end)  # swaps the row depending on the players color to get the correct orientation
            endCol = IndexToCol(end)
            endIndex = RowColtoIndex(endRow, endCol)
            newvalue = self.knightValues[endIndex]
            
        return(newvalue)



    """
    Description: Returns the value of the specific piece given the change in location for the specific player
    Parameter: start: Integer
    Parameter: end: Integer
    Parameter: color: boolean
    Parameter: change: boolean
    Returns: newvalue: integer
    """
    def ReturnBishopValues(self, start, end, color, change):
        if (change):
            startRow = (7 - IndexToRow(start)) if (color) else IndexToRow(start)  # swaps the row depending on the players color to get the correct orientation
            startCol = IndexToCol(start)
            startIndex = RowColtoIndex(startRow, startCol)
            endRow = (7 - IndexToRow(end)) if (color) else IndexToRow(end)  # swaps the row depending on the players color to get the correct orientation
            endCol = IndexToCol(end)
            endIndex = RowColtoIndex(endRow, endCol)
            newvalue = self.bishopValues[endIndex] - self.bishopValues[startIndex]
        else:
            endRow = (7 - IndexToRow(end)) if (color) else IndexToRow(end)  # swaps the row depending on the players color to get the correct orientation
            endCol = IndexToCol(end)
            endIndex = RowColtoIndex(endRow, endCol)
            newvalue = self.bishopValues[endIndex]
            
        return(newvalue)



    """
    Description: Returns the value of the specific piece given the change in location for the specific player
    Parameter: start: Integer
    Parameter: end: Integer
    Parameter: color: boolean
    Parameter: change: boolean
    Returns: newvalue: integer
    """
    def ReturnRookValues(self, start, end, color, change):
        if (change):
            startRow = (7 - IndexToRow(start)) if (color) else IndexToRow(start)  # swaps the row depending on the players color to get the correct orientation
            startCol = IndexToCol(start)
            startIndex = RowColtoIndex(startRow, startCol)
            endRow = (7 - IndexToRow(end)) if (color) else IndexToRow(end)  # swaps the row depending on the players color to get the correct orientation
            endCol = IndexToCol(end)
            endIndex = RowColtoIndex(endRow, endCol)
            newvalue = self.rookValues[endIndex] - self.rookValues[startIndex]
        else:
            endRow = (7 - IndexToRow(end)) if (color) else IndexToRow(end)  # swaps the row depending on the players color to get the correct orientation
            endCol = IndexToCol(end)
            endIndex = RowColtoIndex(endRow, endCol)
            newvalue = self.rookValues[endIndex]
            
        return(newvalue)



    """
    Description: Returns the value of the specific piece given the change in location for the specific player
    Parameter: start: Integer
    Parameter: end: Integer
    Parameter: color: boolean
    Parameter: change: boolean
    Returns: newvalue: integer
    """
    def ReturnQueenValues(self, start, end, color, change):
        if (change):
            startRow = (7 - IndexToRow(start)) if (color) else IndexToRow(start)  # swaps the row depending on the players color to get the correct orientation
            startCol = IndexToCol(start)
            startIndex = RowColtoIndex(startRow, startCol)
            endRow = (7 - IndexToRow(end)) if (color) else IndexToRow(end)  # swaps the row depending on the players color to get the correct orientation
            endCol = IndexToCol(end)
            endIndex = RowColtoIndex(endRow, endCol)
            newvalue = self.queenValues[endIndex] - self.queenValues[startIndex]
        else:
            endRow = (7 - IndexToRow(end)) if (color) else IndexToRow(end)  # swaps the row depending on the players color to get the correct orientation
            endCol = IndexToCol(end)
            endIndex = RowColtoIndex(endRow, endCol)
            newvalue = self.queenValues[endIndex]
            
        return(newvalue)



    """
    Description: Returns the value of the specific piece given the change in location for the specific player
    Parameter: start: Integer
    Parameter: end: Integer
    Parameter: color: boolean
    Parameter: change: boolean
    Returns: newvalue: integer
    """
    def ReturnKingValues(self, start, end, color, change):
        if (change):
            startRow = (7 - IndexToRow(start)) if (color) else IndexToRow(start)  # swaps the row depending on the players color to get the correct orientation
            startCol = IndexToCol(start)
            startIndex = RowColtoIndex(startRow, startCol)
            endRow = (7 - IndexToRow(end)) if (color) else IndexToRow(end)  # swaps the row depending on the players color to get the correct orientation
            endCol = IndexToCol(end)
            endIndex = RowColtoIndex(endRow, endCol)
            newvalue = self.kingValues[endIndex] - self.kingValues[startIndex]
        else:
            endRow = (7 - IndexToRow(end)) if (color) else IndexToRow(end)  # swaps the row depending on the players color to get the correct orientation
            endCol = IndexToCol(end)
            endIndex = RowColtoIndex(endRow, endCol)
            newvalue = self.kingValues[endIndex]
            
        return(newvalue)



"""
Description: Stores the data for each move
"""
class TreeMoveNode():
    def __init__(self, startIndex, endIndex, previousMove, value):
        self.startIndex = startIndex  # moves starting index
        self.endIndex = endIndex  # moves ending index
        self.previousMove = previousMove  # previous move in the list
        self.value = value
        self.branches = []  # the next move in the list
        self.max = 10
        self.worst = 0


"""
Description: Creates the tree and initializes the ais move min max algorithm
Parameter: board: GameBoard class object
Parameter: aiPlayer: Player class object
Parameter: otherPlayer: Player class object
Parameter: moveList: MoveList class object
Parameter: levels: Integer
Returns: best.startIndex, best.endIndex: Integer
Parameter: clock: Clock object
parameter: sm: The screenmanager class object
parameter: client: The client object
"""
def CreateTree(board, aiPlayer, otherPlayer, moveList, levels, clock, sm, client):
    startTime = time.time()
    boardPV = BoardPositionalVlues()
    root = TreeMoveNode(None, None, None, 0)
    FindValidMoves(root, board, aiPlayer, otherPlayer, moveList, levels, boardPV, aiPlayer.color, clock, sm, client)  # creates a tree of all possible moves
    EvaluateTree(root, True)  # evaluates the trees move branches

    best = root.branches[0]

    for x in range(len(root.branches)):  # finds the best of the root branches
        if (root.branches[x].value > best.value):
            best = root.branches[x]

    start = best.startIndex
    end = best.endIndex

    DeleteTree(root)  # delets the tree

    del root  # deletes the root

    endTime = time.time()

    print(f"At a depth of {levels} the AI took {endTime - startTime} seconds")

    return (start, end)



"""
Description: Creates the tree and initializes the ais move min max algorithm
Parameter: root: TreeMoveNode class object
Parameter: board: GameBoard class object
Parameter: currentPlayer: Player class object
Parameter: nextPlayer: Player class object
Parameter: moveList: MoveList class object
Parameter: levels: Integer
Parameter: boardPV: BoardPositionalValues class object
Parameter: aiColor: Boolean
Parameter: clock: Clock object
parameter: sm: The screenmanager class object
parameter: client: The client object
"""
def FindValidMoves(root, board, currentPlayer, nextPlayer, moveList, levels, boardPV, aiColor, clock, sm, client):
    currentColor = currentPlayer.color  # the current players color

    startIndex = currentPlayer.king.index  # the current players king location

    CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex + 1, levels, clock, sm, client)
    CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex + 2, levels, clock, sm, client)
    CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex - 1, levels, clock, sm, client)
    CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex - 2, levels, clock, sm, client)
    CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex - 9, levels, clock, sm, client)
    CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex - 8, levels, clock, sm, client)
    CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex - 7, levels, clock, sm, client)
    CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex + 9, levels, clock, sm, client)
    CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex + 8, levels, clock, sm, client)
    CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex + 7, levels, clock, sm, client)

    startIndex = currentPlayer.queen.index  # the current players queen location

    startRow = IndexToRow(startIndex)
    startCol = IndexToCol(startIndex)

    for y in range(7 - startRow):
        if (not CheckMovesRQB(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex + (8 * (y + 1)), levels, clock, sm, client)):
            break

    for y in range(startRow):
        if (not CheckMovesRQB(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex - (8 * (y + 1)), levels, clock, sm, client)):
            break

    for y in range(7 - startCol):
        if (not CheckMovesRQB(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex + (y + 1), levels, clock, sm, client)):
            break

    for y in range(startCol):
        if (not CheckMovesRQB(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex - (y + 1), levels, clock, sm, client)):
            break

    fourtyFive = min(7 - startRow, 7 - startCol)

    for y in range(fourtyFive):
        if (not CheckMovesRQB(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex + (9 * (y + 1)), levels, clock, sm, client)):
            break
    
    oneThirtyFive = min(7 - startRow, startCol)

    for y in range(oneThirtyFive):
        if (not CheckMovesRQB(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex + (7 * (y + 1)), levels, clock, sm, client)):
            break

    twoTwentyFive = min(startRow, startCol)

    for y in range(twoTwentyFive):
        if (not CheckMovesRQB(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex - (9 * (y + 1)), levels, clock, sm, client)):
            break      

    threeFifteen = min(startRow, 7 - startCol)

    for y in range(threeFifteen):
        if (not CheckMovesRQB(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex - (7 * (y + 1)), levels, clock, sm, client)):
            break

    for x in range(2):
        startIndex = currentPlayer.rook[x].index  # the current players rook location

        startRow = IndexToRow(startIndex)
        startCol = IndexToCol(startIndex)

        for y in range(7 - startRow):
            if (not CheckMovesRQB(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex + (8 * (y + 1)), levels, clock, sm, client)):
                break

        for y in range(startRow):
            if (not CheckMovesRQB(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex - (8 * (y + 1)), levels, clock, sm, client)):
                break

        for y in range(7 - startCol):
            if (not CheckMovesRQB(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex + (y + 1), levels, clock, sm, client)):
                break

        for y in range(startCol):
            if (not CheckMovesRQB(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex - (y + 1), levels, clock, sm, client)):
                break

    for x in range(2):
        startIndex = currentPlayer.knight[x].index  # the current players knight location

        CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex + 6, levels, clock, sm, client)
        CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex + 10, levels, clock, sm, client)
        CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex + 15, levels, clock, sm, client)
        CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex + 17, levels, clock, sm, client)
        CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex - 6, levels, clock, sm, client)
        CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex - 10, levels, clock, sm, client)
        CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex - 15, levels, clock, sm, client)
        CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex - 17, levels, clock, sm, client)

    for x in range(2):
        startIndex = currentPlayer.bishop[x].index  # the current players bishop location

        startRow = IndexToRow(startIndex)
        startCol = IndexToCol(startIndex)
        fourtyFive = min(7 - startRow, 7 - startCol)

        for y in range(fourtyFive):
            if (not CheckMovesRQB(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex + (9 * (y + 1)), levels, clock, sm, client)):
                break
        
        oneThirtyFive = min(7 - startRow, startCol)

        for y in range(oneThirtyFive):
            if (not CheckMovesRQB(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex + (7 * (y + 1)), levels, clock, sm, client)):
                break

        twoTwentyFive = min(startRow, startCol)

        for y in range(twoTwentyFive):
            if (not CheckMovesRQB(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex - (9 * (y + 1)), levels, clock, sm, client)):
                break      

        threeFifteen = min(startRow, 7 - startCol)

        for y in range(threeFifteen):
            if (not CheckMovesRQB(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex - (7 * (y + 1)), levels, clock, sm, client)):
                break

    for x in range(8):
        startIndex = currentPlayer.pawn[x].index  # the current players pawn location

        if (currentColor):
            CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex + 9, levels, clock, sm, client)
            CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex + 8, levels, clock, sm, client)
            CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex + 7, levels, clock, sm, client)
            CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex + 16, levels, clock, sm, client)
            
        else:
            CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex - 9, levels, clock, sm, client)
            CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex - 8, levels, clock, sm, client)
            CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex - 7, levels, clock, sm, client)
            CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, startIndex, startIndex - 16, levels, clock, sm, client)
                


"""
Description: Checks moves for pawn king knight
Parameter: board: GameBoard class object
Parameter: currentPlayer: Player class object
Parameter: nextPlayer: Player class object
Parameter: moveList: MoveList class object
Parameter: root: TreeMoveNode class objectobject
Parameter: aiColor: Boolean
Parameter: boardPV: BoardPositionalValues class 
Parameter: x: Integer
Parameter: y: Integer
Parameter: levels: Integer
Parameter: clock: Clock object
parameter: sm: The screenmanager class object
parameter: client: The client object
"""
def CheckMovesPKN(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, x, y, levels, clock, sm, client):
    ep = False

    if (IsValidMove(board, int(x), int(y), currentPlayer, nextPlayer, moveList)):  # if if is a valid move
        if (WhichPiece(board.board[x].value, "pawn")):  # if the piece is a pawn
            if (IndexToCol(y) != IndexToCol(x)):  # if the columns are different
                if (board.board[y].value == 0):  # if the pawn isn't capturing a piece
                    ep = True

        newValue = root.value + EvaluateBoardPosition(board, aiColor, boardPV, x, y, ep)  
        moveList.AddMove(x, y, board, ep)  # adds the move to the movelist
        MakeMove(board, x, y, currentPlayer, nextPlayer, currentPlayer.color, ep, moveList, False, "none", clock, sm, client)  # makes the move on the board
        
        if (InCheck(board, currentPlayer, nextPlayer, moveList)):  # checks if the move does not put the current player in check
            moveList.DeleteMove(board, currentPlayer, ep)  # deletes the move from the list
            ep = False  # boolean for en passant
            
            return (True)

        else:
            if (len(root.branches) == root.max):
                if (levels % 2 == 0):
                    if (root.worst < newValue):
                        root.branches.append(TreeMoveNode(x, y, root, newValue))
                
                else:
                    if (root.worst > newValue):
                        root.branches.append(TreeMoveNode(x, y, root, newValue))

                root.branches.append(TreeMoveNode(x, y, root, newValue))
            
            elif (len(root.branches) == 0):
                root.branches.append(TreeMoveNode(x, y, root, newValue))
                root.worst = newValue
                root.worstIndex = 0

            else:
                if (levels % 2 == 0):
                    if (root.worst < newValue):
                        root.branches.append(TreeMoveNode(x, y, root, newValue))
                
                else:
                    if (root.worst > newValue):
                        root.branches.append(TreeMoveNode(x, y, root, newValue))
            
            if (levels != 0):
                FindValidMoves(root.branches[len(root.branches) - 1], board, nextPlayer, currentPlayer, moveList, levels - 1, boardPV, aiColor, clock, sm, client)

            moveList.DeleteMove(board, currentPlayer, ep)  # deletes the move from the list

            return (False)



"""
Description: Checks moves for rook bishop and queen
Parameter: board: GameBoard class object
Parameter: currentPlayer: Player class object
Parameter: nextPlayer: Player class object
Parameter: moveList: MoveList class object
Parameter: root: TreeMoveNode class objectobject
Parameter: aiColor: Boolean
Parameter: boardPV: BoardPositionalValues class 
Parameter: x: Integer
Parameter: y: Integer
Parameter: levels: Integer
Parameter: clock: Clock object
parameter: sm: The screenmanager class object
parameter: client: The client object
"""
def CheckMovesRQB(board, currentPlayer, nextPlayer, moveList, root, aiColor, boardPV, x, y, levels, clock, sm, client):
    ep = False

    if (IsValidQRBMove(board, int(x), int(y))):  # if if is a valid move
        newValue = root.value + EvaluateBoardPosition(board, aiColor, boardPV, x, y, ep)  
        moveList.AddMove(x, y, board, ep)  # adds the move to the movelist
        MakeMove(board, x, y, currentPlayer, nextPlayer, currentPlayer.color, ep, moveList, False, "none", clock, sm, client)  # makes the move on the board
        
        if (InCheck(board, currentPlayer, nextPlayer, moveList)):  # checks if the move does not put the current player in check
            moveList.DeleteMove(board, currentPlayer, ep)  # deletes the move from the list
            
            return (True)

        else:
            root.branches.append(TreeMoveNode(x, y, root, newValue))
            
            if (levels != 0):
                FindValidMoves(root.branches[len(root.branches) - 1], board, nextPlayer, currentPlayer, moveList, levels - 1, boardPV, aiColor, clock, sm, client)

            moveList.DeleteMove(board, currentPlayer, ep)  # deletes the move from the list

            return (False)



"""
Description: Evaluates the boards moves
Parameter: board: GameBoard class object
Parameter: color: Boolean
Parameter: boardPV: BoardPositionalValues class object
Returns: positionValue: Integer
"""
def EvaluateBoardPosition(board, color, boardPV, start, end, ep):
    positionValue = 0
    startPiece = board.board[start]
    startPieceColor = startPiece.IsPieceWhite()
    endPiece = board.board[end]

    if (color == startPieceColor):
        if (WhichPiece(startPiece.value, "pawn")):
            positionValue += boardPV.ReturnPawnValues(start, end, color, True)
            
            if (ep):
                if (startPieceColor):
                    epEnd = end - 8
                else:
                    epEnd = end + 8

                endPiece = board.board[epEnd]
        elif (WhichPiece(startPiece.value, "knight")):
            positionValue += boardPV.ReturnKnightValues(start, end, color, True)
        elif (WhichPiece(startPiece.value, "bishop")):
            positionValue += boardPV.ReturnBishopValues(start, end, color, True)
        elif (WhichPiece(startPiece.value, "rook")):
            positionValue += boardPV.ReturnRookValues(start, end, color, True)
        elif (WhichPiece(startPiece.value, "queen")):
            positionValue += boardPV.ReturnQueenValues(start, end, color, True)
        else:
            positionValue += boardPV.ReturnKingValues(start, end, color, True)

            if (start - end == 2):
                positionValue += 1

        if (endPiece.IsPiece()):
            if (ep):
                end = epEnd
                
            if (WhichPiece(startPiece.value, "pawn")):
                positionValue += boardPV.ReturnPawnValues(start, end, color, False) + 10
            elif (WhichPiece(startPiece.value, "knight")):
                positionValue += boardPV.ReturnKnightValues(start, end, color, False) + 30
            elif (WhichPiece(startPiece.value, "bishop")):
                positionValue += boardPV.ReturnRookValues(start, end, color, False) + 30
            elif (WhichPiece(startPiece.value, "rook")):
                positionValue += boardPV.ReturnRookValues(start, end, color, False) + 50
            elif (WhichPiece(startPiece.value, "queen")):
                positionValue += boardPV.ReturnQueenValues(start, end, color, False) + 90
            else:
                positionValue += 1000

    else:
        if (WhichPiece(startPiece.value, "pawn")):
            positionValue -= boardPV.ReturnPawnValues(start, end, not color, True)
            
            if (ep):
                if (startPieceColor):
                    epEnd = end - 8
                else:
                    epEnd = end + 8
                    
                endPiece = board.board[epEnd]
        elif (WhichPiece(startPiece.value, "knight")):
            positionValue -= boardPV.ReturnKnightValues(start, end, not color, True)
        elif (WhichPiece(startPiece.value, "bishop")):
            positionValue -= boardPV.ReturnBishopValues(start, end, not color, True)
        elif (WhichPiece(startPiece.value, "rook")):
            positionValue -= boardPV.ReturnRookValues(start, end, not color, True)
        elif (WhichPiece(startPiece.value, "queen")):
            positionValue -= boardPV.ReturnQueenValues(start, end, not color, True)
        else:
            positionValue -= boardPV.ReturnKingValues(start, end, not color, True)

            if (start - end == 2):
                positionValue -= 1

        if (endPiece.IsPiece()):
            if (ep):
                end = epEnd

            if (WhichPiece(startPiece.value, "pawn")):
                positionValue -= boardPV.ReturnPawnValues(start, end, color, False) + 10
            elif (WhichPiece(startPiece.value, "knight")):
                positionValue -= boardPV.ReturnKnightValues(start, end, color, False) + 30
            elif (WhichPiece(startPiece.value, "bishop")):
                positionValue -= boardPV.ReturnRookValues(start, end, color, False) + 30
            elif (WhichPiece(startPiece.value, "rook")):
                positionValue -= boardPV.ReturnRookValues(start, end, color, False) + 50
            elif (WhichPiece(startPiece.value, "queen")):
                positionValue -= boardPV.ReturnQueenValues(start, end, color, False) + 90
            else:
                positionValue -= 1000

    return (positionValue)



"""
Description: Evaluates the tree
Parameter: root: TreeMoveNode class object
Parameter: aiMove: Boolean
Returns: root.value: Integer
"""
def EvaluateTree(root, aiMove):
    edge = INFINITY if (not aiMove) else -INFINITY

    length = len(root.branches)
    
    if (length > 0):
        for x in range(length):
            current = EvaluateTree(root.branches[x], not aiMove)

            if ((aiMove and (current > edge)) or (not aiMove and (current < edge))):
                edge = current

        root.value += edge

    return (root.value)



"""
Description: Deletes the tree
Parameter: root: TreeMoveNode class object
"""
def DeleteTree(root):
    for x in range(len(root.branches)):
        DeleteTree(root.branches[len(root.branches) - 1])

        del root.branches[len(root.branches) - 1]

    del root.branches
    

                
# End of File