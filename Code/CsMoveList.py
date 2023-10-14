"""
File: CsMoveList.py
Author: Ian Poremba (iporemba@uci.edu)
Author: Devin Reyes (devinnr@uci.edu)
Author: Allen Sien (siena@uci.edu)
Description: Contains the implementation of the move list
Start date: 08/30/2022
Updated: 03/03/2023
"""



# ------------------------- Dependencies -------------------------

from CsPieceRules import WhichPiece
from CsPieces import BoardPiece
from CsConversions import IndexToLetters

# ------------------------- Definitions --------------------------



"""
Description: MoveNode class for containing all important individual move data
Parameter: startIndex: Integer
Parameter: endIndex: Integer
Parameter: startPiece: BoardPiece class object
Parameter: endPiece: BoardPiece class object
Parameter: previousMove: MoveNode class object
"""
class MoveNode():
    def __init__(self, startIndex, endIndex, startPiece, endPiece, previousMove):
        self.startIndex = startIndex  # moves starting index
        self.endIndex = endIndex  # moves ending index
        self.startPiece = startPiece  # piece at the start of the move
        self.endPiece = endPiece  # piece at the end of the move
        self.previousMove = previousMove  # previous move in the list
        self.nextMove = None  # the next move in the list
        self.ep = BoardPiece(None, 64, 0)  # en passant piece captured
        self.promote = False  # promotion boolean
        self.boardSituation = []  # stores the value of the board
        self.ending = ""  # ending message when game ends
        self.check = False  # boolean for if this move puts the player in check



"""
Description: List class for containing all moves
Function: AddMove: Adds moves to the end of the list
Function: DeleteMove: Deletes the last move on the move list
Function: DeleteTree: Deletes the move list
Function: CheckBoardSituation: Checks the situation on the board for threefold repetition
Function: PrintLog: Prints the log of the game
"""
class List():
    def __init__(self):
        self.lastMove = None  # MoveNode class object for the end of the list
        self.firstMove = None  # MoveNode class object for the start of the list



    """
    Description: Adds moves to the end of the list
    Parameter: startIndex: Integer
    Parameter: endIndex: Integer
    Parameter: board: GameBoard class object
    Parameter: ep: Boolean
    """
    def AddMove(self, startIndex, endIndex, board, ep):
        startPiece = board.board[startIndex]  # BoardPiece class object at the start of the move
        endPiece = board.board[endIndex]  # BoardPiece class object at the end of the move

        if (self.lastMove == None):  # if there is no last move
            self.lastMove = MoveNode(startIndex, endIndex, startPiece, endPiece, None)
            self.firstMove = self.lastMove

        else:  # if there is a last move
            temp = MoveNode(startIndex, endIndex, startPiece, endPiece, self.lastMove)  # set temp as the new move
            self.lastMove.nextMove = temp
            self.lastMove = temp

        if (ep):  # if its an en passant
            if ((board.GetBoardPiece(startIndex)).IsPieceWhite()):
                self.lastMove.ep = board.board[endIndex - 8]

            else:
                self.lastMove.ep = board.board[endIndex + 8]



    """
    Description: Deletes the last move on the move list
    Parameter: board: GameBoard class object
    Parameter: currentPlayer: player class
    Parameter: ep: boolean
    """
    def DeleteMove(self, board, currentPlayer, ep):
        last = self.lastMove

        if (self.lastMove != None):  # if there is a last move
            board.board[last.startIndex] = board.board[last.endIndex]
            board.board[last.endIndex] = last.endPiece
            board.board[last.startIndex].index = last.startIndex

            if (board.board[last.endIndex].value != 0):  # if there is a piece at the end of the move
                board.board[last.endIndex].index = last.endIndex

            if (WhichPiece(board.board[last.startIndex].value, "king")):  # if its a king that moved
                if (last.endIndex - last.startIndex == 2):  # if the king castled right
                    board.board[last.startIndex + 1] = BoardPiece(None, 64, 0)
                    board.board[last.startIndex + 3] = currentPlayer.Rook[1]
                    currentPlayer.Rook[1].index = last.startIndex + 3

                elif (last.endIndex - last.startIndex == -2):  # if the king castled left
                    board.board[last.startIndex - 1] = BoardPiece(None, 64, 0)
                    board.board[last.startIndex - 4] = currentPlayer.Rook[0]
                    currentPlayer.Rook[1].index = last.startIndex - 4

            if (ep):  # if it s an en passant
                if (currentPlayer.color):  # if its white turn
                    board.board[last.endIndex - 8] = self.lastMove.ep
                    self.lastMove.ep.index = last.endIndex - 8

                else:  # if its blacks turn
                    board.board[last.endIndex + 8] = self.lastMove.ep
                    self.lastMove.ep.index = last.endIndex + 8

            if (last.promote):  # if the piece was promoted
                board.board[last.startIndex].name = "WP" if (
                    currentPlayer.color) else "BP"
                board.board[last.startIndex].value = 2 if (
                    currentPlayer.color) else 3

            temp = last.previousMove
            del self.lastMove
            self.lastMove = temp



    """
    Description: Deletes the move list
    """
    def DeleteTree(self):
        current = self.lastMove  # sets the move to the previous move

        while (True):
            if (current.previousMove != None):  # if there is a previous move
                nextMove = current.previousMove
                del current

            else:  # if there is not a previous move
                del current
                break

            current = nextMove

        del self



    """
    Description: Checks the situation on the board for threefold repetition
    Parameter: startingSituation: 1d integer array
    Returns: Boolean
    """
    def CheckBoardSituation(self, startingSituation):
        current = self.lastMove  # sets the move to the previous move
        count = 0

        if (current == None):
            return (False)

        while (True):
            if (current.boardSituation[0] == startingSituation[0]):
                if (current.boardSituation[1] == startingSituation[1]):
                    if (current.boardSituation[2] == startingSituation[2]):
                        if (current.boardSituation[3] == startingSituation[3]):
                            if (current.boardSituation[4] == startingSituation[4]):
                                if (current.boardSituation[5] == startingSituation[5]):
                                    if (current.boardSituation[6] == startingSituation[6]):
                                        if (current.boardSituation[7] == startingSituation[7]):
                                            count += 1
                                            
                                            if (count == 2):
                                                return (True)

            if (current.previousMove != None):  # if there is a previous move
                current = current.previousMove

            else:  # if there is not a previous move
                return (False)



    """
    Description: Prints the log of the game
    parameter: sm: the screenmanager class object
    Parameter: clock: Clock object
    Parameter: started: Boolean
    """
    def PrintLog(self, sm, clock, started):
        current = self.firstMove  # sets the move to the previous move
        message = ""

        while (True):
            if (started):
                if (current != None):
                    if (current.endPiece.value == 0 and current.ep.name == None):
                        message += f"{current.startPiece.name} at {IndexToLetters(current.startIndex)} to {IndexToLetters(current.endIndex)}"  # prints the line for a regular move

                    elif (current.ep.name != None):
                        message += f"{current.startPiece.name} at {IndexToLetters(current.startIndex)} to {IndexToLetters(current.endIndex)} capturing {current.ep.name} by en passant "  # prints the line for if theres an en passant

                    else:
                        message += f"{current.startPiece.name} at {IndexToLetters(current.startIndex)} to {IndexToLetters(current.endIndex)} capturing {current.endPiece.name} "  # prints the line if a piece is captured

                    if (current.ending != ""):
                        message += "\n" + current.ending  # prints the line for if the game ended
                        break

                    elif (current.check):
                        message += "check\n"  # prints the line if the opponents gets put in check
                        current = current.nextMove

                    elif (WhichPiece(current.startPiece.value, "king")):
                        message += "castling\n"  # prints the line if the current player castles
                        current = current.nextMove

                    else:
                        message += "\n"  # goes to the next line
                        current = current.nextMove

                else:
                    break

            else:
                message += "Game called before first move."
                break

            
        sm.get_screen("GameOverScreen").UpdateLog(message)
        clock.schedule_once(sm.get_screen("GameOverScreen").DisplayLog)



# End of File