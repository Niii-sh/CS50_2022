"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.

    生成初始棋盘 这个没啥好修改的
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.

    判断当前是谁的回合
    这里我的思路是
    通过当前棋盘上的棋子数目进行判断 X比O 多一个 那么当前就是 O的回合 反之同理
    当然也不要忘了 判断此时棋盘的状态是否为结束状态 这里可以直接调用terminal 函数进行判断
    """
    if terminal(board) == True:
        return None

    sum_x = 0
    sum_o = 0

    for node in board:
        if node == X:
            sum_x += 1
        elif node == O:
            sum_o += 1

    if sum_x > sum_o:
        return X

    if sum_x < sum_o:
        return O

    return None

    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    raise NotImplementedError


# 判断 行 列 对角线 是否存在三点成线
def is_three(node_list, ch):
    sum_ch = 0
    for node in node_list:
        if node == ch:
            sum_ch += 1
    return sum_ch == 3


def winner(board):
    """
    Returns the winner of the game, if there is one.

    分别 当出现 O或X 出现横竖斜 三点成线的情况 即为胜者
    """

    # 进行 行判断
    for i in range(3):
        if is_three(board[i], X):
            return 1
        elif is_three(board[i], O):
            return -1

    # 进行 列判断
    for i in range(3):
        col = [board[0][i], board[1][i], board[2][i]]
        if is_three(col, X):
            return 1
        elif is_three(col, O):
            return -1

    # 进行 斜判断
    dia = []
    for i in range(3):
        dia.append(board[i][i])

    if is_three(dia, X):
        return 1
    elif is_three(dia, O):
        return -1

    b_dia = []

    for i in range(3):
        b_dia.append(board[i][3 - i - 1])

    if is_three(b_dia, X):
        return 1
    elif is_three(b_dia, O):
        return -1

    return 0

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.

    1.棋盘被填满时 游戏已经结束 返回结果
    2.有胜者时 返回结果
    """
    sum_node = 0

    for node in board:
        if node != EMPTY:
            sum_node += 1

    if winner(board) is not None:
        return True

    return False

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
