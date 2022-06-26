import copy
import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.

        count 记录的是 为雷 的数量
        所以 如果 cell == count 则恰好证明 该集合内全部为雷
        """

        if len(self.cells) == self.count:
            return set(self.cells)

        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.

        count 为雷的数量 count==0 则代表非雷 即代表安全 返回即可
        """
        if self.count == 0:
            return set(self.cells)

        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.

        将已知 为雷的格子 更新为 雷
        """

        # 如果该格子 在当前的集合中
        if cell in self.cells:
            # 将其从集合中去除 已经是雷了
            self.cells.remove(cell)
            # count = 1 即标记为雷 因为count记录的是集合内雷的数量
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.

        与 mark_mine 同理
        """

        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def neighboring_cells(self, cell):
        """
        额外添加 函数 用于计算 每个格子 周边的格子信息(包括是否已经计算过 是否安全 是否为雷)
        (因为这个操作会大量使用到)
        :param cell:
        :return:
        """
        mines = 0
        i, j = cell
        neighbors = set()
        # 每个 格子的周边 就是一个九宫格 所以 -1 +2
        for row in range(i - 1, i + 2):
            for col in range(j - 1, j + 2):
                # 判断是否越界 判断该点是否已经被计算过(即已经处于 self.moves_made 集合中)
                if ((0 <= col < self.width) and (0 < row < self.height)
                        and ((row, col) != cell) and ((row, col) is not self.moves_made)):
                    if (row, col) in self.mines:
                        mines += 1
                    elif (row, col) in self.safes:
                        continue
                    else:
                        neighbors.add((row, col))

        return neighbors, mines

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # 1
        self.moves_made.add(cell)
        # 2
        self.safes.add(cell)
        # 3
        # 获取当前点周边的点 的信息 (cell and count)
        neighbors = self.neighboring_cells(cell)[0]
        detected_mines = self.neighboring_cells(cell)[1]
        # 更新当前 点 目前仍需计算的mine
        count -= detected_mines
        # 根据 cell 和 count 创建新的sentence
        new_sentence = Sentence(neighbors, count)
        # 将新建的sentence 加入KB
        if new_sentence not in self.knowledge:
            self.knowledge.append(new_sentence)

        # 4
        # 遍历 KB中的 sentence 更新新加入的点的状态
        for sentence in self.knowledge:
            known_safes = sentence.known_safes()
            for known_safe in known_safes:
                self.mark_safe(known_safe)
            known_mines = sentence.known_mines()
            for known_mine in known_mines:
                self.mark_mine(known_mine)

        # 5
        # 这步 就是根据项目分析中方法 通过 集合差的方式 产生新的sentence
        # 新的集合 含有更小范围的cells 以及 相应的mine 数量
        # 中间的步骤主要是判断 集合之间的大小关系
        konwn_sentences = copy.deepcopy(self.knowledge)
        for sentence1 in konwn_sentences:
            konwn_sentences.remove(sentence1)
            for sentence2 in konwn_sentences:
                # 两个集合长度 则无需再缩小范围
                if (len(sentence2.cells)) == (len(sentence1.cells)):
                    continue
                if len(sentence1.cells) != 0 and len(sentence2.cells) != 0:
                    if len(sentence2.cells) < len(sentence1.cells):
                        subset = sentence2.cells
                        bigset = sentence1.cells
                        diff_count = sentence1.count - sentence2.count
                    elif len(sentence1.cells) < len(sentence2.cells):
                        subset = sentence1.cells
                        bigset = sentence2.cells
                        diff_count = sentence2.count - sentence1.count
                    if subset <= bigset:
                        diff_set = bigset - subset
                        # 如果此时新产生的集合只有一个点
                        # 则可直接判断根据 count判断出其状态不需要再向下进行分割
                        if len(diff_set) == 1:
                            if diff_count == 0:
                                new_safe = diff_set.pop()
                                self.mark_safe(new_safe)
                            elif diff_count == 1:
                                new_mine = diff_set.pop()
                                self.mark_mine(new_mine)
                        else:
                            # 否则 将其加入 KB 进行下一步的 分割判断
                            self.knowledge.append(Sentence(diff_set, diff_count))

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        # 打印出当前已知的可移动的 且未移动过的 位置数
        print(f'{len(self.safes - self.moves_made)} knwon unused safes')
        # 打印出当前已经 发现的雷数
        print(f'{len(self.mines)} detected mine:\n{list(self.mines)}')

        # 在可移动的 位置进行遍历 进行移动
        for move in self.safes:
            # 如果当前位置 已经走过则跳过
            if move in self.moves_made:
                continue
            else:
                safe_move = move
                # 加该位置 加入 已经移动的集合中 防止重复移动
                self.moves_made.add(safe_move)
                print(f'Move made {safe_move}')
                return safe_move

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines

        这个主要是用在 没有确定的safe_move 的时候
        即随机产生一个移动位置 当然这也是有前提:
        1. 该位置是没有移动过的
        2、 改位置不能是 已确定为雷的位置
        """

        potential_move = []

        # 这里其实就比较简单了
        # 主要遍历所有点 并且判断 这个点没有走过 且不是雷即可
        for row in range(self.height):
            for col in range(self.width):
                if (row, col) not in self.moves_made and (row, col) not in self.mines:
                    move = (row, col)
                    potential_move.append(move)
        # 没有任何 一个可以移动的位置 则游戏结束
        if len(potential_move) == 0:
            print(f'Game finished!')
        else:
            random_move = random.choice(potential_move)
            # 将该点 标记 防止重复访问
            self.moves_made.add(random_move)
            print(f'Move made {random_move}')
            return random_move
