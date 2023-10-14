File: README.md
Author: Ian Poremba (iporemba@uci.edu)
Author: Devin Reyes (devinnr@uci.edu)
Author: Allen Sien (siena@uci.edu)
Start date: 08/24/2020
Updated: 11/16/2022

Project Title:
    Wizard's Chess

Project Description:
    Wizard’s Chess aims to design and produce a fully autonomous chess board with an AI. We are constructing a chess board with an undercarriage consisting of an electromagnet based pulley-system connected to slider rails to move around the pieces on top of the board. The pulley system will perform the moves of either the built-in AI as an opponent or an online opponent through the help of our accompanying app, which, in addition, will have features for learning chess. The undercarriage system will provide a different experience from the familiar robotic arm chess robots. We designed this project to allow people to have fun and learn chess on their own or with someone else without the need to be in person or play on a screen.

    Hardware:
	    The undercarriage pf the vhess board will consist of an electromagnet connected to a pulley system connected to 2 stepper motors and 3 linear slide rails in order to move the electromagnet to any position on the underside of the board. The pulleys will have tensioner pulleys in order to keep the belts tight. This will all be connected to a raspberry pi and LCD display in order to be able to control the components. Above the3 board will be a camera in order to track the players moves.

        Linear Rail System:
	        The linear rail system will be utilized to support the movement of the electromagnet underneath the board. The linear rail system will consist of three rails in an “H” shape with all rails the same length to span the entire board. Two of the rails will be parallel at the base of the system with a third rail connected to the rails perpendicular to the first two while being on top of the other two rails for this rail to move along their axis. The third rail will span the other axis to be able to cover the entire board.

        Pulley System: 
	        The pulley system will be overlaid with the linear rail system. The pulley system will be attached to the electromagnet to move it around the board. The pulley system is designed in the pattern shown above in figures 2.2.1.A and 2.2.1.B to move around the entire board with just two stepper motors. The electromagnet will then be attached to the pulleys and the middle linear rail to give it stability from the linear rail system and movement from the pulleys connected to the stepper motors. 

        Camera:
	        The camera will be overhead of the board to see the players’ moves and relay them back to the raspberry pi. This will be done through image processing to identify player moves.

    Software:
	    The software can be broken down into five main components: the chess code, the server-client connection, the application, the stepper motor control, and the image processing. All of these components will be utilized to control the whole project. The project will start by initializing a server on the raspberry pi. From there a client will be able to log in to the application thus using both the server-client component and the application. Once connected to the server through the app the player will be able to choose a game mode and start a game, utilizing the chess code portion of the code. The player will then be able to make their move on the board which will use image processing to identify the player's move and relay it back to the server and then to the player. The ai or online player will then decide its move and then relay it to the stepper motors which will then conduct their move moving the pieces through the various hardware systems.
		
		Chess Code:
	        The chess code is made up of multiple components designed to make the chess game run smoothly. It's made of multiple classes to help store and access data along with running relevant functions. Some of the classes include player classes to store player data such as pieces and color, piece classes to store piece data such as location and value, and board classes to store the game board along with board functionality. The main point of the chess code is to run chess games however and this is done by using, many loops to run the game as a turn-by-turn game with checks to who the player is, if imputed moves are valid, and if the game is ended or if there are any other game status updates.
	
			Chess AI Code:
                The AI opponent works by running a min-max algorithm. It begins by creating a root empty move node for the starting position of the AI. This will then test the board for all possible moves and add them to an array. From here the algorithm will go to each of those moves and repeat the process until all moves have been discovered up to a maximum depth. It does this recursively the AI would first simulate branch 1. The algorythm instead of going horizontally simulating all branches at the depth of branch 1's node, it will then try to go vertically a depth below to branch 1.1. The algorithm then checks if it has reached its maximum depth, in the case it has a maximum depth of 2, it then simulates branch 1.2 and branch 1.3. It then recursively goes back to branch 1 and then back to the root and then simulates branch 2 of the root repeating the process. After it is done creating the moves for all the branches it then Evaluates each move in the same order by checking the changed value after each move based on the relative strength of each side of the branch. From here it then cumulates the value of the root based on all the branches before alternating between the best and worst case depending on if its the ai or players move on the given turn in order to simulate the outcome of each move. Finally it selects the branch with the best outcome.

        Server-Client Code
	        The server-client code is designed to implement a server-client connection to be able to connect hosts to play a game. This connection is done through socket coding. The server side is run creating a server that then is accessed by the clients who then connect. The server client code runs multiple threads to work properly such as a message thread, game thread, and client handler thread. The message thread deals with receiving messages with their assigned headers which then decide if the message is a move, game setup instructions, or a chat message. Based on what the message header is, it'll either send the move to the chess code, start a game with the setup instructions or send a signal to the app to update the chat with the new message.
	
		Application Code
	        The application code is mainly user interface based, but it does have some minimalist code designed to run buttons, switch screens, and update text and the game board. The application starts and loads the main menu screen with buttons for selecting game modes and colors among other options. The application runs multiple threads to handle updating the chat, sending messages, and receiving moves. 
        
        Stepper Motor Code
            Not written yet

        Image Processing Code
            Not written yet

Project Installation:
    System Requirements (Mac, Windows, and Linux users):

    Windows 7 and above 
    Mac OS x Mavericks 10.9 and above 
    Linux: Ubuntu 16.04 and above 

    Setup and Configuration:

    To use our software there will be two programs/languages that are necessary for the user to run our code. First is python which can be downloaded here (version 3.7 recommended). In addition, after installing python you will need to download the Kivy language for the application. For all OS’s and instructions please follow the link here to the official Kivy website for detailed installation instructions. Once you have both languages installed, please download the designated files and use any preferred IDE that supports Python.

    Once both languages are installed and have an IDE that can run python programs you may install all files/folders necessary for this application here. Now there will be one makefile to make the execution process easier for the user. First the server will be created for the user to connect to and host games for their friends, followed by the execution of the application program that will display a GUI for the user if on Mac, Linux, or Windows.

 	For the phone application download install the application

Project Uninstallation:
    To uninstall our application please delete all downloaded files from your device. 

Project Use Instruction:
    Home Screen:
        This is the opening screen when you start the application. If you are attempting to start a game you would select the play game button which will take you to the game mode selection screen. If you wish to change how the game board looks you’d select the settings button to open the settings menu. If you wish to close the application you’d choose the quit button.

    Settings Screen:
        This screen will offer options for ai difficulty along with user interface options such as board color options. It will also have a button for exiting back to the home screen.

    Game Selection Screen:
        This screen has the options of Board vs. App, Board vs. AI, and Go Back. If the game you wish to start is vs. an online opponent, you’d select Board vs. App. If you wish to play an offline game vs. an AI, you’d select Board vs. AI. Both options will take you to the color selection screen. If you wish to go back to the home screen you’d select Go Back.

    Color Selection Screen:
        This screen gives players the option of choosing their side before starting the game. Both black and white will send you to the logging in screen whereas the Go Back button will send you back to the game mode selection screen.

    Logging in Screen:
        This screen gives players the option of choosing their username before starting the game. This will be displayed to the opponent. After entering your username it will take you to the game screen.

    Game Screen:
        This screen is the main screen of the application. It has a game board on the left side where you are playing your opponent while also having a chat on the right hand side where you are able to send messages to your opponent. If you wish to make a move you just need to click on your piece and then click the desired location. If you wish to send a chat message to your opponent all you have to do is type your message in the box and press enter when you are finished.

    Game Log Screen:
        This screen occurs when you exit a game from the game screen. This screen will display all moves by each player through the game. The button on the screen when pressed will take you back to the home screen to restart the process.


End of File
