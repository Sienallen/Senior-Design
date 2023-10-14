"""
File: ConnectLogin.py
Author: Ian Poremba (iporemba@uci.edu)
Author: Devin Reyes (devinnr@uci.edu)
Author: Allen Sien (siena@uci.edu)
Description: Contains the implementation of the username and password login
Start date: 02/18/2023
Updated: 03/02/2023
"""



# ------------------------- Dependencies -------------------------

import os.path

# ------------------------- Definitions --------------------------



"""
Description: Class for the username and password login
Function: OpenFileWrite: Opens the file to write in
Function: OpenFileRead: Opens the file to read from
Function: CloseFile: Closes the file
Function: ClearFile: Clears the file
Function: FinalizeFile: Updates the file with the array
Function: InitialArray: Initializes the array based on the file
Function: A;readyLoggedIn: Finds the specified user is already logged in
Function: FindUser: Finds the specified user
Function: VerifyLogin: Verifies the login information
Function: AddUser: Adds the user
Function: DeleteUser: Deletes the user
Function: LogOutUser: Logs out the user
"""
class UserPassDatabase():
    def __init__(self):
        self.name = "UserPass.txt"
        self.a = []
        self.b = []
        self.len = 0

        if (not os.path.isfile(self.name)):
            f = open(self.name, "w+")
            f.write("End of File")
            f.close()

        self.InitialArray()



    """
    Description: Opens the file to write in
    Returns: f: File
    """
    def OpenFileWrite(self):
        f = open(self.name, "w")

        return(f)



    """
    Description: Opens the file to read from
    Returns: f: File
    """
    def OpenFileRead(self):
        f = open(self.name, "r")
        
        return(f)



    """
    Description: Closes the file
    Parameter: f: File
    """
    def CloseFile(self, f):
        f.close()



    """
    Description: Clears the file
    Parameter: f: File
    """
    def ClearFile(self, f):
        f.truncate(0)



    """
    Description: Updates the file with the array
    """
    def FinalizeFile(self):
        f = self.OpenFileWrite()
        self.ClearFile(f)
        message = ""

        for x in range(self.len):
            message += self.a[x][0] + " " + self.a[x][1] + "\n"

        message += "End of File"
        f.write(message)
        self.CloseFile(f)



    """
    Description: Initializes the array based on the file
    """
    def InitialArray(self):
        f = self.OpenFileRead()
        lines = f.readlines()
        self.len = len(lines) - 1

        for x in range(self.len):
            self.a.append(lines[x].split())

        self.CloseFile(f)



    """
    Description: Finds the specified user is already logged in
    Parameter: username: String
    Returns: Boolean
    """
    def AlreadyLoggedIn(self, username):
        if (username in self.b):
            return (True)
        
        return (False)



    """
    Description: Finds the specified user
    Parameter: username: String
    Returns: Boolean; String
    """
    def FindUser(self, username):
        for x in range(self.len):
            if (self.a[x][0] == username):
                return(True, self.a[x][1])
            
        return (False, "")



    """
    Description: Verifies the login information
    Parameter: username: String
    Parameter: password: String
    Returns: Boolean
    """
    def VerifyLogin(self, username, password):
        exist, passw = self.FindUser(username)

        if (self.AlreadyLoggedIn(username)):
            return (False)

        if (exist and passw == password):
            self.b.append(username)
            return (True)
        
        return (False)



    """
    Description: Adds the user
    Parameter: username: String
    Parameter: password: String
    Returns: Boolean
    """
    def AddUser(self, username, password):
        exist, passw = self.FindUser(username)

        if (exist):
            return (False)
        
        self.a.append([username, password])
        self.len += 1
        
        return(True)



    """
    Description: Deletes the user
    Parameter: username: String
    Returns: Boolean
    """
    def DeleteUser(self, username):
        exist, passw = self.FindUser(username)

        if (exist):
            for x in range(self.len):
                if (self.a[x][0] == username):
                    self.a.pop(x)
            self.len -= 1

            return(True)
        
        return(False)



    """
    Description: Logs out the user
    Parameter: username: String
    """
    def LogOutUser(self, username):
        self.b.remove(username)



# End of File