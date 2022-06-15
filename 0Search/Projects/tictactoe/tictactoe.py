"""
Tic Tac Toe Player
"""
import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.

    生成初始棋盘 这个没啥修改
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.

    判断当前是谁的回合 初始情况下X 获得先手
    这里我的思路是
    通过当前棋盘上的棋子数目进行判断 X比O 多一个 那么当前就是 O的回合 反之同理
    当然也不要忘了 判断此时棋盘的状态是否为结束状态 这里可以直接调用terminal 函数进行判断

    "In the initial game state, X gets the first move. Subsequently, the player alternates with each additional move."
    这个要求 其实还是有一些 难懂的意思 意思就是 OX 棋子数相同时 那么默认是X先手 然后是O

    """


    sum_x = 0
    sum_o = 0

    row = len(board)
    col = len(board[0])

    for i in range(row):
        for j in range(col):
            if board[i][j] == X:
                sum_x += 1
            elif board[i][j] == O:
                sum_o += 1

    return X if sum_x == sum_o else O

    # raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.

    棋盘只要是空格 就可以走
    """

    move = set()
    row = len(board)
    col = len(board[0])
    for i in range(row):
        for j in range(col):
            if board[i][j] == EMPTY:
                move.add((i, j))

    return move

    # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.

    生成action后 的棋盘
    注意不能浅拷贝 要深拷贝 因为浅拷贝弄出来的是reference 会将之前棋盘改变掉
    """

    (x, y) = action

    if x > 2 or x < 0 or y > 2 or y < 0:
        raise IndexError

    # 深拷贝 棋盘
    newBoard = copy.deepcopy(board)
    # 改变状态

    newBoard[x][y] = player(board)

    return newBoard

    # raise NotImplementedError


def checkRows(board, ch):
    row = len(board)
    col = len(board[0])

    for i in range(row):
        count = 0
        for j in range(col):
            if board[i][j] == ch:
                count += 1
        if count == col:
            return True
    return False


def checkCol(board, ch):
    row = len(board)
    col = len(board[0])
    for i in range(col):
        count = 0
        for j in range(row):
            if board[j][i] == ch:
                count += 1
        if count == row:
            return True
    return False


def checkDiag(board, ch):
    row = len(board)
    col = len(board[0])

    count = 0

    for i in range(row):
        if board[i][i] == ch:
            count += 1

    if count == 3:
        return True

    return False


def checkBdiag(board, ch):
    row = len(board)

    count = 0
    for i in range(row):
        if board[row - i - 1][i] == ch:
            count += 1
    if count == row:
        return True
    return False


def winner(board):
    """
    Returns the winner of the game, if there is one.

    分别 当出现 O或X 出现横竖斜 三点成线的情况 即为胜者
    """
    if checkRows(board, X) or checkCol(board, X) or checkDiag(board, X) or checkBdiag(board, X):
        return X
    elif checkRows(board, O) or checkCol(board, O) or checkDiag(board, O) or checkBdiag(board, O):
        return O
    else:
        return None
    # raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.

    1.棋盘被填满时 游戏已经结束 返回结果
    2.有胜者时 返回结果
    """
    sum_node = 0

    row = len(board)
    col = len(board[0])

    for i in range(row):
        for j in range(col):
            if board[i][j] is not EMPTY:
                sum_node += 1

    # 棋盘被填满游戏结束
    if sum_node == 9 or winner(board) is not None:
        return True
    else:
        return False


    # raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

    # raise NotImplementedError


def max_value(board):
    """
    建议 结合brain 上课讲的那个思路来写
    function MAX-VALUE(state):
    if TERMINAL(state)
        return UTILITY(state)
    v = -∞
    for action in Action(state):
    v = MAX(v,MIN-VALUE(RESULT(action,state)))
    return v
    """

    if terminal(board):
        return utility(board)
    v = float("-inf")

    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v


def min_value(board):
    if terminal(board):
        return utility(board)

    v = float("inf")
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.

    按照brain上课的思路来是最好的 先实现MAX_VALUE MIN_VALUE这两个函数
    然后根据当前回合 进行判断即可 然后返回当前最优解的步数
    先实现 max_value 和 min_value 两个函数 将所有action 对应的数值建立映射
    然后sort 一遍 每一次选择最优解返回即可
    """

    # 如果当前游戏已经结束 返回None
    if terminal(board):
        return None

    elif player(board) == X:
        arr = []
        for action in actions(board):
            # minimax算法中 X 寻找将值变大的一方 X选取对手O 也就是min_value中下一步后结果值的最大值
            arr.append([min_value(result(board, action)), action])
        return sorted(arr, key=lambda x: x[0], reverse=True)[0][1]
    elif player(board) == O:
        arr = []
        for action in actions(board):
            arr.append([max_value(result(board, action)), action])
        return sorted(arr, key=lambda x: x[0])[0][1]

    # raise NotImplementedError
