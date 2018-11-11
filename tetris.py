from tkinter import *
import random
import copy
import decimal


####################################
# Shravan Ramamurthy
# sramamu1
# 10/04/2017
# built using specs that can be found
# at this website
# http://www.cs.cmu.edu/~112/notes/notes-tetris/2_5_RotatingTheFallingPiece.html
####################################

####################################
# Helper Functions
####################################
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))


# draws the cell given the following parameters
def drawCell(canvas, data, row, col, color):
    # calculate the coordinates based on the row and col
    coordX1 = data.margin + col * data.cellSize
    coordX2 = coordX1 + data.cellSize
    coordY1 = data.margin + row * data.cellSize
    coordY2 = coordY1 + data.cellSize
    # draw the cell
    canvas.create_rectangle(coordX1, coordY1, coordX2, coordY2,
							fill=color, outline="black",
							width=4)


# to draw the board, either empty or with blocks placed
def drawBoard(canvas, data):
	for row in range(data.rows):
		for col in range(data.cols):
			# iterates and calls drawCell
			drawCell(canvas, data, row, col,
					 data.board[row][col])


def standardPieces():
	# Seven "standard" pieces (tetrominoes)
	# taken from the website
	iPiece = [[True, True, True, True]]
	jPiece = [[True, False, False], [True, True, True]]
	lPiece = [[False, False, True], [True, True, True]]
	oPiece = [[True, True], [True, True]]
	sPiece = [[False, True, True], [True, True, False]]
	tPiece = [[False, True, False], [True, True, True]]
	zPiece = [[True, True, False], [False, True, True]]

	return [iPiece, jPiece, lPiece, oPiece,
			sPiece, tPiece, zPiece]


def standardColors():
	# seven "standard" colors
	# taken from the website
	return ["red", "yellow", "magenta", "pink", "cyan",
			"green", "orange"]


def newFallingPiece(data):
	# randomizes and chooses a piece and color
	randomIndex = random.randint(0, len(data.tetrisPieces) - 1)
	data.fallingPiece = data.tetrisPieces[randomIndex]
	data.fallingPieceColor = data.tetrisPieceColors[randomIndex]
	data.fallingPieceRow = 0
	# sets the center coordinates
	data.fallingPieceCol = data.cols // 2
	data.fallingPieceCol -= len(data.fallingPiece[0]) // 2


def drawFallingPiece(canvas, data):
	# iterates through the piece and draws it on top of the board.
	for row in range(len(data.fallingPiece)):
		for col in range(len(data.fallingPiece[row])):
			if data.fallingPiece[row][col]:
				# reuses the same code as the board.
				drawCell(canvas, data,
						 data.fallingPieceRow + row,
						 data.fallingPieceCol + col,
						 data.fallingPieceColor)


def fallingPieceIsLegal(data):
	# checks to see if the falling piece is legal
	for row in range(len(data.fallingPiece)):
		for col in range(len(data.fallingPiece[row])):
			if data.fallingPiece[row][col]:
				# is it on the board
				if (not data.fallingPieceRow + row in range(data.rows)
					or not data.fallingPieceCol + col in range(data.cols)):
					return False
				# is the color of the spot of the board blue
				if not data.board[data.fallingPieceRow + row]\
					[data.fallingPieceCol + col] == data.emptyColor:
					return False
	return True


def moveFallingPiece(data, drow, dcol):
	# moves the piece based on whether it is a legal move.
	data.fallingPieceRow += drow
	data.fallingPieceCol += dcol
	if not fallingPieceIsLegal(data):
		data.fallingPieceRow -= drow
		data.fallingPieceCol -= dcol
		return False
	return True


def rotateFallingPiece(data):
	# finds the dimensions and places of the new rotated piece.
	oldPiece = copy.deepcopy(data.fallingPiece)
	oldCol = data.fallingPieceCol
	oldRow = data.fallingPieceRow
	oldDimensions = [len(data.fallingPiece), len(data.fallingPiece[0])]
	newDimensions = [len(data.fallingPiece[0]), len(data.fallingPiece)]

	newRow = oldRow + oldDimensions[0] // 2 - newDimensions[0] // 2
	newCol = oldCol + oldDimensions[1] // 2 - newDimensions[1] // 2

	# use list comprehension to create a new array of the roated piece.
	newPiece = [[oldPiece[row][col] for row in range
	(newDimensions[1])]
				for col in range(newDimensions[0] - 1, -1, -1)]

	data.fallingPiece = newPiece
	data.fallingPieceRow = newRow
	data.fallingPieceCol = newCol

	# check if legal
	if not fallingPieceIsLegal(data):
		data.fallingPiece = oldPiece
		data.fallingPieceRow = oldRow
		data.fallingPieceCol = oldCol
		return False
	return True


def placeFallingPiece(data):
	# places the falling piece
	for row in range(len(data.fallingPiece)):
		for col in range(len(data.fallingPiece[row])):
			if data.fallingPiece[row][col]:
				(data.board[data.fallingPieceRow + row]
				 [data.fallingPieceCol + col]) = data.fallingPieceColor
	# check to see if the board should be cleared.
	removeFullRows(data)


def removeFullRows(data):
	# removes rows that don't have any blue squares.
	newBoard = []
	fullRows = 0

	# add to the new board.
	for row in data.board:
		if data.emptyColor in row:
			newBoard.append(row)
		else:
			fullRows += 1
	# add new rows to the top
	newBoard = [[data.emptyColor for col in range(data.cols)] for row \
				in range(fullRows)] + newBoard

	# add to the score if needed.
	if not data.board == newBoard:
		data.score += 1
	data.board = newBoard


####################################
# customize these functions
####################################

def init(data):
	# load data.xyz as appropriate
	data.rows = 15
	data.cols = 10
	data.cellSize = 20
	data.margin = 30
	data.emptyColor = "blue"
	# list comprehension to load with default values.
	data.board = [[data.emptyColor for i in range(data.cols)]
				  for j in range(data.rows)]
	data.tetrisPieces = standardPieces()
	data.tetrisPieceColors = standardColors()
	data.isGameOver = False
	data.score = 0
	# call for the first time.
	newFallingPiece(data)


def keyPressed(event, data):
	# use event.char and event.keysym
	# various commands to control the board.
	if event.keysym == "Left":
		moveFallingPiece(data, 0, -1)
	elif event.keysym == "Right":
		moveFallingPiece(data, 0, 1)
	elif event.keysym == "Up":
		rotateFallingPiece(data)
	elif event.keysym == "Down":
		moveFallingPiece(data, 1, 0)
	elif event.char == "r":
		init(data)


# have a timer that keeps moving the piece downwards.
def timerFired(data):
	if not data.isGameOver:
		# have a new falling piece and see if the game is over.
		if not moveFallingPiece(data, 1, 0):
			placeFallingPiece(data)
			newFallingPiece(data)
			if not fallingPieceIsLegal(data):
				data.isGameOver = True


def redrawAll(canvas, data):
	# draw in canvas
	canvas.create_rectangle(0, 0, data.width, data.height,
							fill="gold2", width=0)
	canvas.create_text(data.width * 0.5,
					   data.margin / 5,
					   text="Score: " + str(data.score),
					   fill="blue",
					   font="Helvetica 14 bold",
					   anchor="n")
	# makes sure that the board can't be modified after the game is over
	if data.isGameOver:
		drawBoard(canvas, data)
		# game over sign
		canvas.create_rectangle(data.margin,
								data.height * 0.25,
								data.width - data.margin,
								data.height * 0.35,
								fill="black")
		canvas.create_text(data.width * 0.5,
						   data.height * 0.31,
						   text="Game Over!",
						   fill="gold2",
						   font="Helvetica 24",
						   anchor="center")
	else:
		# regular board with falling pieces
		drawBoard(canvas, data)
		drawFallingPiece(canvas, data)


####################################
# use the run function as-is
####################################
def playTetris():
	# finds the margin based on the default options for the board.
	rowLength = 10
	colLength = 15
	cellSize = 20
	margin = 30
	width = rowLength * cellSize + margin * 2
	height = colLength * cellSize + margin * 2
	run(width, height)


def run(width=300, height=300):
	def redrawAllWrapper(canvas, data):
		canvas.delete(ALL)
		canvas.create_rectangle(0, 0, data.width, data.height,
								fill='white', width=0)
		redrawAll(canvas, data)
		canvas.update()

	def keyPressedWrapper(event, canvas, data):
		keyPressed(event, data)
		redrawAllWrapper(canvas, data)

	def timerFiredWrapper(canvas, data):
		timerFired(data)
		redrawAllWrapper(canvas, data)
		# pause, then call timerFired again
		canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

	# Set up data and call init
	class Struct(object): pass

	data = Struct()
	data.width = width
	data.height = height
	data.timerDelay = 200  # milliseconds
	init(data)
	# create the root and the canvas
	root = Tk()
	canvas = Canvas(root, width=data.width, height=data.height)
	canvas.pack()
	# set up events
	root.bind("<Key>", lambda event:
	keyPressedWrapper(event, canvas, data))
	timerFiredWrapper(canvas, data)
	# and launch the app
	root.mainloop()  # blocks until window is closed
	print("bye!")


def testNewFallingPiece():
	print("Testing newFallingPiece...", end="")

	class Struct(object):
		pass

	data = Struct()
	for i in range(10):
		init(data)
		if data.fallingPiece == data.tetrisPieces[0]:
			assert (data.fallingPieceCol == 3)
		else:
			assert (data.fallingPieceCol == 4)
	print("Passed!")


def testFallingPieceIsLegal():
	print("Testing fallingPieceIsLegal...", end="")

	class Struct(object): pass

	data = Struct()

	init(data)

	data.fallingPieceCol = 10
	data.fallingPieceRow = 3
	assert (fallingPieceIsLegal(data) == False)

	data.fallingPieceCol = 3
	data.fallingPieceRow = 14
	assert (fallingPieceIsLegal(data) == False)

	data.fallingPieceCol = 3
	data.fallingPieceRow = 11
	assert (fallingPieceIsLegal(data) == True)

	print("Passed!")


def testMoveFallingPiece():
	print("Testing moveFallingPiece...", end="")

	class Struct(object): pass

	data = Struct()
	init(data)

	data.fallingPieceRow = 14
	data.fallingPieceCol = 3
	assert (moveFallingPiece(data, 1, 0) == False)

	data.fallingPieceRow = 11
	data.fallingPieceCol = 3
	assert (moveFallingPiece(data, 1, 0) == True)

	print("Passed!")


def testRotateFallingPiece():
	print("Testing roateFallingPiece...", end="")

	class Struct(object): pass

	data = Struct()
	init(data)

	data.fallingPiece = data.tetrisPieces[1]
	data.fallingPieceRow = 0
	data.fallingPieceCol = 5
	assert (rotateFallingPiece(data) == True)

	data.fallingPiece = data.tetrisPieces[1]
	data.fallingPieceRow = 14
	data.fallingPieceCol = 5
	assert (rotateFallingPiece(data) == False)

	print("Passed!")


def testPlaceFallingPiece():
	print("Testing placeFallingPiece...", end="")

	class Struct(object): pass

	data = Struct()
	init(data)

	data.fallingPiece = data.tetrisPieces[1]
	data.fallingPieceRow = 13
	data.fallingPieceCol = 3
	timerFired(data)

	assert (data.fallingPieceRow == 0)
	print("Passed!")


def testRemoveFullRows():
	print("Testing removeFullRows...", end="")

	class Struct(object): pass

	data = Struct()
	init(data)
	data.board[14] = ["red" for i in range(10)]
	removeFullRows(data)
	assert ("blue" in data.board[14])

	data.board[14] = ["green" for i in range(10)]
	removeFullRows(data)
	assert ("blue" in data.board[14])
	print("Passed!")


def testAll():
	testNewFallingPiece()
	testFallingPieceIsLegal()
	testMoveFallingPiece()
	testRotateFallingPiece()
	testPlaceFallingPiece()
	testRemoveFullRows()


def main():
	testAll()
	playTetris()


if __name__ == '__main__':
	main()
