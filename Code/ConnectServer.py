"""
File: ConnectServer.py
Author: Ian Poremba (iporemba@uci.edu)
Author: Devin Reyes (devinnr@uci.edu)
Author: Allen Sien (siena@uci.edu)
Description: Contains the implementation of the start of the onlineServer
Start date: 08/27/2022
Updated: 03/15/2023
"""



# ------------------------- Dependencies -------------------------

import socket
import threading
from ConnectClient import OnlineClient
import ConnectLogin
from Stepper import Move
from time import sleep
from ImageProcessing import CompareArrays, cap_pre_img as CapturePreImage, cap_post_img as CapturePostImage
from CsConversions import IndexToCol, IndexToRow
import board
import RPi.GPIO as GPIO

# ------------------------- Definitions --------------------------



"""
Description: The start of the server
"""
def StartServer():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    clientLock = threading.Lock()  # lock for the adding clients
    clientEvent = threading.Event()  # event for when a client is ready to be removed
    removeLock = threading.Lock()  # lock for removing clients
    removeEvent = threading.Event()  # event for when a client is removed
    gameLock = threading.Lock()  # lock for changing game queue
    dbLock = threading.Lock()  # lock for the database
    freeEvent = threading.Event()  # event for the board gameplay ending
    buttonEvent = threading.Event()  # event for button being pressed
    buttonBreakEvent = threading.Event()  # event to break the button thread

    clients = []  # array of clients
    clientThreads = []  # array of clients threads
    count = [0]  # array of the count of the clients
    remove = [0]  # array of the client to be removed
    locks = [clientLock, removeLock, gameLock, dbLock]  # array to hold the locks
    events = [clientEvent, removeEvent, freeEvent]  # array tp hold the events
    queue = [[], [], [], []]  # queue for clients waiting to start a game

    db = ConnectLogin.UserPassDatabase()

    port = 9090
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", port))
    server.listen()
    
    buttonThread = threading.Thread(target = Button, args = (buttonEvent, buttonBreakEvent), )
    receiveClientThread = threading.Thread(target = ReceiveClient, args = (server, clients, locks, events, clientThreads, count, remove, queue, db, buttonEvent), )
    removeClientThread = threading.Thread(target = RemoveClient, args = (clients, locks, events, clientThreads, count, remove, db, server), )
    buttonThread.start()
    receiveClientThread.start()
    removeClientThread.start()
    receiveClientThread.join()
    removeClientThread.join()
    buttonBreakEvent.set()
    buttonThread.join()

    print("serverClosed")



"""
Description: Signals when the button is pressed
Parameter: buttonEvent: Threading event object
Parameter: buttonBreakEvent: Threading event object
"""
def Button(buttonEvent, buttonBreakEvent):
    while(not buttonBreakEvent.is_set()):
        if(GPIO.input(27) == 0):
            buttonEvent.set()
            sleep(1)
            buttonEvent.clear()
            continue
        else:
            sleep(.05)
            continue



"""
Description: Connects clients to the server
Parameter: server: The server object
Parameter: clients: Array of client objects
Parameter: locks: Array of mutexes for the server
Parameter: events: Array of event Objects for the server
Parameter: clientThreads: Array of threads
Parameter: count: Array of an integer
parameter: queue: Array of queue arrays of client objects
Parameter: db: the database
Parameter: buttonEvent: Threading event object
"""
def ReceiveClient(server, clients, locks, events, clientThreads, count, remove, queue, db, buttonEvent):
    while (True):
        print("Server is running and listening")

        try:
            newClient, address = server.accept()
        except:
            break
        
        print(f"Connection is established with {str(address)}")

        locks[0].acquire()  # locks the clients to add one
        client = OnlineClient(False, newClient, count[0])
        clients.append(client)
        clientThreads.append(threading.Thread(target = HandleClient, args = (clients[count[0]], clients, locks, events, remove, queue, db, buttonEvent), ))
        
        clientThreads[count[0]].start()
        count[0] += 1
        locks[0].release()  # unlocks the clients



"""
Description: Removes clients to the server
Parameter: clients: Array of client objects
Parameter: locks: Array of mutexes for the server
Parameter: events: Array of event Objects for the server
Parameter: clientThreads: Array of threads
Parameter: count: Array of an integer
Parameter: remove: Array of an integer
Parameter: db: the database
Parameter: server: The server object
"""
def RemoveClient(clients, locks, events, clientThreads, count, remove, db, server):
    while (True):
        events[0].wait()  # waits for a client to want to be removed
        events[0].clear()  # resets the event
        locks[0].acquire()  # locks the clients so none can be added while removing
        
        client = clients.pop(remove[0]) # removes the client from the client array
        client.ClientSend("SetpRmve")  # tells the client to begin shutting down
        client.client.close()  # closes the client
        alias = client.GetAlias()

        del client

        thread = clientThreads.pop(remove[0])  # removes the client thread
        count[0] -= 1

        for cli in range(remove[0], len(clients)):
            clients[cli].SetNum(clients[cli].GetNum() - 1)
        
        locks[0].release()  # unlocks to allow clients to be added
        events[1].set()  # tells clients they can now be removed again
        
        thread.join()
        db.LogOutUser(alias)
        
        print(f"{alias} removed")

        if (len(clients) == 0):
            server.close()
            db.FinalizeFile()
            break



"""
Description: Handles sending messages to clients
Parameter: client: The client object
Parameter: clients: Array of client objects
Parameter: locks: Array of mutexes for the server
Parameter: events: Array of event Objects for the server
Parameter: remove: Array of an integer
Parameter: queue: Array of arrays of client objects
Parameter: db: the database
Parameter: buttonEvent: Threading event object
"""
def HandleClient(client, clients, locks, events, remove, queue, db, buttonEvent):
    moveThread = 0
    checkButtonThread = 0
    getBoardMoveThread = 0

    while (True):
        message = client.ClientReceive()
        messageLength = len(message)
        switch = False
        
        if (messageLength > 3):
            if (message[:4] == "Setp"):
                if (messageLength > 7):
                    if (message[4:8] == "Logn"):
                        username = ""
                        password = ""

                        for x in range(8, messageLength):
                            if (message[x] == " "):
                                switch = True
                                continue
                            
                            if (switch):
                                password += message[x]

                            else:
                                username += message[x]

                        locks[3].acquire()

                        if (db.VerifyLogin(username, password)):
                            client.ClientSend("SetpLognT")
                            client.SetAlias(username)

                        else:
                            client.ClientSend("SetpLognF")

                        locks[3].release()

                    elif (message[4:8] == "Addd"):
                        username = ""
                        password = ""
                        
                        for x in range(8, messageLength):
                            if (message[x] == " "):
                                switch = True
                                continue
                            
                            if (switch):
                                password += message[x]

                            else:
                                username += message[x]

                        locks[3].acquire()
                        
                        if (db.AddUser(username, password)):
                            client.ClientSend("SetpAdddT")

                        else:
                            client.ClientSend("SetpAdddF")
                        
                        locks[3].release()

                    elif (message[4:8] == "Dell"):
                        username = ""
                        password = ""
                        
                        for x in range(8, messageLength):
                            if (message[x] == " "):
                                switch = True
                                continue
                            
                            if (switch):
                                password += message[x]

                            else:
                                username += message[x]

                        locks[3].acquire()
                        
                        if (db.DeleteUser(username)):
                            client.ClientSend("SetpDellT")

                        else:
                            client.ClientSend("SetpDellF")
                        
                        locks[3].release()

                    elif (message[4:8] == "Rmve"):
                        print(f"Removing {client.GetAlias()}")
                        
                        locks[1].acquire()  # locks clients from removing until this client is done
                        remove[0] = client.GetNum()  # sets which client to be removed
                        events[0].set()  # tells the removing thread to start
                        events[1].wait()  # waits for the client to be removed
                        events[1].clear()  # resets the event
                        locks[1].release()  # lets other clients be removed
                        
                        break

                    elif (message[4:8] == "Strt"):
                        client.SetMode(message[8:9])
                        client.SetColor(message[9:])

                        if (message[8:9] == "0"):
                            if (message[9:] == "0"):
                                locks[2].acquire()

                                if (len(queue[0]) > 0 and queue[0][0].GetColor() == "1"):
                                    opp = queue[0].pop(0)
                                    StartTwoPlayer(client, opp)

                                else:
                                    queue[0].append(client)

                                locks[2].release()

                            else:
                                locks[2].acquire()

                                if (len(queue[0]) > 0 and queue[0][0].GetColor() == "0"):
                                    opp = queue[0].pop(0)
                                    StartTwoPlayer(client, opp)

                                else:
                                    queue[0].append(client)

                                locks[2].release()

                        elif (message[8:9] == "1"):                            
                            if (message[9:] == "0"):
                                locks[2].acquire()

                                if (len(queue[1]) > 0 and queue[1][0].GetColor() == "1"):
                                    opp = queue[1].pop(0)
                                    CheckIfTwoReady(queue, client, opp, locks, events)

                                else:
                                    queue[1].append(client)

                                locks[2].release()

                            else:
                                locks[2].acquire()

                                if (len(queue[2]) > 0 and queue[2][0].GetColor() == "0"):
                                    opp = queue[2].pop(0)
                                    CheckIfTwoReady(queue, client, opp, locks, events)

                                else:
                                    queue[2].append(client)

                                locks[2].release()

                        elif (message[8:9] == "2"):                            
                            if (message[9:] == "0"):
                                locks[2].acquire()

                                if (len(queue[2]) > 0 and queue[2][0].GetColor() == "1"):
                                    opp = queue[2].pop(0)
                                    CheckIfTwoReady(queue, client, opp, locks, events)

                                else:
                                    queue[2].append(client)

                                locks[2].release()

                            else:
                                locks[2].acquire()

                                if (len(queue[1]) > 0 and queue[1][0].GetColor() == "0"):
                                    opp = queue[1].pop(0)
                                    CheckIfTwoReady(queue, client, opp, locks, events)

                                else:
                                    queue[1].append(client)

                                locks[2].release()

                        elif (message[8:9] == "3"):
                            if (message[9:] == "0"):
                                client.ClientSend("SetpOpntBlack AI")

                            else:
                                client.ClientSend("SetpOpntWhite AI")

                        elif (message[8:9] == "4"):
                            locks[2].acquire()

                            queue[3].append(client)

                            if (queue[3][0] == client):
                                CapturePreImage()

                                if (message[9:] == "0"):
                                    client.ClientSend("SetpOpntBlack AI")

                                else:
                                    client.ClientSend("SetpOpntWhite AI")

                            else:
                                while (queue[3][0] != client):
                                    locks[2].release()

                                    events[2].wait()
                                    
                                    locks[2].acquire()
                                
                                CapturePreImage()

                                if (message[9:] == "0"):
                                    client.ClientSend("SetpOpntBlack AI")

                                else:
                                    client.ClientSend("SetpOpntWhite AI")

                            locks[2].release()
                            
            elif (message[:4] == "Chat"):
                if (client.GetOpponent() != "None"):
                    for cli in clients:
                        if (cli.GetAlias() == client.GetOpponent()):
                            cli.ClientSend("Chat" + message[4:])

            elif (message[:4] == "Move"):
                if (client.GetOpponent() != "None"):
                    for cli in clients:
                        if (cli.GetAlias() == client.GetOpponent()):
                            cli.ClientSend(message)
            
            elif (message[:4] == "Mvai"):
                moveThread = threading.Thread(target = Move, args = (int(message[4:6]), int(message[6:8]), int(message[8:10]), message[10], message[11], message[12], client), )
                moveThread.start()

            elif (message[:4] == "Mvjn"):
                moveThread.join()

            elif (message[:4] == "Endd"):
                client.ClientSend("Endd")

            elif (message[:4] == "Meff"):
                client.ClientSend("MoveMeff")
                if (client.GetOpponent() != "None"):
                    for cli in clients:
                        if (cli.GetAlias() == client.GetOpponent()):
                            cli.ClientSend("Forf")

            elif (message[:4] == "Free"):
                locks[2].acquire()

                if (client in queue[3]):
                    queue[3].remove(client)
                
                locks[2].release()

                events[2].set()
                sleep(3)
                events[2].clear()

            elif (message[:4] == "Sbmv"):
                checkButtonThread = threading.Thread(target = CheckButton, args = (0, client, buttonEvent), )
                getBoardMoveThread = threading.Thread(target = GetBoardMove, args = (0, client), )
                checkButtonThread.start()
                getBoardMoveThread.start()

            elif (message[:4] == "Cclr"):
                checkButtonThread.join()
                checkButtonThread = 0

            elif (message[:4] == "Bmjn"):
                getBoardMoveThread.join()
                getBoardMoveThread = 0

            elif (message[:4] == "Cpre"):
                errorMoveThread = threading.Thread(target = ErrorCheck, args = (0, client, buttonEvent), )
                errorMoveThread.start()

            elif (message[:4] == "Cdne"):
                errorMoveThread.join()
                errorMoveThread = 0



"""
Description: Handles incorrect player moves
Parameter: num: Integer
Parameter: client: The client object
Parameter: buttonEvent: Threading event object
"""
def ErrorCheck(num, client, buttonEvent):
    buttonEvent.wait()
    buttonEvent.clear()

    CapturePreImage()
    client.ClientSend("Cpre")



"""
Description: Starts a game between two clients
Parameter: client: The client object
Parameter: opp: The client object for opponent
"""
def StartTwoPlayer(client, opp):
    opp.ClientSend("SetpOpnt" + client.GetAlias())
    client.ClientSend("SetpOpnt" + opp.GetAlias())
    client.SetOpponent(opp.GetAlias())
    opp.SetOpponent(client.GetAlias())



"""
Description: prepares to start a game between two clients
Parameter: queue: Array of arrays of client objects
Parameter: client: The client object
Parameter: opp: The client object for opponent
Parameter: locks: Array of mutexes for the server
Parameter: events: Array of event Objects for the server
"""
def CheckIfTwoReady(queue, client, opp, locks, events):
    queue[3].append(client)

    if (queue[3][0] == client):
        StartTwoPlayer(client, opp)
        CapturePreImage()

    else:
        while (queue[3][0] != client):
            locks[2].release()

            events[2].wait()
            
            locks[2].acquire()

        StartTwoPlayer(client, opp)
        CapturePreImage()



"""
Description: Checks if a button is pressed
Parameter: client: The client object
"""
def CheckButton(num, client, buttonEvent):
    buttonEvent.wait()
    buttonEvent.clear()

    CapturePostImage()
    start, end = CompareArrays()

    client.bdMvLock.acquire()

    client.bMove[0] = start
    client.bMove[1] = end

    client.bdMvLock.release()

    client.bmvEvent.set()

    client.ClientSend("Cclr")



"""
Description: Gets the move from the client on the board
Parameter: client: The client object
"""
def GetBoardMove(num, client):
    client.bmvEvent.wait()
    client.bmvEvent.clear()

    client.bdMvLock.acquire()

    bStart = str(client.bMove[0])
    bEnd = str(client.bMove[1])

    client.bMove[0] = 64
    client.bMove[1] = 64

    client.bdMvLock.release()
    
    if (len(bStart) == 1):
        bStart = "0" + bStart
    
    if (len(bStart) == 1):
        bEnd = "0" + bEnd
        
    client.ClientSend("Bdmv" + bStart + bEnd)



if __name__ == "__main__":
    StartServer().run()



# End of File