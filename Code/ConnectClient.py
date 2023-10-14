"""
File: ConnectClient.py
Author: Ian Poremba (iporemba@uci.edu)
Author: Devin Reyes (devinnr@uci.edu)
Author: Allen Sien (siena@uci.edu)
Description: Contains the implementation of the online client
Start date: 08/27/2022
Updated: 03/15/2023
"""



# ------------------------- Dependencies -------------------------

import socket
import threading
from time import sleep
from CsGame import GamePlay
from CsConversions import IndexToRow, IndexToCol

# ------------------------- Definitions --------------------------



ip = socket.gethostbyname("raspberrypi")



"""
Description: Class for the online client containing its alias
Parameter: clientSide: Boolean
Parameter: newClient: ClientObject
Parameter: num: Integer
Function: AddMessage: Adds messages to the client
Function: SetInGame: Sets the game status of the client
Function: GetInGame: Gets the game status of the client
Function: SetAlias: Sets the alias of the client
Function: GetAlias: Gets the alias of the client
Function: SetOpponent: Sets the opponent of the client
Function: GetOpponent: Gets the opponent of the Client
Function: SetMode: Sets the mode of the client
Function: GetMode: Gets the mode of the client
Function: SetColor: Sets the color of the client
Function: GetColor: Gets the color of the client
Function: SetNum: Sets the num of the client
Function: GetNum: Gets the num of the Client
Function: SetPlayer: Sets the color of the player of the client
Function: GetPlayer: Gets the color of the player of the client
Function: ClientMove: Sets the move of the client
Function: ClientMoveBoard: Sets the move of the client 
Function: GetClientMove: Sets the move of the client
Function: ResetMove: Resets the move of the client
Function: DoneMove: Signals when the client has finished reading the move
Function: GetClientProm: Sets the promotion of the client
Function: ResetProm: Resets the promotion of the client
Function: GetOppMove: Gets the opponents move
Function: SetOppMove: Sets the opponents move
Function: Connect: Connects the client to the server
Function: ClientSend: Sends setup related messages between the client and the server
Function: ClientReceive: Receives setup related messages between the client and the server
Function: CheckWithServer: Checks username password information with the server
Function: StartDecoder: Creates the decoder thread
Function: EndDecoder: Ends the decoder thread
Function: CheckIfColor: Checks the color of a piece at an index
Funciton: ClientDecoder: Receives messages and decodes them
Function: ClientClose: closes the client
"""
class OnlineClient():
    def __init__(self, clientSide, newClient, num):
        if (clientSide):
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # the client object
            self.num = 0  # the clients number

        else:
            self.client = newClient  # the client object
            self.num = num  # the clients number
            
        self.inGame = False  # the boolean for being in game or not
        self.alias = "None"  # the string for the name of the client
        self.opponent = "None"  # the string for the name of the opponent
        self.mode = "0"  # the gamemode to be played
        self.color = "0"  # color of the client
        self.decoderThread = 0  # the message decoder thread
        self.messages = []  # the clients messages
        self.chatLock = threading.Lock()  # the message lock
        self.moveLock = threading.Lock()  # the move lock
        self.bdMvLock = threading.Lock()  # the board move lock
        self.setEvent = threading.Event()  # set move event
        self.getEvent = threading.Event()  # get move event
        self.recEvent = threading.Event()  # rec move event
        self.logEvent = threading.Event()  # log in event
        self.addEvent = threading.Event()  # add event
        self.delEvent = threading.Event()  # del event
        self.aimEvent = threading.Event()  # aim event
        self.disEvent = threading.Event()  # dis event
        self.spmEvent = threading.Event()  # spm event
        self.bmvEvent = threading.Event()  # bmv event
        self.preEvent = threading.Event()  # pre event
        self.oppMove = ""  # move from the opponent
        self.move = [64, 64]  # the move of the client
        self.bMove = [64, 64]  # the move of the client
        self.prom = "None"
        self.temp = ""  # temporary holder of the username
        self.waitStatus = False  # status if waiting for the server
        self.logStatus = False  # status of being logged in
        self.addStatus = False  # status of being added
        self.delStatus = False  # status of being deleted


    """
    Description: Adds messages to the client
    Parameter: message: String
    """
    def AddMessage(self, message):
        self.chatLock.acquire()

        if (len(self.messages) > 20):
            self.messages.pop(0)
        
        self.messages.append(message)
        self.chatLock.release()



    """
    Description: Sets the game status of the client
    Parameter: inGame: Boolean
    """
    def SetInGame(self, inGame):
        self.inGame = inGame



    """
    Description: Gets the game status of the client
    Returns: inGame: Boolean
    """
    def GetInGame(self):
        return (self.inGame)



    """
    Description: Sets the alias of the client
    Parameter: alias: String
    """
    def SetAlias(self, alias):
        self.alias = alias



    """
    Description: Gets the alias of the client
    Returns: alias: String
    """
    def GetAlias(self):
        return (self.alias)



    """
    Description: Sets the opponent of the client
    Parameter: opponent: String
    """
    def SetOpponent(self, opponent):
        self.opponent = opponent



    """
    Description: Gets the opponent of the Client
    Returns: opponent: String
    """
    def GetOpponent(self):
        return (self.opponent)



    """
    Description: Sets the mode of the client
    Parameter: mode: Char
    """
    def SetMode(self, mode):
        self.mode = mode



    """
    Description: Gets the mode of the client
    Returns: mode: Char
    """
    def GetMode(self):
        return (self.mode)



    """
    Description: Sets the color of the client
    Parameter: color: Char
    """
    def SetColor(self, color):
        self.color = color



    """
    Description: Gets the color of the client
    Returns: color: Char
    """
    def GetColor(self):
        return (self.color)



    """
    Description: Sets the num of the client
    Parameter: num: Integer
    """
    def SetNum(self, num):
        self.num = num



    """
    Description: Gets the num of the client
    Returns: num: Integer
    """
    def GetNum(self):
        return (self.num)



    """
    Description: Sets the player of the client
    Parameter: player: Boolean
    """
    def SetPlayer(self, player):
        self.player = player



    """
    Description: Gets the player of the client
    Returns: player: Boolean
    """
    def GetPlayer(self):
        return (self.player)
    


    """
    Description: Sets the move of the client
    Parameter: button: Integer
    """
    def ClientMove(self, button):
        self.moveLock.acquire()

        if (self.move[0] == 64):
            self.move[0] = int(button)
        else:
            self.move[1] = int(button)

        self.setEvent.set()  # tells the client there is now a move
        self.getEvent.wait()  # waits for the client to read the move
        self.getEvent.clear()
        self.moveLock.release()
    


    """
    Description: Sets the move of the client
    Parameter: start: Integer
    Parameter: end: Integer
    """
    def ClientMoveBoard(self, start, end):
        self.moveLock.acquire()

        self.move[0] = start

        self.setEvent.set()  # tells the client there is now a move
        self.getEvent.wait()  # waits for the client to read the move
        self.getEvent.clear()
        
        self.move[1] = end

        self.setEvent.set()  # tells the client there is now a move
        self.getEvent.wait()  # waits for the client to read the move
        self.getEvent.clear()

        self.moveLock.release()




    """
    Description: Sets the move of the client
    Returns: move[]: Integer
    """
    def GetClientMove(self):
        self.setEvent.wait()  # waits for the client to choose the move
        self.setEvent.clear()
        
        return (self.move[0] if (self.move[1] == 64) else self.move[1])
    


    """
    Description: Resets the move of the client
    """
    def ResetMove(self):
        self.move[0] = 64
        self.move[1] = 64



    """
    Description: Signals when the client has finished reading the move
    """
    def DoneMove(self):
        self.getEvent.set()  # tells the client it has read the move



    """
    Description: Sets the promotion of the client
    Returns: promtion: String
    """
    def GetClientProm(self):
        self.spmEvent.wait()  # waits for the client to choose the move
        self.spmEvent.clear()
        promtion = self.prom
        self.ResetProm()
        
        return (promtion)
    


    """
    Description: Resets the promotion of the client
    """
    def ResetProm(self):
        self.prom = "None"



    """
    Description: Gets the opponents move
    """
    def GetOppMove(self):
        self.recEvent.wait()
        self.recEvent.clear()

        return(self.oppMove)



    """
    Description: Sets the opponents move
    """
    def SetOppMove(self, oppMove):
        self.oppMove = oppMove
        self.recEvent.set()



    """
    Description: Connects the client to the server
    """
    def Connect(self):
        host = ip
        port = 9090
        self.client.connect((host, port))



    """
    Description: Sends setup related messages between the client and the server
    Parameter: message: String
    """
    def ClientSend(self, message):
        print(message)
        self.client.send(message.encode())



    """
    Description: Receives setup related messages between the client and the server
    Returns: message: String
    """
    def ClientReceive(self):
        message = self.client.recv(1024).decode()
        print(message)

        return (message)



    """
    Description: Checks username password information with the server
    Parameter: username: String
    Parameter: password: String
    Parameter: choice: String
    """
    def CheckWithServer(self, username, password, choice):
        self.waitStatus == True
        self.temp = username
        
        if (choice == "Logn"):
            self.ClientSend("SetpLogn" + username + " " + password)

        elif (choice == "Addd"):
            self.ClientSend("SetpAddd" + username + " " + password)

        elif (choice == "Dell"):
            self.ClientSend("SetpDell" + username + " " + password)

        return (True)


    
    """
    Description: Creates the decoder thread
    Parameter: sm: ScreenManager Object
    Parameter: clock: Clock object
    """ 
    def StartDecoder(self, sm, clock):
        self.decoderThread = threading.Thread(target=self.ClientDecoder, args=(sm, clock), )
        self.decoderThread.start()

        
    
    """
    Description: Ends the decoder thread
    """ 
    def EndDecoder(self):
        self.decoderThread.join()



    """
    Description: Receives messages and decodes them
    Parameter: sm: ScreenManager Object
    Parameter: clock: Clock object
    """
    def ClientDecoder(self, sm, clock):
        while (True):
            message = self.ClientReceive()
            messageLength = 0
            if(message):
                messageLength = len(message)

            if (messageLength > 3):
                if (not self.GetInGame() and message[:4] == "Setp"):
                    if (messageLength > 7):
                        if (message[4:8] == "Logn"):
                            
                            if (message[8] == "T"):
                                self.SetAlias(self.temp)
                                self.logStatus = True
                                self.logEvent.set()

                            else:
                                self.logStatus = False
                                self.logEvent.set()

                            self.waitStatus = False

                        elif (message[4:8] == "Addd"):
                            if (message[8] == "T"):
                                self.addStatus = True
                                self.addEvent.set() 

                            else:
                                self.addStatus = False
                                self.addEvent.set() 

                            self.waitStatus = False

                        elif (message[4:8] == "Dell"):
                            if (message[8] == "T"):
                                self.delStatus = True
                                self.delEvent.set() 

                            else:
                                self.delStatus = False
                                self.delEvent.set() 

                            self.waitStatus = False

                        elif (message[4:8] == "Rmve"):
                            self.client.close()
                            sleep(.05)
                            break

                        elif (message[4:8] == "Opnt"):
                            self.SetOpponent(message[8:])
                            self.SetInGame(True)
                            sm.get_screen("GameScreen").UpdateGameText(f"Playing {self.GetOpponent()}.")
                            clock.schedule_once(sm.get_screen("GameScreen").DisplayGameText)
                            gameThread = threading.Thread(target = GamePlay, args = (self, sm, clock), )
                            gameThread.start()

                elif (self.GetInGame() and message[:4] == "Endd"):
                    gameThread.join()
                    
                    if (self.GetMode() == "1" or self.GetMode() == "2" or self.GetMode() == "4"):
                        self.ClientSend("Free")

                    self.SetInGame(False)
                    self.messages = []

                elif (self.GetInGame() and message[:4] == "Chat"):
                    self.AddMessage(message[4:])
                    clock.schedule_once(sm.get_screen("GameScreen").UpdateChat)
                    
                elif (self.GetInGame() and message[:4] == "Move"):
                    self.SetOppMove(message[4:])
                    
                elif (self.GetInGame() and message[:4] == "Forf"):
                    self.ClientMove("-1")
                    
                elif (self.GetInGame() and message[:4] == "Asig"):
                    self.aimEvent.set()

                elif (self.GetInGame() and message[:4] == "Bdmv"):
                    self.ClientMoveBoard(int(message[4:6]), int(message[6:8]))
                    self.ClientSend("Bmjn")

                elif (self.GetInGame() and message[:4] == "Cpre"):
                    self.ClientSend("Cdne")
                    self.preEvent.set()

                elif (self.GetInGame() and message[:4] == "Cclr"):
                    self.ClientSend("Cclr")
                    


    """
    Description: closes the client
    """
    def ClientClose(self):
        self.ClientSend("SetpRmve")



# End of File