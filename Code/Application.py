"""
File: Application.py
Author: Ian Poremba (iporemba@uci.edu)
Author: Devin Reyes (devinnr@uci.edu)
Author: Allen Sien (siena@uci.edu)
Description: Contains the implementation of the games and moves
Start date: 08/30/2022
Updated: 03/11/2023
"""



# ------------------------- Dependencies -------------------------

from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
import kivy
from kivy.uix.image import Image
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import kivy.clock
import threading
import ConnectClient
from time import sleep 
from CsGameBoard import GameBoard
from CsPlayer import Players

# ------------------------- Definitions --------------------------



windowStart = Window.height



"""
Description: The class to handle the creation of the app itself
Parameter: App: The application
"""
class MyApp(App):
    def build(self):
        global client
        global sm
        global app 
        global clock

        clock = kivy.clock.Clock
        app = App
        client = ConnectClient.OnlineClient(True, 0, 0)
        Window.clearcolor = (.15, .15, .15, 1)
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="LoginScreen"))
        sm.add_widget(HomeScreen(name="HomeScreen"))
        sm.add_widget(SettingsScreen(name="SettingsScreen"))
        sm.add_widget(GameModesScreen(name="GameModesScreen"))
        sm.add_widget(ColorScreen(name="ColorScreen"))
        sm.add_widget(GameScreen(name="GameScreen"))
        sm.add_widget(GameOverScreen(name="GameOverScreen"))

        client.Connect()
        client.StartDecoder(sm, clock)
        
        blackPawnImg = Image(source = "icons/black-pawn.png")
        whitePawnImg = Image(source = "icons/white-pawn.png")
        blackRookImg = Image(source = "icons/black-rook.png")
        whiteRookImg = Image(source = "icons/white-rook.png")
        blackKnightImg = Image(source = "icons/black-knight.png")
        whiteKnightImg = Image(source = "icons/white-knight.png")
        blackBishopImg = Image(source = "icons/black-bishop.png")
        whiteBishopImg = Image(source = "icons/white-bishop.png")
        blackQueenImg = Image(source = "icons/black-queen.png")
        whiteQueenImg = Image(source = "icons/white-queen.png")
        blackKingImg = Image(source = "icons/black-king.png")
        whiteKingImg = Image(source = "icons/white-king.png")

        return (sm)
    


"""
Description: The class to handle LoginScreen widgets
Parameter: Screen: Screen object from screen manager
"""
class LoginScreen(Screen):
    global client

    username = ObjectProperty(None)
    password = ObjectProperty(None)
    login = ObjectProperty(None)
    loginLayout = ObjectProperty(None)
    title = ObjectProperty(None)
    usernameLabel = ObjectProperty(None)
    passwordLabel = ObjectProperty(None)
    loginButton = ObjectProperty(None)
    signUpButton = ObjectProperty(None)
    exitButton = ObjectProperty(None)



    """
    Description: Resizes the login screen
    """
    def ResizeLoginScreen(self, num):
        minimum = min(Window.width, Window.height)
        self.loginLayout.size_hint = (minimum / Window.width, minimum / Window.height)
        self.title.font_size = 50 * minimum / windowStart
        self.login.font_size = 36 * minimum / windowStart
        self.usernameLabel.font_size = 24 * minimum / windowStart
        self.passwordLabel.font_size = 24 * minimum / windowStart
        self.username.font_size = 16 * minimum / windowStart
        self.password.font_size = 16 * minimum / windowStart
        self.loginButton.font_size = 12 * minimum / windowStart
        self.signUpButton.font_size = 12 * minimum / windowStart
        self.exitButton.font_size = 12 * minimum / windowStart



    """
    Description: Signs the client up
    """
    def UpdateLoginText(self, message):
        self.login.text = message



    """
    Description: Signs the client up
    """
    def SignUp(self):
        if (client.waitStatus == False):
            username = self.username.text
            password = self.password.text

            for x in username:
                if (x == ' ' or x == "\t"):
                    self.username.text = ""
                    self.password.text = ""
                    self.UpdateLoginText("Adding player failed. Username and password can not contain spaces.")
                    
                    return

            for x in password:
                if (x == ' ' or x == "\t"):
                    self.username.text = ""
                    self.password.text = ""
                    self.UpdateLoginText("Adding player failed. Username and password can not contain spaces.")

                    return
                
            if (len(username) == 0 or len(password) == 0):
                self.username.text = ""
                self.password.text = ""
                self.UpdateLoginText("Adding player failed. Username and password must contain characters.")

                return

            elif (not client.CheckWithServer(username, password, "Addd")):
                self.UpdateLoginText("Adding player failed.")

        client.addEvent.wait()
        client.addEvent.clear()

        if (client.addStatus):
            self.UpdateLoginText("Adding player succeded. Please log in.")

        else:
            self.UpdateLoginText("Adding player failed.")



    """
    Description: Logs the client in
    """
    def LogIn(self):
        if (client.waitStatus == False):
            username = self.username.text
            password = self.password.text

            for x in username:
                if (x == " " or x == "\t"):
                    self.username.text = ""
                    self.password.text = ""
                    self.UpdateLoginText("Login failed. Username and password can not contain spaces.")

                    return

            for x in password:
                if (x == " " or x == "\t"):
                    self.username.text = ""
                    self.password.text = ""
                    self.UpdateLoginText("Login failed. Username and password can not contain spaces.")

                    return
                
            if (len(username) == 0 or len(password) == 0):
                self.username.text = ""
                self.password.text = ""
                self.UpdateLoginText("Login failed. Username and password must contain characters.")

                return

            elif (not client.CheckWithServer(self.username.text, self.password.text, "Logn")):
                self.UpdateLoginText("Login failed.")

        client.logEvent.wait()
        client.logEvent.clear()

        if (client.logStatus):
            self.parent.current = "HomeScreen"
            self.parent.transition.direction = "right"

        else:
            self.UpdateLoginText("Login failed.")



    """
    Description: Closes the client
    """
    def LogClosingClient(self):
        client.ClientClose()
        sleep(.1)



"""
Description: The class to handle HomeScreen widget
Parameter: Screen: Screen object from screen manager
"""
class HomeScreen(Screen):
    homeLayout = ObjectProperty(None)
    title = ObjectProperty(None)
    authors = ObjectProperty(None)
    gameButton = ObjectProperty(None)
    settingsButton = ObjectProperty(None)
    exitButton = ObjectProperty(None)



    """
    Description: Resizes the home screen
    """
    def ResizeHomeScreen(self, num):
        minimum = min(Window.width, Window.height)
        self.homeLayout.size_hint = (minimum / Window.width, minimum / Window.height)
        self.title.font_size = 50 * minimum / windowStart
        self.authors.font_size = 24 * minimum / windowStart
        self.gameButton.font_size = 12 * minimum / windowStart
        self.settingsButton.font_size = 12 * minimum / windowStart
        self.exitButton.font_size = 12 * minimum / windowStart



    """
    Description: Closes the client
    """
    def ClosingClient(self):
        global client

        client.ClientClose()
        sleep(.1)



"""
Description: The class to handle SettingScreen widget
Parameter: Screen: Screen object from screen manager
"""
class SettingsScreen(Screen):
    global app
    global client

    set = ObjectProperty(None)
    settingsLayout = ObjectProperty(None)
    settingsTitle = ObjectProperty(None)
    backButton = ObjectProperty(None)
    deleteButton = ObjectProperty(None)



    """
    Description: Resizes the settings screen
    """
    def ResizeSettingsScreen(self, num):
        minimum = min(Window.width, Window.height)
        self.settingsLayout.size_hint = (minimum / Window.width, minimum / Window.height)
        self.set.font_size = 36 * minimum / windowStart
        self.settingsTitle.font_size = 36 * minimum / windowStart
        self.backButton.font_size = 12 * minimum / windowStart
        self.deleteButton.font_size = 12 * minimum / windowStart



    """
    Description: Signs the client up
    """
    def UpdateSetText(self, message):
        self.set.text = message



    """
    Description: Deletes the client
    """
    def DelAcc(self):
        if (client.waitStatus == False):
            client.CheckWithServer(client.GetAlias(), "", "Dell")

        client.delEvent.wait()
        client.delEvent.clear()

        if (client.delStatus):
            self.SetClosingClient()

        else:
            self.UpdateSetText("Delete account failed.")
                


    """
    Description: Closes the client
    """
    def SetClosingClient(self):
        client.ClientClose()
        sleep(.1)
        app.get_running_app().stop()



"""
Description: The class to handle GameScreen wdiget
Parameter: Screen: Screen object from screen manager
"""
class GameModesScreen(Screen):
    appVsApp = ObjectProperty(None)
    boardVsAppAsApp = ObjectProperty(None)
    boardVsAppAsBoard = ObjectProperty(None)
    appVsAi = ObjectProperty(None)
    boardVsAi = ObjectProperty(None)
    gamemodeLayout = ObjectProperty(None)
    gameModeTitle = ObjectProperty(None)
    backButton = ObjectProperty(None)



    """
    Description: Resizes the gamemode screen
    """
    def ResizeGamemodeScreen(self, num):
        minimum = min(Window.width, Window.height)
        self.gamemodeLayout.size_hint = (minimum / Window.width, minimum / Window.height)
        self.gameModeTitle.font_size = 36 * minimum / windowStart
        self.appVsApp.font_size = 12 * minimum / windowStart
        self.boardVsAppAsApp.font_size = 12 * minimum / windowStart
        self.boardVsAppAsBoard.font_size = 12 * minimum / windowStart
        self.appVsAi.font_size = 12 * minimum / windowStart
        self.boardVsAi.font_size = 12 * minimum / windowStart
        self.backButton.font_size = 12 * minimum / windowStart



    """
    Description: Selects the mode for the client
    Parameter: btn: Button object
    """
    def GamemodeSelection(self, btn):
        global client

        if (btn == self.appVsApp):
            client.SetMode("0")

        elif (btn == self.boardVsAppAsApp):
            client.SetMode("1")

        elif (btn == self.boardVsAppAsBoard):
            client.SetMode("2")

        elif (btn == self.appVsAi):
            client.SetMode("3")

        elif (btn == self.boardVsAi):
            client.SetMode("4")



"""
Description: The class to handle ColorScreen widget
Parameter: Screen: Screen object from screen manager
"""
class ColorScreen(Screen):
    global sm

    blackBtn = ObjectProperty(None)
    whiteBtn = ObjectProperty(None)
    colorLayout = ObjectProperty(None)
    backButton = ObjectProperty(None)
    colorTitle = ObjectProperty(None)



    """
    Description: Resizes the color screen
    """
    def ResizeColorScreen(self, num):
        minimum = min(Window.width, Window.height)
        self.colorLayout.size_hint = (minimum / Window.width, minimum / Window.height)
        self.whiteBtn.font_size = 12 * minimum / windowStart
        self.blackBtn.font_size = 12 * minimum / windowStart
        self.backButton.font_size = 12 * minimum / windowStart
        self.colorTitle.font_size = 36 * minimum / windowStart



    """
    Description: Selects the color for the client
    Parameter: btn: Button object
    """
    def ColorSelection(self, btn):
        global client

        if (btn == self.whiteBtn):
            client.SetColor("0")

        elif (btn == self.blackBtn):
            client.SetColor("1")

        client.ClientSend("SetpStrt" + client.GetMode() + client.GetColor())
        sm.get_screen("GameScreen").UpdateBoard(GameBoard(Players(True), Players(False)), True)
        sm.get_screen("GameScreen").DisplayBoard(0)
        client.disEvent.wait()
        client.disEvent.clear()
            


"""
Description: The class to handle GameOverScreen widget
Parameter: Screen: Screen object from screen manager
"""
class GameOverScreen(Screen):
    log = ""
    scrollView2 = ObjectProperty(None)
    gameoverLayout = ObjectProperty(None)
    exitButton = ObjectProperty(None)
    gameOverLabel = ObjectProperty(None)



    """
    Description: Resizes the settings screen
    """
    def ResizeGameoverScreen(self, num):
        minimum = min(Window.width, Window.height)
        self.gameoverLayout.size_hint = (minimum / Window.width, minimum / Window.height)
        self.scrollView2.endGameChat.font_size = 16 * minimum / windowStart
        self.gameOverLabel.font_size = 36 * minimum / windowStart
        self.exitButton.font_size = 12 * minimum / windowStart



    """
    Description: Updates the game log
    Parameter: log: String
    """
    def UpdateLog(self, log):
        self.log = log



    """
    Description: Displays the game log
    """
    def DisplayLog(self, num):
        self.scrollView2.endGameChat.text = self.log



"""
Description: The class to handle GameScreen widget
Parameter: Screen: Screen object from screen manager
"""
class GameScreen(Screen):
    global client

    yourTurn = False
    gameText = ""
    board = 0
    yourColor = False

    scrollView = ObjectProperty(None)
    chatInput = ObjectProperty(None)
    chessboardText = ObjectProperty(None)
    forfeitButton = ObjectProperty(None)
    onlineChat = ObjectProperty(None)
    
    
    btn00 = ObjectProperty(None)
    btn01 = ObjectProperty(None)
    btn02 = ObjectProperty(None)
    btn03 = ObjectProperty(None)
    btn04 = ObjectProperty(None)
    btn05 = ObjectProperty(None)
    btn06 = ObjectProperty(None)
    btn07 = ObjectProperty(None)
    btn08 = ObjectProperty(None)
    btn09 = ObjectProperty(None)
    btn10 = ObjectProperty(None)
    btn11 = ObjectProperty(None)
    btn12 = ObjectProperty(None)
    btn13 = ObjectProperty(None)
    btn14 = ObjectProperty(None)
    btn15 = ObjectProperty(None)
    btn16 = ObjectProperty(None)
    btn17 = ObjectProperty(None)
    btn18 = ObjectProperty(None)
    btn19 = ObjectProperty(None)
    btn20 = ObjectProperty(None)
    btn21 = ObjectProperty(None)
    btn22 = ObjectProperty(None)
    btn23 = ObjectProperty(None)
    btn24 = ObjectProperty(None)
    btn25 = ObjectProperty(None)
    btn26 = ObjectProperty(None)
    btn27 = ObjectProperty(None)
    btn28 = ObjectProperty(None)
    btn29 = ObjectProperty(None)
    btn30 = ObjectProperty(None)
    btn31 = ObjectProperty(None)
    btn32 = ObjectProperty(None)
    btn33 = ObjectProperty(None)
    btn34 = ObjectProperty(None)
    btn35 = ObjectProperty(None)
    btn36 = ObjectProperty(None)
    btn37 = ObjectProperty(None)
    btn38 = ObjectProperty(None)
    btn39 = ObjectProperty(None)
    btn40 = ObjectProperty(None)
    btn41 = ObjectProperty(None)
    btn42 = ObjectProperty(None)
    btn43 = ObjectProperty(None)
    btn44 = ObjectProperty(None)
    btn45 = ObjectProperty(None)
    btn46 = ObjectProperty(None)
    btn47 = ObjectProperty(None)
    btn48 = ObjectProperty(None)
    btn49 = ObjectProperty(None)
    btn50 = ObjectProperty(None)
    btn51 = ObjectProperty(None)
    btn52 = ObjectProperty(None)
    btn53 = ObjectProperty(None)
    btn54 = ObjectProperty(None)
    btn55 = ObjectProperty(None)
    btn56 = ObjectProperty(None)
    btn57 = ObjectProperty(None)
    btn58 = ObjectProperty(None)
    btn59 = ObjectProperty(None)
    btn60 = ObjectProperty(None)
    btn61 = ObjectProperty(None)
    btn62 = ObjectProperty(None)
    btn63 = ObjectProperty(None)
    
    ra = ObjectProperty(None)
    rb = ObjectProperty(None)
    rc = ObjectProperty(None)
    rd = ObjectProperty(None)
    re = ObjectProperty(None)
    rf = ObjectProperty(None)
    rg = ObjectProperty(None)
    rh = ObjectProperty(None)
    c1 = ObjectProperty(None)
    c2 = ObjectProperty(None)
    c3 = ObjectProperty(None)
    c4 = ObjectProperty(None)
    c5 = ObjectProperty(None)
    c6 = ObjectProperty(None)
    c7 = ObjectProperty(None)
    c8 = ObjectProperty(None)
    gameLayout = ObjectProperty(None)
    
    imgDict = { 
            "WP": "icons/white-pawn.png",
            "WB": "icons/white-bishop.png",
            "WN": "icons/white-knight.png",
            "WQ": "icons/white-queen.png",
            "WK": "icons/white-king.png",
            "WR": "icons/white-rook.png",
            "BP": "icons/black-pawn.png",
            "BB": "icons/black-bishop.png",
            "BN": "icons/black-knight.png",
            "BQ": "icons/black-queen.png",
            "BK": "icons/black-king.png",
            "BR": "icons/black-rook.png", 
    }



    """
    Description: Resizes the game screen
    """
    def ResizeGameScreen(self, num):
        minimum = min(Window.width, Window.height)
        self.gameLayout.size_hint = (minimum / Window.width, minimum / Window.height)
        self.ra.font_size = 32 * minimum / windowStart
        self.rb.font_size = 32 * minimum / windowStart
        self.rc.font_size = 32 * minimum / windowStart
        self.rd.font_size = 32 * minimum / windowStart
        self.re.font_size = 32 * minimum / windowStart
        self.rf.font_size = 32 * minimum / windowStart
        self.rg.font_size = 32 * minimum / windowStart
        self.rh.font_size = 32 * minimum / windowStart
        self.c1.font_size = 32 * minimum / windowStart
        self.c2.font_size = 32 * minimum / windowStart
        self.c3.font_size = 32 * minimum / windowStart
        self.c4.font_size = 32 * minimum / windowStart
        self.c5.font_size = 32 * minimum / windowStart
        self.c6.font_size = 32 * minimum / windowStart
        self.c7.font_size = 32 * minimum / windowStart
        self.c8.font_size = 32 * minimum / windowStart
        self.scrollView.inGameChat.font_size = 16 * minimum / windowStart
        self.forfeitButton.font_size = 12 * minimum / windowStart
        self.chatInput.font_size = 16 * minimum / windowStart
        self.onlineChat.font_size = 18 * minimum / windowStart
        self.chessboardText.font_size = 18 * minimum / windowStart



    """
    Description: The function that adds promotion buttons for player to choose from
    Parameter: self
    """      
    def promotion(self, num):
        self.yourTurn = False
        self.promotionSelection.pos_hint = {"x": 0.1, "y": 0.11}
        sm.get_screen("GameScreen").UpdateGameText(f"Promotion! Please select the piece to promote to.")
        clock.schedule_once(sm.get_screen("GameScreen").DisplayGameText)
    


    """
    Description: The function that removes promotion buttons for player to choose from
    Parameter: self
    """      
    def DeletePromotion(self, btn):
        if(btn.txt == "promRook"):
            client.prom = "rook"
        
        elif(btn.txt == "promQueen"):
            client.prom = "queen"
        
        elif(btn.txt == "promKnight"):
            client.prom = "knight"
        
        elif(btn.txt == "promBishop"):
            client.prom = "bishop"   

        self.promotionSelection.pos_hint = {"x": 2, "y": 2}
    
        client.spmEvent.set()
        self.yourTurn = True
    
    
    """
    Description: The function that changes the appearance of the app based on the orientation being used
    Parameter: self
    """    
    def move_chat(self):
        win_size = Window.size
        # if the window is wider than the height
        if (win_size[0] > win_size[1]) and (self.chat_label.text == ""):
            self.chat_grid.pos_hint = {"x": 0.55, "top": 0.497}
            self.board_grid.pos_hint = {"x": 0.05, "top": 0.85}
            if(self.promotionSelection.pos_hint == {"x": 2, "top": 2}):
                pass
            else:
                self.promotionSelection.cols = 1
                self.promotionSelection.pos_hint = {"x": 0.47, "top": 0.75}         
            self.scrollView.height = 600
            self.chat_grid.row_force_default = True
            self.chat_grid.row_default_height = 60
            self.chat_grid.col_default_width = 470
            self.exit_btn.pos_hint = {"x": .45, "y": 0.12}
            self.exit_btn.size_hint = (0.1,0.05)
            self.chessboardText.pos_hint = {"x": .21, "y": 0.87}
        else:
            self.chat_grid.pos_hint = {"x": 0.23, "top": 0.25}
            self.board_grid.pos_hint = {"x": 0.15, "top": 0.88}
            if(self.promotionSelection.pos_hint == {"x": 2, "top": 2}):
                pass
            else:
                self.promotionSelection.rows = 1
                self.promotionSelection.cols = 5
                self.promotionSelection.pos_hint = {"x": 0.2, "top": 0.4}
            self.chat_label.text = ""
            self.scrollView.height = 200
            self.chat_grid.row_force_default = True
            self.chat_grid.row_default_height = 60
            self.chat_grid.col_default_width = 465
            self.exit_btn.pos_hint = {"x": .45, "y": 0.03}
            self.exit_btn.size_hint = (0.2,0.05)
            self.chessboardText.pos_hint = {"x": .48, "y": 0.89}



    """
    Description: Updates a signal on screen switch
    """
    def SwitchToNext(self):
        if (self.forfeitButton.text == "Exit"):
            self.forfeitButton.text = "Forfeit"
            self.yourTurn = False
            sm.get_screen("GameScreen").UpdateBoard(GameBoard(Players(True), Players(False)), True)
            sm.get_screen("GameScreen").DisplayBoard(0)
            client.disEvent.wait()
            client.disEvent.clear()
            self.scrollView.inGameChat.text = ""
            self.chessboardText.text = "Waiting for opponent"
            self.parent.current = "GameOverScreen"
            self.parent.transition.direction = "right"

        else:
            if (client.GetOpponent() == "White AI" or client.GetOpponent() == "Black AI"):
                self.yourTurn = False  
                client.ClientMove("-3")

            else:
                if (self.yourTurn == True):
                    self.yourTurn = False  
                    client.ClientMove("-2")
                else:
                    client.ClientSend("Meff")



    """
    Description: Set Turn for moves
    Parameter: turn: Boolean
    """
    def SetTurn(self, turn):
        self.yourTurn = turn



    """
    Description: Handles a button press
    Parameter: btn: Button object
    """
    def HandleButton(self, btn):
        if (self.yourTurn):
            client.ClientMove(btn.int)



    """
    Description: Handles sending a message
    """
    def ChatSend(self):
        if (client.GetInGame()):
            client.AddMessage("Me: " + self.chatInput.text)
            
            if (client.GetMode() == "1"):
                client.AddMessage("AI: I'm an AI I can't respond stupid.")

            else:
                client.ClientSend("Chat" + client.GetAlias() + ": " + self.chatInput.text)

            self.scrollView.inGameChat.text = ""
            self.UpdateChat(0)
    


    """
    Description: Updates the chat
    """
    def UpdateChat(self, num):
        self.scrollView.inGameChat.text = ""

        for x in range(len(client.messages)):
            self.scrollView.inGameChat.text += client.messages[x] + "\n"



    """
    Descrition: Updates the forfeit buttons name
    """
    def UpdateForfeitName(self, num):
        self.forfeitButton.text = "Exit"



    """
    Description: Updates the the game text
    """
    def UpdateGameText(self, message):
        self.gameText = message



    """
    Description: Updates the the game text
    """
    def DisplayGameText(self, num):
        self.chessboardText.text = self.gameText
        


    """
    Description: Updates the button images
    Parameter: string: String
    """
    def ButtonImages(self, string):
        self.pieceName = string
        
        if(self.pieceName != ""):
            self.img = self.imgDict[self.pieceName]
            
            return (self.img)
        
        else:
            return (None)
        
        
    
    """
    Description: Updates the board array
    Parameter: board: GameBoard class object
    Parameter: yourColor: Boolean
    """
    def UpdateBoard(self, board, yourColor):
        self.board = board
        self.yourColor = yourColor
        
    
    """
    Description: Displays the board as pieces move
    """
    def DisplayBoard(self, num):
        if (self.yourColor):
            x = 0
            self.ra.text = "A"
            self.rb.text = "B"
            self.rc.text = "C"
            self.rd.text = "D"
            self.re.text = "E"
            self.rf.text = "F"
            self.rg.text = "G"
            self.rh.text = "H"
            self.c1.text = "1"
            self.c2.text = "2"
            self.c3.text = "3"
            self.c4.text = "4"
            self.c5.text = "5"
            self.c6.text = "6"
            self.c7.text = "7"
            self.c8.text = "8"

        else:
            x = 63
            self.ra.text = "H"
            self.rb.text = "G"
            self.rc.text = "F"
            self.rd.text = "E"
            self.re.text = "D"
            self.rf.text = "C"
            self.rg.text = "B"
            self.rh.text = "A"
            self.c1.text = "8"
            self.c2.text = "7"
            self.c3.text = "6"
            self.c4.text = "5"
            self.c5.text = "4"
            self.c6.text = "3"
            self.c7.text = "2"
            self.c8.text = "1"

        if (self.board.board[abs(x - 0)].name != None):
            self.btn00.btn0Img.source = self.ButtonImages(self.board.board[abs(x - 0)].name)
            self.btn00.btn0Img.color = 1,1,1,1
        
        else:
            self.btn00.btn0Img.source = ""
            self.btn00.btn0Img.color = 0,0,0,0

        if (self.board.board[abs(x - 1)].name != None):
            self.btn01.btn1Img.source = self.ButtonImages(self.board.board[abs(x - 1)].name)
            self.btn01.btn1Img.color = 1,1,1,1
        
        else:
            self.btn01.btn1Img.source = ""
            self.btn01.btn1Img.color = 0,0,0,0

        if (self.board.board[abs(x - 2)].name != None):
            self.btn02.btn2Img.source = self.ButtonImages(self.board.board[abs(x - 2)].name)
            self.btn02.btn2Img.color = 1,1,1,1

        else:
            self.btn02.btn2Img.source = ""
            self.btn02.btn2Img.color = 0,0,0,0
        
        if (self.board.board[abs(x - 3)].name != None):
            self.btn03.btn3Img.source = self.ButtonImages(self.board.board[abs(x - 3)].name)
            self.btn03.btn3Img.color = 1,1,1,1

        else:
            self.btn03.btn3Img.source = ""
            self.btn03.btn3Img.color = 0,0,0,0

        if (self.board.board[abs(x - 4)].name != None):
            self.btn04.btn4Img.source = self.ButtonImages(self.board.board[abs(x - 4)].name)
            self.btn04.btn4Img.color = 1,1,1,1

        else:
            self.btn04.btn4Img.source = ""
            self.btn04.btn4Img.color = 0,0,0,0

        if (self.board.board[abs(x - 5)].name != None):
            self.btn05.btn5Img.source = self.ButtonImages(self.board.board[abs(x - 5)].name)
            self.btn05.btn5Img.color = 1,1,1,1

        else:
            self.btn05.btn5Img.source = ""
            self.btn05.btn5Img.color = 0,0,0,0

        if (self.board.board[abs(x - 6)].name != None):
            self.btn06.btn6Img.source = self.ButtonImages(self.board.board[abs(x - 6)].name)
            self.btn06.btn6Img.color = 1,1,1,1

        else:
            self.btn06.btn6Img.source = ""
            self.btn06.btn6Img.color = 0,0,0,0

        if (self.board.board[abs(x - 7)].name != None):
            self.btn07.btn7Img.source = self.ButtonImages(self.board.board[abs(x - 7)].name)
            self.btn07.btn7Img.color = 1,1,1,1

        else:
            self.btn07.btn7Img.source = ""
            self.btn07.btn7Img.color = 0,0,0,0

        if (self.board.board[abs(x - 8)].name != None):
            self.btn08.btn8Img.source = self.ButtonImages(self.board.board[abs(x - 8)].name)
            self.btn08.btn8Img.color = 1,1,1,1

        else:
            self.btn08.btn8Img.source = ""
            self.btn08.btn8Img.color = 0,0,0,0

        if (self.board.board[abs(x - 9)].name != None):
            self.btn09.btn9Img.source = self.ButtonImages(self.board.board[abs(x - 9)].name)
            self.btn09.btn9Img.color = 1,1,1,1

        else:
            self.btn09.btn9Img.source = ""
            self.btn09.btn9Img.color = 0,0,0,0

        if (self.board.board[abs(x - 10)].name != None):
            self.btn10.btn10Img.source = self.ButtonImages(self.board.board[abs(x - 10)].name)
            self.btn10.btn10Img.color = 1,1,1,1

        else:
            self.btn10.btn10Img.source = ""
            self.btn10.btn10Img.color = 0,0,0,0

        if (self.board.board[abs(x - 11)].name != None):
            self.btn11.btn11Img.source = self.ButtonImages(self.board.board[abs(x - 11)].name)
            self.btn11.btn11Img.color = 1,1,1,1

        else:
            self.btn11.btn11Img.source = ""
            self.btn11.btn11Img.color = 0,0,0,0

        if (self.board.board[abs(x - 12)].name != None):
            self.btn12.btn12Img.source = self.ButtonImages(self.board.board[abs(x - 12)].name)
            self.btn12.btn12Img.color = 1,1,1,1

        else:
            self.btn12.btn12Img.source = ""
            self.btn12.btn12Img.color = 0,0,0,0

        if (self.board.board[abs(x - 13)].name != None):
            self.btn13.btn13Img.source = self.ButtonImages(self.board.board[abs(x - 13)].name)
            self.btn13.btn13Img.color = 1,1,1,1

        else:
            self.btn13.btn13Img.source = ""
            self.btn13.btn13Img.color = 0,0,0,0

        if (self.board.board[abs(x - 14)].name != None):
            self.btn14.btn14Img.source = self.ButtonImages(self.board.board[abs(x - 14)].name)
            self.btn14.btn14Img.color = 1,1,1,1

        else:
            self.btn14.btn14Img.source = ""
            self.btn14.btn14Img.color = 0,0,0,0

        if (self.board.board[abs(x - 15)].name != None):
            self.btn15.btn15Img.source = self.ButtonImages(self.board.board[abs(x - 15)].name)
            self.btn15.btn15Img.color = 1,1,1,1

        else:
            self.btn15.btn15Img.source = ""
            self.btn15.btn15Img.color = 0,0,0,0

        if (self.board.board[abs(x - 16)].name != None):
            self.btn16.btn16Img.source = self.ButtonImages(self.board.board[abs(x - 16)].name)
            self.btn16.btn16Img.color = 1,1,1,1

        else:
            self.btn16.btn16Img.source = ""
            self.btn16.btn16Img.color = 0,0,0,0

        if (self.board.board[abs(x - 17)].name != None):
            self.btn17.btn17Img.source = self.ButtonImages(self.board.board[abs(x - 17)].name)
            self.btn17.btn17Img.color = 1,1,1,1

        else:
            self.btn17.btn17Img.source = ""
            self.btn17.btn17Img.color = 0,0,0,0

        if (self.board.board[abs(x - 18)].name != None):
            self.btn18.btn18Img.source = self.ButtonImages(self.board.board[abs(x - 18)].name)
            self.btn18.btn18Img.color = 1,1,1,1

        else:
            self.btn18.btn18Img.source = ""
            self.btn18.btn18Img.color = 0,0,0,0

        if (self.board.board[abs(x - 19)].name != None):
            self.btn19.btn19Img.source = self.ButtonImages(self.board.board[abs(x - 19)].name)
            self.btn19.btn19Img.color = 1,1,1,1

        else:
            self.btn19.btn19Img.source = ""
            self.btn19.btn19Img.color = 0,0,0,0

        if (self.board.board[abs(x - 20)].name != None):
            self.btn20.btn20Img.source = self.ButtonImages(self.board.board[abs(x - 20)].name)
            self.btn20.btn20Img.color = 1,1,1,1

        else:
            self.btn20.btn20Img.source = ""
            self.btn20.btn20Img.color = 0,0,0,0

        if (self.board.board[abs(x - 21)].name != None):
            self.btn21.btn21Img.source = self.ButtonImages(self.board.board[abs(x - 21)].name)
            self.btn21.btn21Img.color = 1,1,1,1

        else:
            self.btn21.btn21Img.source = ""
            self.btn21.btn21Img.color = 0,0,0,0

        if (self.board.board[abs(x - 22)].name != None):
            self.btn22.btn22Img.source = self.ButtonImages(self.board.board[abs(x - 22)].name)
            self.btn22.btn22Img.color = 1,1,1,1

        else:
            self.btn22.btn22Img.source = ""
            self.btn22.btn22Img.color = 0,0,0,0

        if (self.board.board[abs(x - 23)].name != None):
            self.btn23.btn23Img.source = self.ButtonImages(self.board.board[abs(x - 23)].name)
            self.btn23.btn23Img.color = 1,1,1,1

        else:
            self.btn23.btn23Img.source = ""
            self.btn23.btn23Img.color = 0,0,0,0

        if (self.board.board[abs(x - 24)].name != None):
            self.btn24.btn24Img.source = self.ButtonImages(self.board.board[abs(x - 24)].name)
            self.btn24.btn24Img.color = 1,1,1,1
            
        else:
            self.btn24.btn24Img.source = ""
            self.btn24.btn24Img.color = 0,0,0,0

        if (self.board.board[abs(x - 25)].name != None):
            self.btn25.btn25Img.source = self.ButtonImages(self.board.board[abs(x - 25)].name)
            self.btn25.btn25Img.color = 1,1,1,1

        else:
            self.btn25.btn25Img.source = ""
            self.btn25.btn25Img.color = 0,0,0,0
            
        if (self.board.board[abs(x - 26)].name != None):
            self.btn26.btn26Img.source = self.ButtonImages(self.board.board[abs(x - 26)].name)
            self.btn26.btn26Img.color = 1,1,1,1

        else:
            self.btn26.btn26Img.source = ""
            self.btn26.btn26Img.color = 0,0,0,0

        if (self.board.board[abs(x - 27)].name != None):
            self.btn27.btn27Img.source = self.ButtonImages(self.board.board[abs(x - 27)].name)
            self.btn27.btn27Img.color = 1,1,1,1

        else:
            self.btn27.btn27Img.source = ""
            self.btn27.btn27Img.color = 0,0,0,0

        if (self.board.board[abs(x - 28)].name != None):
            self.btn28.btn28Img.source = self.ButtonImages(self.board.board[abs(x - 28)].name)
            self.btn28.btn28Img.color = 1,1,1,1

        else:
            self.btn28.btn28Img.source = ""
            self.btn28.btn28Img.color = 0,0,0,0

        if (self.board.board[abs(x - 29)].name != None):
            self.btn29.btn29Img.source = self.ButtonImages(self.board.board[abs(x - 29)].name)
            self.btn29.btn29Img.color = 1,1,1,1

        else:
            self.btn29.btn29Img.source = ""
            self.btn29.btn29Img.color = 0,0,0,0

        if (self.board.board[abs(x - 30)].name != None):
            self.btn30.btn30Img.source = self.ButtonImages(self.board.board[abs(x - 30)].name)
            self.btn30.btn30Img.color = 1,1,1,1

        else:
            self.btn30.btn30Img.source = ""
            self.btn30.btn30Img.color = 0,0,0,0

        if (self.board.board[abs(x - 31)].name != None):
            self.btn31.btn31Img.source = self.ButtonImages(self.board.board[abs(x - 31)].name)
            self.btn31.btn31Img.color = 1,1,1,1

        else:
            self.btn31.btn31Img.source = ""
            self.btn31.btn31Img.color = 0,0,0,0
            
        if (self.board.board[abs(x - 32)].name != None):
            self.btn32.btn32Img.source = self.ButtonImages(self.board.board[abs(x - 32)].name)
            self.btn32.btn32Img.color = 1,1,1,1

        else:
            self.btn32.btn32Img.source = ""
            self.btn32.btn32Img.color = 0,0,0,0

        if (self.board.board[abs(x - 33)].name != None):
            self.btn33.btn33Img.source = self.ButtonImages(self.board.board[abs(x - 33)].name)
            self.btn33.btn33Img.color = 1,1,1,1

        else:
            self.btn33.btn33Img.source = ""
            self.btn33.btn33Img.color = 0,0,0,0

        if (self.board.board[abs(x - 34)].name != None):
            self.btn34.btn34Img.source = self.ButtonImages(self.board.board[abs(x - 34)].name)
            self.btn34.btn34Img.color = 1,1,1,1

        else:
            self.btn34.btn34Img.source = ""
            self.btn34.btn34Img.color = 0,0,0,0

        if (self.board.board[abs(x - 35)].name != None):
            self.btn35.btn35Img.source = self.ButtonImages(self.board.board[abs(x - 35)].name)
            self.btn35.btn35Img.color = 1,1,1,1

        else:
            self.btn35.btn35Img.source = ""
            self.btn35.btn35Img.color = 0,0,0,0
            
        if (self.board.board[abs(x - 36)].name != None):
            self.btn36.btn36Img.source = self.ButtonImages(self.board.board[abs(x - 36)].name)
            self.btn36.btn36Img.color = 1,1,1,1

        else:
            self.btn36.btn36Img.source = ""
            self.btn36.btn36Img.color = 0,0,0,0

        if (self.board.board[abs(x - 37)].name != None):
            self.btn37.btn37Img.source = self.ButtonImages(self.board.board[abs(x - 37)].name)
            self.btn37.btn37Img.color = 1,1,1,1

        else:
            self.btn37.btn37Img.source = ""
            self.btn37.btn37Img.color = 0,0,0,0

        if (self.board.board[abs(x - 38)].name != None):
            self.btn38.btn38Img.source = self.ButtonImages(self.board.board[abs(x - 38)].name)
            self.btn38.btn38Img.color = 1,1,1,1

        else:
            self.btn38.btn38Img.source = ""
            self.btn38.btn38Img.color = 0,0,0,0

        if (self.board.board[abs(x - 39)].name != None):
            self.btn39.btn39Img.source = self.ButtonImages(self.board.board[abs(x - 39)].name)
            self.btn39.btn39Img.color = 1,1,1,1

        else:
            self.btn39.btn39Img.source = ""
            self.btn39.btn39Img.color = 0,0,0,0

        if (self.board.board[abs(x - 40)].name != None):
            self.btn40.btn40Img.source = self.ButtonImages(self.board.board[abs(x - 40)].name)
            self.btn40.btn40Img.color = 1,1,1,1

        else:
            self.btn40.btn40Img.source = ""
            self.btn40.btn40Img.color = 0,0,0,0

        if (self.board.board[abs(x - 41)].name != None):
            self.btn41.btn41Img.source = self.ButtonImages(self.board.board[abs(x - 41)].name)
            self.btn41.btn41Img.color = 1,1,1,1

        else:
            self.btn41.btn41Img.source = ""
            self.btn41.btn41Img.color = 0,0,0,0

        if (self.board.board[abs(x - 42)].name != None):
            self.btn42.btn42Img.source = self.ButtonImages(self.board.board[abs(x - 42)].name)
            self.btn42.btn42Img.color = 1,1,1,1

        else:
            self.btn42.btn42Img.source = ""
            self.btn42.btn42Img.color = 0,0,0,0

        if (self.board.board[abs(x - 43)].name != None):
            self.btn43.btn43Img.source = self.ButtonImages(self.board.board[abs(x - 43)].name)
            self.btn43.btn43Img.color = 1,1,1,1

        else:
            self.btn43.btn43Img.source = ""
            self.btn43.btn43Img.color = 0,0,0,0

        if (self.board.board[abs(x - 44)].name != None):
            self.btn44.btn44Img.source = self.ButtonImages(self.board.board[abs(x - 44)].name)
            self.btn44.btn44Img.color = 1,1,1,1

        else:
            self.btn44.btn44Img.source = ""
            self.btn44.btn44Img.color = 0,0,0,0

        if (self.board.board[abs(x - 45)].name != None):
            self.btn45.btn45Img.source = self.ButtonImages(self.board.board[abs(x - 45)].name)
            self.btn45.btn45Img.color = 1,1,1,1

        else:
            self.btn45.btn45Img.source = ""
            self.btn45.btn45Img.color = 0,0,0,0

        if (self.board.board[abs(x - 46)].name != None):
            self.btn46.btn46Img.source = self.ButtonImages(self.board.board[abs(x - 46)].name)
            self.btn46.btn46Img.color = 1,1,1,1

        else:
            self.btn46.btn46Img.source = ""
            self.btn46.btn46Img.color = 0,0,0,0

        if (self.board.board[abs(x - 47)].name != None):
            self.btn47.btn47Img.source = self.ButtonImages(self.board.board[abs(x - 47)].name)
            self.btn47.btn47Img.color = 1,1,1,1

        else:
            self.btn47.btn47Img.source = ""
            self.btn47.btn47Img.color = 0,0,0,0

        if (self.board.board[abs(x - 48)].name != None):
            self.btn48.btn48Img.source = self.ButtonImages(self.board.board[abs(x - 48)].name)
            self.btn48.btn48Img.color = 1,1,1,1

        else:
            self.btn48.btn48Img.source = ""
            self.btn48.btn48Img.color = 0,0,0,0

        if (self.board.board[abs(x - 49)].name != None):
            self.btn49.btn49Img.source = self.ButtonImages(self.board.board[abs(x - 49)].name)
            self.btn49.btn49Img.color = 1,1,1,1

        else:
            self.btn49.btn49Img.source = ""
            self.btn49.btn49Img.color = 0,0,0,0

        if (self.board.board[abs(x - 50)].name != None):
            self.btn50.btn50Img.source = self.ButtonImages(self.board.board[abs(x - 50)].name)
            self.btn50.btn50Img.color = 1,1,1,1

        else:
            self.btn50.btn50Img.source = ""
            self.btn50.btn50Img.color = 0,0,0,0

        if (self.board.board[abs(x - 51)].name != None):
            self.btn51.btn51Img.source = self.ButtonImages(self.board.board[abs(x - 51)].name)
            self.btn51.btn51Img.color = 1,1,1,1

        else:
            self.btn51.btn51Img.source = ""
            self.btn51.btn51Img.color = 0,0,0,0

        if (self.board.board[abs(x - 52)].name != None):
            self.btn52.btn52Img.source = self.ButtonImages(self.board.board[abs(x - 52)].name)
            self.btn52.btn52Img.color = 1,1,1,1

        else:
            self.btn52.btn52Img.source = ""
            self.btn52.btn52Img.color = 0,0,0,0

        if (self.board.board[abs(x - 53)].name != None):
            self.btn53.btn53Img.source = self.ButtonImages(self.board.board[abs(x - 53)].name)
            self.btn53.btn53Img.color = 1,1,1,1

        else:
            self.btn53.btn53Img.source = ""
            self.btn53.btn53Img.color = 0,0,0,0

        if (self.board.board[abs(x - 54)].name != None):
            self.btn54.btn54Img.source = self.ButtonImages(self.board.board[abs(x - 54)].name)
            self.btn54.btn54Img.color = 1,1,1,1

        else:
            self.btn54.btn54Img.source = ""
            self.btn54.btn54Img.color = 0,0,0,0

        if (self.board.board[abs(x - 55)].name != None):
            self.btn55.btn55Img.source = self.ButtonImages(self.board.board[abs(x - 55)].name)
            self.btn55.btn55Img.color = 1,1,1,1

        else:
            self.btn55.btn55Img.source = ""
            self.btn55.btn55Img.color = 0,0,0,0

        if (self.board.board[abs(x - 56)].name != None):
            self.btn56.btn56Img.source = self.ButtonImages(self.board.board[abs(x - 56)].name)
            self.btn56.btn56Img.color = 1,1,1,1

        else:
            self.btn56.btn56Img.source = ""
            self.btn56.btn56Img.color = 0,0,0,0

        if (self.board.board[abs(x - 57)].name != None):
            self.btn57.btn57Img.source = self.ButtonImages(self.board.board[abs(x - 57)].name)
            self.btn57.btn57Img.color = 1,1,1,1

        else:
            self.btn57.btn57Img.source = ""
            self.btn57.btn57Img.color = 0,0,0,0

        if (self.board.board[abs(x - 58)].name != None):
            self.btn58.btn58Img.source = self.ButtonImages(self.board.board[abs(x - 58)].name)
            self.btn58.btn58Img.color = 1,1,1,1

        else:
            self.btn58.btn58Img.source = ""
            self.btn58.btn58Img.color = 0,0,0,0

        if (self.board.board[abs(x - 59)].name != None):
            self.btn59.btn59Img.source = self.ButtonImages(self.board.board[abs(x - 59)].name)
            self.btn59.btn59Img.color = 1,1,1,1

        else:
            self.btn59.btn59Img.source = ""
            self.btn59.btn59Img.color = 0,0,0,0

        if (self.board.board[abs(x - 60)].name != None):
            self.btn60.btn60Img.source = self.ButtonImages(self.board.board[abs(x - 60)].name)
            self.btn60.btn60Img.color = 1,1,1,1

        else:
            self.btn60.btn60Img.source = ""
            self.btn60.btn60Img.color = 0,0,0,0

        if (self.board.board[abs(x - 61)].name != None):
            self.btn61.btn61Img.source = self.ButtonImages(self.board.board[abs(x - 61)].name)
            self.btn61.btn61Img.color = 1,1,1,1

        else:
            self.btn61.btn61Img.source = ""
            self.btn61.btn61Img.color = 0,0,0,0

        if (self.board.board[abs(x - 62)].name != None):
            self.btn62.btn62Img.source = self.ButtonImages(self.board.board[abs(x - 62)].name)
            self.btn62.btn62Img.color = 1,1,1,1

        else:
            self.btn62.btn62Img.source = ""
            self.btn62.btn62Img.color = 0,0,0,0

        if (self.board.board[abs(x - 63)].name != None):
            self.btn63.btn63Img.source = self.ButtonImages(self.board.board[abs(x - 63)].name)
            self.btn63.btn63Img.color = 1,1,1,1

        else:
            self.btn63.btn63Img.source = ""
            self.btn63.btn63Img.color = 0,0,0,0

        client.disEvent.set()



if __name__ == "__main__":
    global clock

    def Resize(Window, width, height):
        clock.schedule_once(sm.get_screen("LoginScreen").ResizeLoginScreen)
        clock.schedule_once(sm.get_screen("HomeScreen").ResizeHomeScreen)
        clock.schedule_once(sm.get_screen("SettingsScreen").ResizeSettingsScreen)
        clock.schedule_once(sm.get_screen("GameModesScreen").ResizeGamemodeScreen)
        clock.schedule_once(sm.get_screen("ColorScreen").ResizeColorScreen)
        clock.schedule_once(sm.get_screen("GameScreen").ResizeGameScreen)
        clock.schedule_once(sm.get_screen("GameOverScreen").ResizeGameoverScreen)

    Window.bind(on_resize = Resize)
    MyApp().run()



# End of File