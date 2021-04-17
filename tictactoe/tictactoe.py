"""
Tic Tac Toe Player
"""

import math, copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    if terminal(board):
    	return None

    sumX = sum(row.count(X) for row in board)
    sumO = sum(row.count(O) for row in board)

    if sumX == sumO + 1:
    	return O
    elif sumX == sumO:
    	return X
    else:
    	return None

    raise NotImplementedError


def actions(board):

	actionSet = []

	for i in [0, 1, 2]:
		for j in [0, 1, 2]:
			if board[i][j] is None:
				actionSet.append((i, j))


	return actionSet


def result(board, action): #action = (i, j)

	i = action[0]
	j = action[1]

	if board[i][j] is not None:
		raise Exception("result function error: position filled")
	newboard = copy.deepcopy(board)

	newboard[i][j] = player(board)

	return newboard

def winner(board):

    for i in [0, 1, 2]:
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
    for j in [0, 1, 2]:
        if board[0][j] == board[1][j] == board[2][j] and board[0][j] is not None:
            return board[0][j]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[2][0] is not None:
        return board[0][2]
    return None


def terminal(board):
    if winner(board) is not None:
        return True

    for row in board:
        if None in row:
            return False
    return True

    raise Exception("terminal error")


def utility(board):
    if winner(board) is X:
        return 1
    if winner(board) is O:
        return -1
    return 0


def minimax(board):
    if terminal(board):
        return None
        
    if player(board) is X: #pursues max
        value = -2
        for action in actions(board):
            testvalue = minimum(result(board, action))
            if testvalue > value:
                value = testvalue
                move = action
        return move


    if player(board) is O: # pursues min
        value = 2
        for action in actions(board):
            testvalue = maximum(result(board, action))
            if testvalue < value:
                value = testvalue
                move = action
        return move

def maximum(board):
    if terminal(board):
        return utility(board)
    value = -3
    for action in actions(board):
        value = max(value, minimum(result(board, action)))
    return value

def minimum(board):
    if terminal(board):
        return utility(board)
    value = 3
    for action in actions(board):
        value = min(value, maximum(result(board, action)))
    return value