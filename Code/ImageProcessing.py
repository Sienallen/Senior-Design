"""
File: ImgProc.py
Author: Ian Poremba (iporemba@uci.edu)
Author: Devin Reyes (devinnr@uci.edu)
Author: Allen Sien (siena@uci.edu)
Description: Contains code necessary to process moves made by players
Date: 11/22/2022
Updated: 03/15/2023
"""


# ------------------------- Dependencies -------------------------

import cv2 as cv
import numpy as np
import imutils
import glob
from matplotlib import pyplot as plt
import time
from CsConversions import LettersToIndex
from CsPieceRules import IsValidMove

# ------------------------- Definitions --------------------------



row0 = [478, 515]
row1 = [429, 468]
row2 = [381, 419]
row3 = [334, 373]
row4 = [285, 324]
row5 = [240, 279]
row6 = [192, 230]
row7 = [142, 183]
colA = [387, 422]
colB = [338, 377]
colC = [291, 327]
colD = [244, 281]
colE = [197, 235]
colF = [149, 186]
colG = [102, 140]
colH = [52, 93]
rows = [row0, row1, row2, row3, row4, row5, row6, row7]
cols = [colA, colB, colC, colD, colE, colF, colG, colH]
  
  
  
"""
Description: This function turns on the webcam to take the initial image before a player
makes a move
"""
def cap_pre_img():
	cap = cv.VideoCapture(0)
	for i in range(10):
		return_value, image = cap.read()
		cv.imwrite('saved_img1'+str(i)+'.jpg', image)
	files = glob.glob ("saved_img1*.jpg")
	image_data = []
	for my_file in files:
		this_image = cv.imread(my_file, 1)
		image_data.append(this_image)

    # Calculate average image
	dst = image_data[0]
	for i in range(len(image_data)):
		if i == 0:
			pass
		else:
			alpha = 1.0/(i + 1)
			beta = 1.0 - alpha
			dst = cv.addWeighted(image_data[i], alpha, dst, beta, 0.0)
			
	cv.imwrite('saved_img1.jpg', dst)
  
  

"""
Description: This function turns on the webcam to take the after image once a player
makes a move and moves their chosen piece. 
"""
def cap_post_img():
	cap = cv.VideoCapture(0)
	for i in range(10):
		return_value, image = cap.read()
		cv.imwrite('saved_img2'+str(i)+'.jpg', image)
	files = glob.glob ("saved_img2*.jpg")
	image_data = []
	for my_file in files:
		this_image = cv.imread(my_file, 1)
		image_data.append(this_image)

    # Calculate average image
	dst = image_data[0]
	for i in range(len(image_data)):
		if i == 0:
			pass
		else:
			alpha = 1.0/(i + 1)
			beta = 1.0 - alpha
			dst = cv.addWeighted(image_data[i], alpha, dst, beta, 0.0)
			
	cv.imwrite('saved_img2.jpg', dst)



"""
Description: Creates arrays containing the positions of each colors pieces
Parameter: image: String
"""
def FindArrays(image):
	img  = cv.imread(image)
	img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

	red1 = cv.inRange(img_hsv, (0,50,20), (5,255,255))
	red2 = cv.inRange(img_hsv, (175,50,20), (180,255,255))
	green = cv.inRange(img_hsv, (60,50,20), (80,255,255))
	maskR = cv.bitwise_or(red1, red2)
	maskG = cv.bitwise_or(green, green)
	
	tempG = [0] * (len(img) * len(img[0]))

	for x in range(2, len(img) - 2):
		for y in range(2, len(img[0]) - 2):
			countG = 0

			if (maskG[x][y] == 255):
				for r in range(x - 2, x + 2):
					for c in range(y - 2, y + 2):
						if (maskG[r][c] == 255):
							countG += 1
				
				tempG[x * len(img[0]) + y] = 255 if (countG > 8) else 0
				
	for x in range(len(img)):
		for y in range(len(img[0])):
			maskG[x][y] = tempG[x * len(img[0]) + y]
	
	tempR = [0] * (len(img) * len(img[0]))

	for x in range(2, len(img) - 2):
		for y in range(2, len(img[0]) - 2):
			countR = 0

			if (maskR[x][y] == 255):
				for r in range(x - 2, x + 2):
					for c in range(y - 2, y + 2):
						if (maskR[r][c] == 255):
							countR += 1
				
				tempR[x * len(img[0]) + y] = 255 if (countR > 8) else 0
				
	for x in range(len(img)):
		for y in range(len(img[0])):
			maskR[x][y] = tempR[x * len(img[0]) + y]

	tileG = [maskG] * 64
	tileR = [maskR] * 64
	tilesG = [0] * 64
	tilesR = [0] * 64

	for row in range(8):
		rowx = rows[row]
		for col in range(8):
			coly = cols[col]
			index = row * 8 + col
			tileG[index] = maskG[coly[0]: coly[1], rowx[0]: rowx[1]]
			tileR[index] = maskR[coly[0]: coly[1], rowx[0]: rowx[1]]

			for x in range(len(tileG[0])):
				for y in range(len(tileG[0][0])):
					if (tilesG[index] == 1 and tilesR[index] == 1):
						break
						
					if (tileG[index][x][y] == 255):
						tilesG[row * 8 + col] = 1

					if (tileR[index][x][y] == 255):
						tilesR[row * 8 + col] = 1

	return (tilesR, tilesG, tileR, tileG, maskR, maskG)



"""
Description: Compares pre and post arrays of players pieces
Returns: start: Integer; end: Integer
"""
def CompareArrays():
	preWhite, preBlack, preimagew, preimageb, prmaskw, prmaskb = FindArrays('saved_img1.jpg')
	postWhite, postBlack, postimagew, postimageb, pomaskw, pomaskb = FindArrays('saved_img2.jpg')

	moveBlack = [64] * 4
	moveWhite = [64] * 4
	start = 64
	end = 64
	wCount = 0
	bCount = 0

	for x in range(64):
		if (preWhite[x] == 1 and postWhite[x] == 0):
			wCount += 1
			
			if (moveWhite[0] == 64):
				moveWhite[0] = x

			else:
				moveWhite[1] = x

		elif (preWhite[x] == 0 and postWhite[x] == 1):
			wCount += 1
			
			if (moveWhite[3] == 64):
				moveWhite[3] = x

			else:
				moveWhite[2] = x

		if (preBlack[x] == 1 and postBlack[x] == 0):
			bCount += 1
			
			if (moveBlack[0] == 64):
				moveBlack[0] = x

			else:
				moveBlack[1] = x

		elif (preBlack[x] == 0 and postBlack[x] == 1):
			bCount += 1
			
			if (moveBlack[3] == 64):
				moveBlack[3] = x

			else:
				moveBlack[2] = x

	if (wCount == 4 and bCount == 0 and 4 in moveWhite):
		if (7 in moveWhite):
			start = 4
			end = 6

		elif (0 in moveWhite):
			start = 4
			end = 2

	elif (bCount == 4 and wCount == 0 and 60 in moveBlack):
		if (63 in moveBlack):
			start = 60
			end = 62

		elif (56 in moveBlack):
			start = 60
			end = 58

	elif (wCount == 2 and (bCount == 1 or bCount == 0)):
		start = moveWhite[0]
		end = moveWhite[3]

	elif (bCount == 2 and (wCount == 1 or wCount == 0)):
		start = moveBlack[0]
		end = moveBlack[3]

	else:
		"""plt.imshow(prmaskw, cmap='gray')
		plt.show()
		plt.imshow(prmaskb, cmap='gray')
		plt.show()
		plt.imshow(pomaskw, cmap='gray')
		plt.show()
		plt.imshow(pomaskb, cmap='gray')
		plt.show()

		for x in range(4):
			if (moveWhite[x] != 64):
				plt.imshow(preimagew[x], cmap='gray')
				plt.show()
				plt.imshow(postimagew[x], cmap='gray')
				plt.show()

			if (moveBlack[x] != 64):
				plt.imshow(preimageb[x], cmap='gray')
				plt.show()
				plt.imshow(postimageb[x], cmap='gray')
				plt.show()"""
	
		"""for y in range(8):
			print()
			for z in range(8):
				print(preWhite[y * 8 + x]) 
				
		for y in range(8):
			print()
			for z in range(8):
				print(postWhite[y * 8 + x]) 

		for y in range(8):
			print()
			for z in range(8):
				print(preBlack[y * 8 + x]) 

		for y in range(8):
			print()
			for z in range(8):
				print(postBlack[y * 8 + x])"""
	
		print(moveWhite, moveBlack)

	return (start, end)
	


if __name__ == "__main__":
	cap_pre_img()
	#x = input()
	#cap_post_img()
	img  = cv.imread('saved_img1.jpg')
	#plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
	#plt.show()
	print(FindArrays('saved_img1.jpg'))
 

	 
# End Of File

