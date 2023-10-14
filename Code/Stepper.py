"""
File: CsConversions.py
Author: Ian Poremba (iporemba@uci.edu)
Author: Devin Reyes (devinnr@uci.edu)
Author: Allen Sien (siena@uci.edu)
Description: Contains the implementation of the Motor's movement and Electromagnet
Start date: 12/15/2022
Updated: 03/12/2023
"""



# ------------------------- Dependencies -------------------------

import board
import RPi.GPIO as GPIO
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
from CsConversions import IndexToCol, IndexToRow, RowColtoIndex
from ImageProcessing import cap_pre_img

# ------------------------- Definitions --------------------------



square = 276
drag = 70
dragCorner = 50
killDistance = 95



def Move(start, end, capLocation, cap, color, castle, client):
    startRow = IndexToRow(start)
    startCol = IndexToCol(start)
    endRow = IndexToRow(end)
    endCol = IndexToCol(end)
    motorRow = 4
    motorCol = 4
    corner = "dL"
    cap = True if (cap == "T") else False
    color = True if (color == "T") else False
    castle = True if (castle == "T") else False
    
    if (castle):
        castleDirection = "r" if (end > start) else "l"

    else:
        castleDirection = "n"
    
    if (cap):
        capRow = IndexToRow(capLocation)
        capCol = IndexToCol(capLocation)
        motorRow, motorCol, corner = NewCornerConvert(motorRow, motorCol, capRow, capCol, corner)
        MoveMotors(motorRow, motorCol, capRow, capCol)
        motorRow, motorCol, corner = KillRelease(color, capRow, capCol, corner)

    motorRow, motorCol, corner = NewCornerConvert(motorRow, motorCol, startRow, startCol, corner)
    MoveMotors(motorRow, motorCol, startRow, startCol)
    CenterCornerChange(False, True, corner)
    corner = OldCornerConvert(startRow, startCol, endRow, endCol)
    CenterCornerChange(True, True, corner)
    startRow, startCol, corner = NewCornerConvert(startRow, startCol, endRow, endCol, corner)
    MoveMotorsDragging(startRow, startCol, endRow, endCol)
    CenterCornerChange(False, False, corner)

    if (castleDirection == "r"):
        startCastleCol = 7
        endCastleCol = 5

        if (color):
            CastleRow = 0

        else:
            CastleRow = 7

        corner = OldCornerConvert(endRow, endCol, CastleRow, startCastleCol)
        CenterCornerChange(True, False, corner)
        endRow, endCol, corner = NewCornerConvert(endRow, endCol, CastleRow, startCastleCol, corner)
        MoveMotors(endRow, endCol, CastleRow, startCastleCol)
        CenterCornerChange(False, True, corner)
        corner = OldCornerConvert(CastleRow, startCastleCol, CastleRow, endCastleCol)
        CenterCornerChange(True, True, corner)
        CastleRow, startCastleCol, corner = NewCornerConvert(CastleRow, startCastleCol, CastleRow, endCastleCol, corner)
        MoveMotorsDragging(CastleRow, startCastleCol, CastleRow, endCastleCol)
        CenterCornerChange(False, False, corner)
        corner = OldCornerConvert(CastleRow, endCastleCol, 4, 4)
        CenterCornerChange(True, False, corner)
        ReturnHome(CastleRow, endCastleCol, corner)

    elif (castleDirection == "l"):
        startCastleCol = 0
        endCastleCol = 3

        if (color):
            CastleRow = 0

        else:
            CastleRow = 7

        corner = OldCornerConvert(endRow, endCol, CastleRow, startCastleCol)
        CenterCornerChange(True, False, corner)
        endRow, endCol, corner = NewCornerConvert(endRow, endCol, CastleRow, startCastleCol, corner)
        MoveMotors(endRow, endCol, CastleRow, startCastleCol)
        CenterCornerChange(False, True, corner)
        corner = OldCornerConvert(CastleRow, startCastleCol, CastleRow, endCastleCol)
        CenterCornerChange(True, True, corner)
        CastleRow, startCastleCol, corner = NewCornerConvert(CastleRow, startCastleCol, CastleRow, endCastleCol, corner)
        MoveMotorsDragging(CastleRow, startCastleCol, CastleRow, endCastleCol)
        CenterCornerChange(False, False, corner)
        corner = OldCornerConvert(CastleRow, endCastleCol, 4, 4)
        CenterCornerChange(True, False, corner)
        ReturnHome(CastleRow, endCastleCol, corner)

    else:
        corner = OldCornerConvert(endRow, endCol, 4, 4)
        CenterCornerChange(True, False, corner)
        ReturnHome(endRow, endCol, corner)

    client.ClientSend("Asig")
    cap_pre_img()



def ReturnHome(startRow, startCol, corner):
    if (corner[0] == "u"):
        startRow += 1
    
    if (corner[1] == "R"):
        startCol += 1

    MoveMotors(startRow, startCol, 4, 4)



def MoveMotors(startRow, startCol, endRow, endCol):
    xDis = endCol - startCol
    yDis = endRow - startRow
    
    diagonalDis = min(abs(xDis), abs(yDis)) * square
    straightDis = max(abs(xDis), abs(yDis)) * square - diagonalDis
    smallIsX = True if (abs(xDis) * square == diagonalDis) else False

    if (xDis > 0):
        if (yDis > 0):
            if (smallIsX):
                MoveMotorsStraight("u", straightDis)
            
            else:
                MoveMotorsStraight("r", straightDis)

            MoveMotorsLeft("u", diagonalDis)

        else:
            if (smallIsX):
                MoveMotorsStraight("d", straightDis)
            
            else:
                MoveMotorsStraight("r", straightDis)

            MoveMotorsRight("d", diagonalDis)

    else:
        if (yDis > 0):
            if (smallIsX):
                MoveMotorsStraight("u", straightDis)
            
            else:
                MoveMotorsStraight("l", straightDis)

            MoveMotorsRight("u", diagonalDis)

        else:
            if (smallIsX):
                MoveMotorsStraight("d", straightDis)
            
            else:
                MoveMotorsStraight("l", straightDis)

            MoveMotorsLeft("d", diagonalDis)



def KillRelease(white, capRow, capCol, corner):
    if (white):
        CenterCornerChange(False, True, corner)
        corner = OldCornerConvert(capRow, capCol, 4, 7)
        CenterCornerChange(True, False, corner)
        MoveMotorsDragging(capRow, capCol, 4, 7)
        MoveMotorsStraight("r", killDistance)
        MoveMotorsStraight("u", square)
        MoveMotorsStraight("d", square)
        Drag("d", True, False)
        MoveMotorsStraight("l", square + killDistance)

        return (4, 7, "dL")

    else:
        CenterCornerChange(False, True, corner)
        corner = OldCornerConvert(capRow, capCol, 4, 0)
        CenterCornerChange(True, False, corner)
        MoveMotorsDragging(capRow, capCol, 4, 0)
        MoveMotorsStraight("l", killDistance)
        MoveMotorsStraight("d", square)
        MoveMotorsStraight("u", square)
        Drag("u", True, False)
        MoveMotorsStraight("r", square + killDistance)

        return (4, 0, "dR")



def CenterCornerChange(inCenter, mag, corner):
    if (inCenter):
        if (corner == "uR"):
            MoveMotorsLeft("u", square // 2)

        elif (corner == "dR"):
            MoveMotorsRight("d", square // 2)

        elif (corner == "uL"):
            MoveMotorsRight("u", square // 2)

        elif (corner == "dL"):
            MoveMotorsLeft("d", square // 2)

    else:
        if (corner == "uR"):
            MoveMotorsLeft("d", square // 2)
            
            if (mag):
                Magnet(True)
            
            else:
                Drag(corner, False, True)

        elif (corner == "dR"):
            MoveMotorsRight("u", square // 2)
            
            if (mag):
                Magnet(True)
            
            else:
                Drag(corner, False, True)

        elif (corner == "uL"):
            MoveMotorsRight("d", square // 2)
            
            if (mag):
                Magnet(True)
            
            else:
                Drag(corner, False, True)

        elif (corner == "dL"):
            MoveMotorsLeft("u", square // 2)
            
            if (mag):
                Magnet(True)
            
            else:
                Drag(corner, False, True)



def Drag(direction, release, inCorner):
    if (inCorner):
        if (direction == "dL"):
            MoveMotorsLeft("u", dragCorner)
            Magnet(False)
            MoveMotorsLeft("d", dragCorner)

        elif (direction == "uL"):
            MoveMotorsRight("d", dragCorner)
            Magnet(False)
            MoveMotorsRight("u", dragCorner)

        elif (direction == "dR"):
            MoveMotorsRight("u", dragCorner)
            Magnet(False)
            MoveMotorsRight("d", dragCorner)

        elif (direction == "uR"):
            MoveMotorsLeft("d", dragCorner)
            Magnet(False)
            MoveMotorsLeft("u", dragCorner)

    else:
        if (direction == "u"):
            opp = "d"

        elif (direction == "d"):
            opp = "u"

        elif (direction == "r"):
            opp = "l"

        elif (direction == "l"):
            opp = "r"

        MoveMotorsStraight(direction, drag)

        if (release):
            Magnet(False)

        MoveMotorsStraight(opp, drag)



def MoveMotorsDragging(startRow, startCol, endRow, endCol):
    if (startRow > endRow):
        MoveMotorsStraight("d", (startRow - endRow) * square)

    else:
        MoveMotorsStraight("u", (endRow - startRow) * square)

    if (startCol > endCol):
        MoveMotorsStraight("l", (startCol - endCol) * square)

    else:
        MoveMotorsStraight("r", (endCol - startCol) * square)



def MoveMotorsStraight(direction, steps):
    kit = MotorKit(i2c=board.I2C())
    kit.stepper1.release()
    kit.stepper2.release()

    if (direction == "u"):
        for i in range(int(steps)):
            kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)  
            kit.stepper2.onestep(style=stepper.DOUBLE)  

    elif (direction == "d"):
        for i in range(int(steps)):
            kit.stepper1.onestep(style=stepper.DOUBLE)
            kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)

    elif (direction == "r"):
        for i in range(int(steps)):
            kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)  
            kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)

    elif (direction == "l"):
        for i in range(int(steps)):
            kit.stepper1.onestep(style=stepper.DOUBLE) 
            kit.stepper2.onestep(style=stepper.DOUBLE) 
    
    kit.stepper1.release()
    kit.stepper2.release()



def MoveMotorsRight(direction, steps):
    kit = MotorKit(i2c=board.I2C())
    kit.stepper2.release()

    if (direction == "d" or direction == "r"):
        for i in range(int(2 * steps)):
            kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)  

    elif (direction == "u" or direction == "l"):
        for i in range(int(2 * steps)):
            kit.stepper2.onestep(style=stepper.DOUBLE)
    
    kit.stepper2.release()



def MoveMotorsLeft(direction, steps):
    kit = MotorKit(i2c=board.I2C())
    kit.stepper1.release()

    if (direction == "u" or direction == "r"):
        for i in range(int(2 * steps)):
            kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)  

    elif (direction == "d" or direction == "l"):
        for i in range(int(2 * steps)):
            kit.stepper1.onestep(style=stepper.DOUBLE)
    
    kit.stepper1.release()



def Magnet(on):
    if (on):
        GPIO.output(18, 1)

    else:
        GPIO.output(18, 0)



def NewCornerConvert(startRow, startCol, endRow, endCol, corner):
    rowDirection = "u" if (startRow > endRow or endRow == 0) else "d"
    colDirection = "R" if (startCol > endCol or endCol == 0) else "L"

    if (corner[0] == "d" and rowDirection == "u"):
        startRow -= 1

    elif (corner[0] == "u" and rowDirection == "d"):
        startRow += 1

    if (corner[1] == "L" and colDirection == "R"):
        startCol -= 1

    elif (corner[1] == "R" and colDirection == "L"):
        startCol += 1

    return (startRow, startCol, rowDirection + colDirection)



def OldCornerConvert(startRow, startCol, endRow, endCol):
    rowDirection = "u" if (endRow > startRow or startRow == 0) else "d"
    colDirection = "R" if (endCol > startCol or startCol == 0) else "L"

    return (rowDirection + colDirection)



# End of File