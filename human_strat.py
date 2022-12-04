# ABOUT: used for testing

def getMove(board, color, time_left):
	#print(board)
	if color == 1:
		print("Black to Move")
	else:
		print("White to Move")
	mv = input("enter coordinates of your move, separated by spaces: ")
	mv= mv.split()
	return (int(mv[0]),int(mv[1]))
