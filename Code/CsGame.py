"""
File: CsGame.py
Author: Ian Poremba (iporemba@uci.edu)
Author: Devin Reyes (devinnr@uci.edu)
Author: Allen Sien (siena@uci.edu)
Description: Contains the implementation of the games and moves
Start date: 08/30/2022
Updated: 03/15/2023
"""



# ------------------------- Dependencies -------------------------

from CsPlayer import Players
from CsPieces import BoardPiece
from CsMoveList import List
from CsGameBoard import GameBoard
from CsConversions import IndexToCol, IndexToRow, IndexToLetters, LettersToIndex, RowColtoIndex
from CsGameRules import Checkmate, InCheck
from CsPieceRules import WhichPiece, IsValidMove
from time import sleep

# ------------------------- Definitions --------------------------



"""
Description: The player game
Parameter: client: OnlineClient class object
parameter: sm: the screenmanager class object
Parameter: clock: Clock object
"""
def GamePlay(client, sm, clock):
    yourColor = True if (client.GetColor() == "0") else False
    client.SetPlayer(yourColor)
    ai = True if (client.GetMode() == "3" or client.GetMode() == "4") else False
    sm.get_screen("GameScreen").SetTurn(yourColor)
    opponent = client.GetOpponent()  # opponent that you are playing
    playerName = client.GetAlias()  # the name of the player
    whitePlayer = Players(True)  # the white class structure
    blackPlayer = Players(False)  # the black class structure
    currentPlayer = whitePlayer  # contains the player class that is up
    nextPlayer = blackPlayer  # contains the player class that is up next
    moveList = List()  # contains the empty MoveList class object
    count = 0
    isWhiteTurn = True  # tells if white is up
    board = GameBoard(whitePlayer, blackPlayer)  # sets up the board
    board.SetPieceLocations()
    sm.get_screen("GameScreen").UpdateBoard(board, client.GetPlayer())
    clock.schedule_once(sm.get_screen("GameScreen").DisplayBoard)
    client.disEvent.wait()
    client.disEvent.clear()
    started = False
    
    while (True):  # the turn loop
        capture = False
        startingSituation = board.GetBoardSituation()  # gets the position of all pieces and stores it
        end = EndGameChecks(board, currentPlayer, nextPlayer, moveList, yourColor, startingSituation, count, whitePlayer, blackPlayer, sm, client, clock)  # checks if the game is over

        if (end != ""):  # checks if the game has ended
            if (moveList.lastMove != None):
                moveList.lastMove.ending = end

            sm.get_screen("GameScreen").UpdateGameText("Game Over.")
            clock.schedule_once(sm.get_screen("GameScreen").DisplayGameText)
            clock.schedule_once(clock.schedule_once(sm.get_screen("GameScreen").UpdateForfeitName))
            moveList.PrintLog(sm, clock, started)
            break

        count += 1

        if (yourColor):
            val, capture = PlayerTurn(board, playerName, currentPlayer, nextPlayer, isWhiteTurn, moveList, capture, sm, client, clock)  # Gets the move of the player

            sm.get_screen("GameScreen").UpdateBoard(board, client.GetPlayer())
            clock.schedule_once(sm.get_screen("GameScreen").DisplayBoard)
            client.disEvent.wait()
            client.disEvent.clear()
            
            if (val == "Meff"):
                if (moveList.lastMove != None):
                    moveList.lastMove.ending = "\nGame Over you Forfeited\nYou Lose"
                
                client.ClientSend("MoveForf")

                if (started):
                    sm.get_screen("GameScreen").UpdateGameText("Game Forfeited You Lose.")

                else:
                    sm.get_screen("GameScreen").UpdateGameText("Game Called.")

                clock.schedule_once(sm.get_screen("GameScreen").DisplayGameText)
                clock.schedule_once(sm.get_screen("GameScreen").UpdateForfeitName)
                moveList.PrintLog(sm, clock, started)
                break

            elif (val == "Forf"):
                if (moveList.lastMove != None):
                    moveList.lastMove.ending = f"\nGame Over {client.GetOpponent()} Forfeited\nYou Win"
                
                if (started):
                    sm.get_screen("GameScreen").UpdateGameText("Game Forfeited You Win.")

                else:
                    sm.get_screen("GameScreen").UpdateGameText("Game Called.")

                clock.schedule_once(sm.get_screen("GameScreen").DisplayGameText)
                clock.schedule_once(sm.get_screen("GameScreen").UpdateForfeitName)
                sm.get_screen("GameScreen").SetTurn(False)
                moveList.PrintLog(sm, clock, started)
                break
            
            elif (val == "Mefa"):
                if (moveList.lastMove != None):
                    moveList.lastMove.ending = "\nGame Over you Forfeited\nYou Lose"
                
                if (started):
                    sm.get_screen("GameScreen").UpdateGameText("Game Forfeited You Lose.")

                else:
                    sm.get_screen("GameScreen").UpdateGameText("Game Called.")

                clock.schedule_once(sm.get_screen("GameScreen").DisplayGameText)
                clock.schedule_once(sm.get_screen("GameScreen").UpdateForfeitName)
                moveList.PrintLog(sm, clock, started)
                break

            if (not (ai)):
                message = (IndexToLetters(moveList.lastMove.startIndex) + IndexToLetters(moveList.lastMove.endIndex) + val)  # creates the message to be sent to the opponent
                client.ClientSend("Move" + message)  # sends the message to the opponent

        else:
            if (ai):
                capture = AiTurn(board, currentPlayer, nextPlayer, moveList, client, clock, sm)  # if theres an ai and is the opponents turn does the ais move

            else:
                end, capture = ClientReceiveTurn(board, opponent, moveList, currentPlayer, nextPlayer, isWhiteTurn, sm, client, clock)  # recieves the online opponents move if theres no ai

                if (end == "Forf"):
                    if (moveList.lastMove != None):
                        moveList.lastMove.ending = f"\nGame Over {client.GetOpponent()} Forfeited\nYou Win"
                    
                    if (started):
                        sm.get_screen("GameScreen").UpdateGameText("Game Forfeited You Win.")

                    else:
                        sm.get_screen("GameScreen").UpdateGameText("Game Called.")

                    clock.schedule_once(sm.get_screen("GameScreen").DisplayGameText)
                    clock.schedule_once(sm.get_screen("GameScreen").UpdateForfeitName)
                    moveList.PrintLog(sm, clock, started)
                    break
                
                elif (end == "Meff"):
                    if (moveList.lastMove != None):
                        moveList.lastMove.ending = "\nGame Over you Forfeited\nYou Lose"
                    
                    if (started):
                        sm.get_screen("GameScreen").UpdateGameText("Game Forfeited You Lose.")

                    else:
                        sm.get_screen("GameScreen").UpdateGameText("Game Called.")
                    
                    clock.schedule_once(sm.get_screen("GameScreen").DisplayGameText)
                    clock.schedule_once(sm.get_screen("GameScreen").UpdateForfeitName)
                    moveList.PrintLog(sm, clock, started)
                    break

        yourColor = not yourColor  # switches players turn
        sm.get_screen("GameScreen").SetTurn(yourColor)
        isWhiteTurn = not isWhiteTurn  # switches players turn
        currentPlayer = (whitePlayer if (currentPlayer == blackPlayer) else blackPlayer)  # switches current player
        nextPlayer = (whitePlayer if (currentPlayer == blackPlayer) else blackPlayer)  # switches next player
        moveList.lastMove.boardSituation = startingSituation
        started = True

        if (capture):
            count = 0

    client.ClientSend("Endd")



"""
Description: Does the checks for ending the game
Parameter: board: GameBoard class object
Parameter: currentPlayer: Player class object
Parameter: nextPlayer: Player class object
Parameter: moveList: MoveList class object
Parameter: yourColor: Boolean
Parameter: startingSituation: 1d array
Parameter: count: Integer
Parameter: whitePlayer: Player class object
Parameter: blackPlayer: Player class object
parameter: sm: the screenmanager class object
parameter: client: The client object
Parameter: clock: Clock object
Returns: end: String
"""
def EndGameChecks(board, currentPlayer, nextPlayer, moveList, yourColor, startingSituation, count, whitePlayer, blackPlayer, sm, client, clock):
    end = ""
    check = InCheck(board, currentPlayer, nextPlayer, moveList)
  
    if (Checkmate(board, currentPlayer, nextPlayer, moveList, clock, sm, client)):  # checks if the player has any moves to end the game
        if (check):  # checks if the player is in check
            moveList.DeleteTree()  # Deletes the movelist and resets the board
            sm.get_screen("GameScreen").UpdateBoard(board, client.GetPlayer())
            clock.schedule_once(sm.get_screen("GameScreen").DisplayBoard)
            client.disEvent.wait()
            client.disEvent.clear()
            end = ("\nCheckmate\nYou Lose!!!" if (yourColor) else "\nCheckmate\nYou Win!!!")
            
            return (end)

        else:
            sm.get_screen("GameScreen").UpdateBoard(board, client.GetPlayer())
            clock.schedule_once(sm.get_screen("GameScreen").DisplayBoard)
            client.disEvent.wait()
            client.disEvent.clear()
            end = "\nStalemate!\nDraw!!!"

            return (end)

    if (moveList.CheckBoardSituation(startingSituation)):
        sm.get_screen("GameScreen").UpdateBoard(board, client.GetPlayer())
        clock.schedule_once(sm.get_screen("GameScreen").DisplayBoard)
        client.disEvent.wait()
        client.disEvent.clear()
        end = "\nThreefold Repetition!\nDraw!!!"

        return (end)

    if (count == 50):
        sm.get_screen("GameScreen").UpdateBoard(board, client.GetPlayer())
        clock.schedule_once(sm.get_screen("GameScreen").DisplayBoard)
        client.disEvent.wait()
        client.disEvent.clear()
        end = "\nFifty Turn Rule!\nDraw!!!"

        return (end)

    if (whitePlayer.IsLackOfMaterial() and blackPlayer.IsLackOfMaterial()):
        sm.get_screen("GameScreen").UpdateBoard(board, client.GetPlayer())
        clock.schedule_once(sm.get_screen("GameScreen").DisplayBoard)
        client.disEvent.wait()
        client.disEvent.clear()
        end = "\nLack of mating material!\nDraw!!!"

        return (end)

    if (moveList.lastMove != None):
        moveList.lastMove.check = check

    return (end)



"""
Description: Does the players turn
Parameter: board: GameBoard class object
Parameter: playerName: String of the players name
Parameter: currentPlayer: Player class object
Parameter: nextPlayer: Player class object
Parameter: isWhiteTurn: Boolean
Parameter: moveList: MoveList class object
Parameter: capture: Boolean
parameter: sm: the screenmanager class object
parameter: client: The client object
Parameter: clock: Clock object
Returns: val: String
"""
def PlayerTurn(board, playerName, currentPlayer, nextPlayer, isWhiteTurn, moveList, capture, sm, client, clock):
    val = "none"
    capture = False
    cap = False
    castle = False
    count = 0

    if (client.GetMode() == "2" or client.GetMode() == "4"):
        sm.get_screen("GameScreen").UpdateGameText(f"{playerName} make your move and press the button.")
    
    else:
        sm.get_screen("GameScreen").UpdateGameText(f"{playerName} select a piece.")
    
    clock.schedule_once(sm.get_screen("GameScreen").DisplayGameText)
    sm.get_screen("GameScreen").UpdateBoard(board, client.GetPlayer())
    clock.schedule_once(sm.get_screen("GameScreen").DisplayBoard)
    client.disEvent.wait()
    client.disEvent.clear()
            
    while (True):  # the input loop
        client.ResetMove()
        sm.get_screen("GameScreen").UpdateBoard(board, client.GetPlayer())
        clock.schedule_once(sm.get_screen("GameScreen").DisplayBoard)
        client.disEvent.wait()
        client.disEvent.clear()

        if (client.GetMode() == "2" or client.GetMode() == "4"):
            if (count):
                client.DoneMove()
                sleep(.5)
                client.getEvent.clear()
                client.ClientSend("Cpre")
                client.preEvent.wait()
                client.preEvent.clear()

            sm.get_screen("GameScreen").UpdateGameText(f"{playerName} make your move and press the button.")
            clock.schedule_once(sm.get_screen("GameScreen").DisplayGameText)
            client.ClientSend("Sbmv")

        pieceStartIndex = client.GetClientMove() # gets the players input
        count += 1

        if (pieceStartIndex ==  -1):
            return ("Forf", False)
        
        elif (pieceStartIndex == -2):
            return ("Meff", False)
        
        elif (pieceStartIndex == -3):
            return ("Mefa", False)
        
        elif (pieceStartIndex > 63 or pieceStartIndex < 0):
            if (client.GetMode() == "2" or client.GetMode() == "4"):
                sm.get_screen("GameScreen").UpdateGameText(f"Error: Position is not on the board. \n{playerName} reset the move and press the button.")

            else:
                sm.get_screen("GameScreen").UpdateGameText(f"Error: Position is not on the board. \n{playerName} select a piece.")

            clock.schedule_once(sm.get_screen("GameScreen").DisplayGameText)
            client.DoneMove()
            continue

        if (client.GetMode() != "2" and client.GetMode() != "4"):
            pieceStartIndex = 63 - pieceStartIndex if (not currentPlayer.color) else pieceStartIndex

        moveStartCoordinates = IndexToLetters(pieceStartIndex)  # converts the input to an coordinate

        if (not board.board[pieceStartIndex].IsPiece() or isWhiteTurn != board.board[pieceStartIndex].IsPieceWhite()):  # checks if there is a piece and if the piece is the correct color at the starting location
            if (client.GetMode() == "2" or client.GetMode() == "4"):
                sm.get_screen("GameScreen").UpdateGameText(f"Error: {moveStartCoordinates}: Invalid piece. \n{playerName} reset the move and press the button.")

            else:
                sm.get_screen("GameScreen").UpdateGameText(f"Error: {moveStartCoordinates}: Invalid piece. \n{playerName} select a piece.")

            clock.schedule_once(sm.get_screen("GameScreen").DisplayGameText)
            client.DoneMove()
            continue

        client.DoneMove()
        sm.get_screen("GameScreen").UpdateGameText(f"{playerName} select a position.")
        clock.schedule_once(sm.get_screen("GameScreen").DisplayGameText)
        pieceEndIndex = client.GetClientMove() # gets the players input

        if (pieceEndIndex ==  -1):
            return ("Forf", False)
        
        elif (pieceEndIndex == -2):
            return ("Meff", False)
        
        elif (pieceStartIndex > 63 or pieceStartIndex < 0):
            if (client.GetMode() == "2" or client.GetMode() == "4"):
                sm.get_screen("GameScreen").UpdateGameText(f"Error: Position is not on the board. \n{playerName} reset the move and press the button.")

            else:
                sm.get_screen("GameScreen").UpdateGameText(f"Error: Position is not on the board. \n{playerName} select a piece.")

            clock.schedule_once(sm.get_screen("GameScreen").DisplayGameText)
            continue

        if (client.GetMode() != "2" and client.GetMode() != "4"):
            pieceEndIndex = 63 - pieceEndIndex if (not currentPlayer.color) else pieceEndIndex

        moveEndCoordinates = IndexToLetters(pieceEndIndex)  # converts the input to an coordinate
      
        if (board.board[pieceEndIndex].IsPiece() and isWhiteTurn == board.board[pieceEndIndex].IsPieceWhite()):  # checks if there is a piece and if the piece is the incorrect color at the ending location
            if (client.GetMode() == "2" or client.GetMode() == "4"):
                sm.get_screen("GameScreen").UpdateGameText(f"Error: {moveEndCoordinates}: Invalid location. \n{playerName} reset the move and press the button.")

            else:
                sm.get_screen("GameScreen").UpdateGameText(f"Error: {moveEndCoordinates}: Invalid location. \n{playerName} select a piece.")
            
            clock.schedule_once(sm.get_screen("GameScreen").DisplayGameText)
            client.DoneMove()
            continue

        if (not IsValidMove(board, int(pieceStartIndex), int(pieceEndIndex), currentPlayer, nextPlayer, moveList)):  # checks if the move is invalid
            if (client.GetMode() == "2" or client.GetMode() == "4"):
                sm.get_screen("GameScreen").UpdateGameText(f"Error: {moveStartCoordinates}{moveEndCoordinates}: Invalid move. \n{playerName} reset the move and press the button.")

            else:
                sm.get_screen("GameScreen").UpdateGameText(f"Error: {moveStartCoordinates}{moveEndCoordinates}: Invalid move. \n{playerName} select a piece.")
            
            clock.schedule_once(sm.get_screen("GameScreen").DisplayGameText)
            client.DoneMove()
            continue

        else:
            startPieceVal = board.GetPieceVal(pieceStartIndex)  # the starting pieces value
            endPieceVal = board.GetPieceVal(pieceEndIndex)  # the ending pieces value

            if (endPieceVal != 0):
                capture = True
                cap = True

            ep = False  # boolean for en passant

            if (WhichPiece(startPieceVal, "pawn")):  # checks if the starting piece is a pawn
                capture = True
              
                if (IndexToCol(pieceEndIndex) != IndexToCol(pieceStartIndex)):  # checks if the starting and ending column is unequal
                    cap = True

                    if (endPieceVal == 0):  # checks if there is no ending piece
                        ep = True

            if (WhichPiece(startPieceVal, "king") and abs(pieceEndIndex - pieceStartIndex) == 2):  # checks if the king castled
                castle = True
          
            moveList.AddMove(pieceStartIndex, pieceEndIndex, board, ep)  # adds the move to the movelist
            val = MakeMove(board, pieceStartIndex, pieceEndIndex, currentPlayer, nextPlayer, isWhiteTurn, ep, moveList, True, val, clock, sm, client)  # makes the move

            if (InCheck(board, currentPlayer, nextPlayer, moveList)):  # checks if the player is in check and redoes the turn if they are
                moveList.DeleteMove(board, currentPlayer, ep)  # deletes the temporary move
                
                if (client.GetMode() == "2" or client.GetMode() == "4"):
                    sm.get_screen("GameScreen").UpdateGameText(f"Error: {moveStartCoordinates}{moveEndCoordinates}: Can not move into check. \n{playerName} select a piece.")

                else:
                    sm.get_screen("GameScreen").UpdateGameText(f"Error: {moveStartCoordinates}{moveEndCoordinates}: Can not move into check. \n{playerName} reset the move and press the button.")
                
                clock.schedule_once(sm.get_screen("GameScreen").DisplayGameText)
                capture = False
                castle = False
                cap = False
                ep = False  # boolean for en passant
                client.DoneMove()
                continue

            break

    client.DoneMove()

    if (client.GetMode() == "1"):
        Motors(pieceStartIndex, pieceEndIndex, cap, endPieceVal, castle, client)
    
    return (val, capture)



"""
Description: Does the clients receiving turn
Parameter: board: GameBoard class object
Parameter: opponent: String
Parameter: moveList: MoveList class object
Parameter: currentPlayer: Player class object
Parameter: nextPlayer: Player class object
Parameter: isWhiteTurn: Boolean
parameter: sm: The screenmanager class object
parameter: client: The client object
Parameter: clock: Clock object
Returns: Boolean
Returns: capture: Boolean
"""
def ClientReceiveTurn(board, opponent, moveList, currentPlayer, nextPlayer, isWhiteTurn, sm, client, clock):
    sm.get_screen("GameScreen").UpdateBoard(board, client.GetPlayer())
    clock.schedule_once(sm.get_screen("GameScreen").DisplayBoard)
    client.disEvent.wait()
    client.disEvent.clear()
    capture = False
    sm.get_screen("GameScreen").UpdateGameText(f"Waiting for {opponent} to make their move.")
    clock.schedule_once(sm.get_screen("GameScreen").DisplayGameText)
    message = client.GetOppMove()

    if (message[:4] == "Forf"):
        return ("Forf", False)
    
    elif (message[:4] == "Meff"):
        return ("Meff", False)

    pieceStartIndex = LettersToIndex(message[:2])  # starting position of the move
    pieceEndIndex = LettersToIndex(message[2:4])  # ending position of the move
    val = message[4:]  # promotion value of the piece
    startPieceVal = board.GetPieceVal(pieceStartIndex)  # the starting pieces value
    endPieceVal = board.GetPieceVal(pieceEndIndex)  # the ending pieces value

    if (endPieceVal != 0):
        capture = True

    ep = False  # boolean for en passant

    if (WhichPiece(startPieceVal, "pawn")):  # checks if the starting piece is a pawn
        capture = True
      
        if (IndexToCol(pieceEndIndex) != IndexToCol(pieceStartIndex)):  # checks if the starting and ending column is unequal
            if (endPieceVal == 0):  # checks if there is no ending piece
                ep = True

    moveList.AddMove(pieceStartIndex, pieceEndIndex, board, ep)  # adds the move to the movelist
    MakeMove(board, pieceStartIndex, pieceEndIndex, currentPlayer, nextPlayer, isWhiteTurn, ep, moveList, True, val, clock, sm, client)  # makes the move

    return (False, capture)



"""
Description: Makes the inputted move on the board
Parameter: board: GameBoard class object
Parameter: startingIndex: Integer
Parameter: endingIndex: Integer
Parameter: currentPlayer: Player class
Parameter: nextPlayer: Player class
Parameter: isWhiteTurn: Boolean
Parameter: ep: Boolean
Parameter: moveList: MoveList class
Parameter: real: Boolean
Parameter: val: String
Parameter: clock: Clock object
parameter: sm: The screenmanager class object
parameter: client: The client object
Returns: val: String
"""
def MakeMove(board, startingIndex, endingIndex, currentPlayer, nextPlayer, isWhiteTurn, ep, moveList, real, val, clock, sm, client):
    if (board.board[endingIndex].IsPiece()):  # checks if the ending position is a piece
        board.board[endingIndex].index = 64
  
    startPieceVal = board.GetPieceVal(startingIndex)  # the starting pieces value
    endPieceVal = board.GetPieceVal(endingIndex)  # the ending pieces value

    if (WhichPiece(startPieceVal, "king")):  # checks if the moving piece is a king
        currentPlayer.canCastleRight = False
        currentPlayer.canCastleLeft = False

        if (endingIndex - startingIndex == 2):  # checks if the king is castling right
            board.board[startingIndex + 1] = board.board[startingIndex + 3]
            board.board[startingIndex + 3] = BoardPiece(None, 64, 0)
            board.board[startingIndex + 1].index = startingIndex + 1

        elif (endingIndex - startingIndex == -2):  # checks if the king is castling left
            board.board[startingIndex - 1] = board.board[startingIndex - 4]
            board.board[startingIndex - 4] = BoardPiece(None, 64, 0)
            board.board[startingIndex - 1].index = startingIndex - 1

    if (WhichPiece(startPieceVal, "rook")):  # checks if the starting piece is a rook
        if (isWhiteTurn):  # if the piece is the white rook
            if (startingIndex == 0):  # if the rook is on the left
                currentPlayer.canCastleLeft = False

            if (startingIndex == 7):  # if the rook is on the right
                currentPlayer.canCastleRight = False

        else:  # if the piece is the black rook
            if (startingIndex == 56):  # if the rook is on the left
                currentPlayer.canCastleLeft = False

            if (startingIndex == 63):  # if the rook is on the right
                currentPlayer.canCastleRight = False

    if (WhichPiece(endPieceVal, "rook")):  # checks if the ending piece is a rook
        if (isWhiteTurn):  # if the piece is the white rook
            if (endingIndex == 56):  # if the rook is on the left
                nextPlayer.canCastleLeft = False

            if (endingIndex == 63):  # if the rook is on the right
                nextPlayer.canCastleRight = False

        else:
            if (endingIndex == 0):  # if the rook is on the left
                nextPlayer.canCastleLeft = False

            if (endingIndex == 7):  # if the rook is on the right
                nextPlayer.canCastleRight = False

    if (WhichPiece(startPieceVal, "pawn")):  # checks if the starting piece is a pawn
      
        if (IndexToRow(endingIndex) == 0 or IndexToRow(endingIndex) == 7):  # checks if the pawn is on the last row
            moveList.lastMove.promote = True

            while (real):  # checks if this a real turn or a hypothetical move
                if (val != "rook" and val != "knight" and val != "bishop" and val != "queen"):
                    clock.schedule_once(sm.get_screen("GameScreen").promotion)
                    val = client.GetClientProm()

                if (val == "rook"):  # promotes the pawn to the inputted piece

                    board.board[startingIndex].name = "WR" if (isWhiteTurn) else "BR"
                    board.board[startingIndex].value = 4 if (isWhiteTurn) else 5

                elif (val == "knight"):

                    board.board[startingIndex].name = "WN" if (isWhiteTurn) else "BN"
                    board.board[startingIndex].value = 8 if (isWhiteTurn) else 9

                elif (val == "bishop"):

                    board.board[startingIndex].name = "WB" if (isWhiteTurn) else "BB"
                    board.board[startingIndex].value = 16 if (isWhiteTurn) else 17

                elif (val == "queen"):

                    board.board[startingIndex].name = "WQ" if (isWhiteTurn) else "BQ"
                    board.board[startingIndex].value = 32 if (isWhiteTurn) else 33

                break

    if (ep):  # if its an en passant
        if (isWhiteTurn):
            board.board[endingIndex - 8].index = 64  # removes the captured pawn
            board.board[endingIndex - 8] = BoardPiece(None, 64, 0)  # empties the captured pawns place on the board

        else:
            board.board[endingIndex + 8].index = 64  # removes the captured pawn
            board.board[endingIndex + 8] = BoardPiece(None, 64, 0)  # empties the captured pawns place on the board

    board.board[startingIndex].index = endingIndex  # moves the starting piece to the end of the board
    board.board[endingIndex] = board.board[startingIndex]  # moves the starting piece to the end location
    board.board[startingIndex] = BoardPiece(None, 64, 0)  # empties the starting position on the board

    return (val)



"""
Description: Does the Ai's turn
Parameter: board: GameBoard class object
Parameter: currentPlayer: Player class object
Parameter: nextPlayer: Player class object
Parameter: moveList: MoveList class object
parameter: client: The client object
Parameter: clock: Clock object
parameter: sm: The screenmanager class object
Returns: capture: Boolean
"""
def AiTurn(board, currentPlayer, nextPlayer, moveList, client, clock, sm):
    from CsAi import CreateTree

    cap = False
    ep = False
    capture = False
    castle = False
    start, end = CreateTree(board, currentPlayer, nextPlayer, moveList, 2, clock, sm, client) # decides the ais move

    startPieceVal = board.GetPieceVal(start)  # the ending pieces value
    endPieceVal = board.GetPieceVal(end)  # the ending pieces value
    
    if (WhichPiece(startPieceVal, "pawn")):  # if the piece is a pawn
        capture = True

        if (IndexToCol(end) != IndexToCol(start)):  # if the columns are different
            cap = True

            if (board.board[end].value == 0):  # if the pawn isn't capturing a piece
                ep = True

    if (WhichPiece(startPieceVal, "king") and abs(end - start) == 2):  # checks if the king castled
        castle = True

    if (endPieceVal != 0):
        capture = True
        cap = True

    moveList.AddMove(start, end, board, ep)  # adds the move to the movelist
    MakeMove(board, start, end, currentPlayer, nextPlayer, currentPlayer.color, ep, moveList, False, "none", clock, sm, client)  # makes the move on the board
    
    if (client.GetMode() == "4"):
        Motors(start, end, cap, endPieceVal, castle, client)

    return (capture)



"""
Description: Does controls the motors
Parameter: start: Integer
Parameter: end: Integer
Parameter: capture: Boolean
Parameter: endPieceVal: Integer
Parameter: castler: Boolean
parameter: client: The client object
"""
def Motors(start, end, capture, endPieceVal, castle, client):
    capLocation = end
    color = not client.GetPlayer() if (capture) else client.GetPlayer()
    color = "T" if (color) else "F"
    cap = "T" if (capture) else "F"
    castle = "T" if (castle) else "F"

    if (capture and endPieceVal == 0):
        endRow = IndexToRow(start)
        endCol = IndexToCol(end)
        capLocation = str(RowColtoIndex(endRow, endCol))

        if (len(capLocation) == 1):
            capLocation = "0" + capLocation

    else:
        capLocation = str(capLocation)

        if (len(capLocation) == 1):
            capLocation = "0" + capLocation

    start = str(start)
    end = str(end)

    if (len(start) == 1):
        start = "0" + start

    if (len(end) == 1):
        end = "0" + end

    client.ClientSend("Mvai" + start + end + capLocation + cap + color + castle)
    client.aimEvent.wait()
    client.aimEvent.clear()
    client.ClientSend("Mvjn")
    


# End of File