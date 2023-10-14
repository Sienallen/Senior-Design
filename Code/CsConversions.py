"""
File: CsConversions.py
Author: Ian Poremba (iporemba@uci.edu)
Author: Devin Reyes (devinnr@uci.edu)
Author: Allen Sien (siena@uci.edu)
Description: Contains the implementation of the chess conversions
Start date: 09/17/2022
Updated: 02/18/2023
"""



# ------------------------- Dependencies -------------------------



# ------------------------- Definitions --------------------------



"""
Description: Returns the value of the index based off the row and column
Parameter: row: Integer
Parameter: col: Integer
Returns: index: Integer
"""
def RowColtoIndex(row, col):
    index = row * 8 + col  # index of the coordinate

    return (index)



"""
Description: Returns the value of the row based off the index
Parameter: index: Integer
Returns: row: Integer
"""
def IndexToRow(index):
    row = index // 8  # row of the index

    return (row)



"""
Description: Returns the value of the column based off the index
Parameter: index: Integer
Returns: col: Integer
"""
def IndexToCol(index):
    col = index % 8  # column of the index

    return (col)



"""
Description: Returns the value of the index based off the inputted coordinate
Parameter: letters: String
Returns: index: Integer
"""
def LettersToIndex(letters):
    let = letters[0].lower()  # the initial letter of the position ie. A - H
    num = int(letters[1]) - 1  # the secondary number for the row 1 - 8
    index = num * 8

    if (let == 'a'):
        index += 0

    elif (let == 'b'):
        index += 1

    elif (let == 'c'):
        index += 2

    elif (let == 'd'):
        index += 3

    elif (let == 'e'):
        index += 4

    elif (let == 'f'):
        index += 5

    elif (let == 'g'):
        index += 6

    elif (let == 'h'):
        index += 7

    return (index)



"""
Description: Returns the value of the string based off the inputted index
Parameter: index: Integer
Returns: letters: String
"""
def IndexToLetters(index):
    col = IndexToCol(index)  # column of the index
    row = IndexToRow(index) + 1  # row of the index

    if (col == 0):
        letters = 'a'

    elif (col == 1):
        letters = 'b'

    elif (col == 2):
        letters = 'c'

    elif (col == 3):
        letters = 'd'

    elif (col == 4):
        letters = 'e'

    elif (col == 5):
        letters = 'f'

    elif (col == 6):
        letters = 'g'

    elif (col == 7):
        letters = 'h'

    letters = letters + str(row)

    return (letters)



# End of File
