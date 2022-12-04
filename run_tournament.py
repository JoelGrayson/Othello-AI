# <Players
import human_strat
import random_strat
import joel_strat

# Play Random
playerNames = ['joel_strat', 'random_strat']
player_modules = [joel_strat, random_strat]
    
# # Play Human
# playerNames = ['joel_strat', 'human_strat']
# player_modules = [joel_strat, human_strat]

# Play Itself
playerNames = ['joel_strat', 'joel_strat']
player_modules = [joel_strat, joel_strat]

# >








import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import time
import random


# hack - index 1 is black, index -1 is white
players = ["", "Black", "White"]

SIZE = 8


class Othello:

	def __init__(self, blackModule, whiteModule):
		self.board = np.zeros((SIZE, SIZE), dtype=np.int8)
		self.turn = 1  # will be -1 (white) or 1 (black)

		# starting board state
		self.board[3, 3] = -1
		self.board[4, 4] = -1
		self.board[3, 4] = 1
		self.board[4, 3] = 1

		# CHANGE MODULE NAMES TO TEST AIs
		self.black = blackModule.getMove
		self.white = whiteModule.getMove

		self.max_time = 1800  # maximum time (seconds) allocated
		# to each AI for the whole game
		self.cur_times = [0, 0]  # elapsed time for white, black

		plt.ion()  # turn on interactive mode

		winner = self.play()  # game loop
		# input("game over")
		plt.ioff()  #
		if winner == 1:
			winner = blackModule.__name__
		elif winner == -1:
			winner = whiteModule.__name__
		else:
			winner = "Draw"
		input(f"game over. Winner: {winner}")
		plt.close()  # close image of board

	def showBoard(self):
		plt.clf()  # clear previous board

		# green background
		green = np.array([0, 100, 0, 255], dtype=np.uint8)
		imArr = np.full((800, 800, 4), green)

		# convert to PIL image to use ImageDraw module
		im = Image.fromarray(imArr)
		draw = ImageDraw.Draw(im)

		# draw gridlines
		for i in range(100, 800, 100):
			draw.line((i, 0, i, im.size[1]), fill="white", width=3)
		for j in range(100, 800, 100):
			draw.line((0, j, im.size[0], j), fill="white", width=3)

		# draw stones
		for r in range(SIZE):
			for c in range(SIZE):
				if self.board[r, c] == 1:
					draw.ellipse([100 * c + 5, 100 * r + 5, 100 * c + 95, 100 * r + 95],
					             fill="black")
				elif self.board[r, c] == -1:
					draw.ellipse([100 * c + 5, 100 * r + 5, 100 * c + 95, 100 * r + 95],
					             fill="white")

		# convert back to array so plt can plot it.
		arr = np.array(im)
		fig = plt.imshow(arr)

		# get rid of axis ticks and numbers
		# plt.axis('off')
		# fig.axes.get_xaxis().set_visible(False)
		# fig.axes.get_yaxis().set_visible(False)
		plt.xticks(range(50, 800, 100), range(8))
		plt.yticks(range(50, 800, 100), range(8))

		# show updated image
		plt.draw()
		plt.pause(.1)

	# return List of stones to flip if move is legal
	# empty list otherwise
	def checkMove(self, row, col):
		# position is not empty
		if self.board[row, col] != 0:
			return []
		stonesToFlip = []

		# 8 directions
		#			  down	  up	  right	  left	  dr 	  dl	   ur		ul
		directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1),
		              (-1, -1)]
		for d in directions:
			flank = False
			r = row + d[0]  # first position we're checking
			c = col + d[1]  # in the current direction

			# temporary list of positions to flip
			# don't know if accurate until we find that the stones are surrounded
			tempflips = []
			# while we're still on the board

			while r >= 0 and r < SIZE and c >= 0 and c < SIZE:
				# first we should find stones of opponts color
				if self.board[r, c] == -self.turn:
					flank = True
					tempflips.append((r, c))  # opponent stones we might flip

				# then a stone of our color, so the line is surrounded
				elif self.board[r, c] == self.turn:
					if flank:  # found stones of opponent color surrounded by our color
						stonesToFlip += tempflips
						break

					else:  # if no stones of opponents color
						break  # break without adding any stones

				else:  # found a blank spot when expecting something else
					break  # break without adding any stones

				r += d[0]  # next
				c += d[1]  # position

			# if we reached the end of the loop without finding flanked stones, no stones are added
		# We've searched all directions
		return stonesToFlip

	# Return False if there are any legal moves for either player
	def noMoves(self, check=[-1, 1]):
		turnSave = self.turn  # actual turn
		for t in check:  # check both playersif necessary
			self.turn = t
			for i in range(SIZE):
				for j in range(SIZE):
					# only run checkMove if spot is empty
					# since checkMove is expensive
					if self.board[i, j] == 0:
						if self.checkMove(i, j):
							self.turn = turnSave  # restore correct turn
							return False

		self.turn = turnSave  # restore correct turn
		return True

	# calculate black and white scores
	def score(self):
		score_black = 0
		score_white = 0

		# loop through board, count stones
		for r in range(SIZE):
			for c in range(SIZE):
				if self.board[r, c] == 1:
					score_black += 1
				elif self.board[r, c] == -1:
					score_white += 1
		return (score_black, score_white)

	def play(self):
		self.showBoard()
		while not self.noMoves():

			# convert [-1,1] to [0, 1]
			ind = (self.turn + 1) // 2
			time_left = self.max_time - self.cur_times[ind]

			# print(self.board) #replace this with GUI
			# Get move from AI
			if self.turn == 1:
				print("Black's turn")
				# measure time expired within function call
				tstart = time.time()
				move = self.black(self.board.copy(), 1, time_left)
				tend = time.time()
			else:
				print("White's turn")
				tstart = time.time()
				move = self.white(self.board.copy(), -1, time_left)
				tend = time.time()
				
			# add time elapsed this move
			self.cur_times[ind] += tend - tstart

			print("Time Remaining\nBlack: {}\nWhite: {}".format(
			 self.max_time - self.cur_times[1], self.max_time - self.cur_times[0]))

			# Timeout game over condition
			if self.cur_times[ind] > self.max_time:
				print("{} is out of time. {} wins!".format(players[self.turn],
				                                           players[-self.turn]))

				return -self.turn
			try:
				if move[0] >= -1 and move[0] < SIZE and move[1] >= -1 and move[1] < SIZE:
					pass
				else:
					print(
					 f"Illegal Move ({move}) by {players[self.turn]}. {players[-self.turn]} wins!"
					)
					return -self.turn
			except:
				print(
				 f"Illegal Move ({move}) by {players[self.turn]}. {players[-self.turn]} wins!"
				)
				return -self.turn

			if (move[0], move[1]) == (-1, -1):  #if player passed
				if self.noMoves([self.turn]):
					self.turn *= -1
					continue
				else:
					print(
					 f"Illegal pass by {players[self.turn]}. {players[-self.turn]} wins!")
					return -self.turn
			# list of stones to flip, empty if illegal

			flips = self.checkMove(move[0], move[1])
			if flips:
				self.board[move] = self.turn  #place stone
				for pos in flips:  #flips stones
					self.board[pos] *= -1
			else:  #move was invalid. Player auto-loss
				print(
				 f"Illegal Move ({move}) by {players[self.turn]}. {players[-self.turn]} wins!"
				)
				return -self.turn

			self.showBoard()
			self.turn *= -1  #toggle turn

		# calculate Final scores and declare winner.
		sb, sw = self.score()
		print("Final Score: Black {}, White {}".format(sb, sw))
		if sb > sw:
			print("Black wins")
			return 1
		elif sb < sw:
			print("White wins")
			return -1
		else:
			print("It's a draw!")


def main():
	num_players = len(playerNames)

	# create all unique matchups (order matters)
	matchups = [(i, j) for i in range(num_players) for j in range(num_players)
	            if i != j]

	random.shuffle(matchups)
	print(matchups)

	gameNum = 1
	for p1, p2 in matchups:
		print("Game {}: {}(black) vs. {}(white)".format(gameNum, playerNames[p1],
		                                                playerNames[p2]))
		skip = input("Press Enter to begin")
		if skip != 's':
			o = Othello(player_modules[p1], player_modules[p2])
		print("--------------")
		gameNum += 1


if __name__ == '__main__':
	main()
