# 0Search_Notes
    一个实体从给定初始状态和目标状态 返回从初始状态到目标状态的可行解即为搜索问题
- Agent
    能感知环境并做出反应的实体(导航app中的汽车模型)
- State
    状态(位置 排布方式)
- Actions
    function 
    记 state s 为输入 Action(s) 则其的返回值 为一系列s可以执行的action
- Transition Model
    function
    记 state s Action a 为输入 Result(s,a) 则其返回值为s执行a后的新的state
- State Space
    一系列可由初始状态执行一系列操作后所能达到的状态的集合
- Goal Test
    就是看当前节点是否为终点
- Path Cost

## Soling Search Problems
- Solution
    解决方案
    - Optimal Solution
        最优解
    - node 包含:
        - a state
        - parent state
        - action (从parent state 到 当前state的操作)
        - cost(从初始状态到当前状态的cost)
### frontier(可以理解容器吧 可以是stack\queue\priority_queue)

```
Repeat:
    1.If the frontier is empty, 
        Stop. There is no solution to the problem
    2.Remove a node from the frontier. This is the node that will be considered.
    3.If the node contains the goal state,
        Return the solution.Stop.
     Else: 
        Expand the node (find all the new nodes that could be reached from this node), and add resulting nodes to the frontier.
        Add the current node to the explored set.
    frontier为空无解 
    从frontier中取出将要被considered的结点
    consider:
        包含目标状态 返回solution 否则 扩展节点 将当前节点加入explored的集合(就是判重数组)
```

### DFS
    frontier --- stack
- Cons:
    - 不一定是最优解
    - 运气不好的话 开销过大
### BFS
    frontier --- queue
- Cons:
    - 可以找到最优解 但耗时过长

### uninformed search / informed search
- uninformed search: 不考虑问题的结构 总之就是不给出针对性的求解方式 例如 DFS/BFS 在二维 三维空间的求解方式基本是一致的可以套用
- informed search: (启发式搜索 中文好像是这个译名)更加智能 针对问题提出更针对性的解 
- 

### GBFS(Greedy Best-First Search)
    每次扩展 它认为最接近目标节点的点(这与DFS还有BFS是不同 这两个虽然也可以在扩展时加入条件判断 但其实就是向深处和周围扩展)    
    至于 如何知道当前是否最接近目标节点 则需要Heuristic function h(n) (启发函数) 评估当前点到目标的距离
以Brian Yu课堂上的例子则 取h(n)为每个点目标点的曼哈顿距离 GBFS每次进行扩展时 根据h(n)的最优值进行扩展
但GBFS 并不能总是选取最优解 关键原因就是GBFS的只针对当前情况做出最优解

### A* search
    GBFS的问题在于 h(n)指计算当前节点到目标点的曼哈顿距离 但忽视从走到当前节点所需的花费 
    所以 引入g(n) 表示到当前节点花费
    因此A* search 每次扩展节点的策略为 根据h(n)+g(n)的最优解进行选择
    当h(n)所计算的估值是准确的(admissible) 且每个节点为连续时(consistent) 可确保A* search获取的是最优解

## Adversarial Search
    上述的搜索均为只有一个agent情况上的搜索(就是只为一个实体寻找从一个点到另一个点的距离)
    当有多个agent时 则引入一种新概念 Adversarial Search(对抗搜索)

### MiniMax
Max(X) aims to maximize score 
MIN(O) aims to minimize score
将游戏结果以及过程转换计算机所理解的数值的形式 数值增大 以及 数值减小


#### tic-tac-toe game
    以tic-tac-toe(井字棋 两个agent o 和 x) 为例子
    1.数字化(将游戏结果转化为计算机可以理解的语言) -1 0 1 分别表示 o赢 平局 x赢
    2.游戏状态定义
    S0: 在tic-tac-toe中初始状态定义为棋盘
    PLAYERS(s): 用于判现在是谁的回合
    ACTIONS(s): 返回当前状态可以进行的移动
    RESULT(s):  状态转换模型 返回产生移动后的结果   相当于告诉AI 当前游戏的运行规则
    TERMINNAL(s): 类似于goal test 判断此刻状态是否为最终状态    相当于告诉AI游戏 何时结束
    UTILITY(s): 转换最终状态的结果值 判断实际的游戏结果(因为已经将结果数字化为 -1 0 1 所以最后还要再转换一下将其返回)

Given a state x:
- MAX picks action a in ACTION(s) that produces highest value of MIN-VALUE(RESULT(s,a))
- MIN picks action a in ACTION(s)  that produces smallest value of MAX-VALUE(RESULT(s,a))
- 将比分做多者 从当前可以选取的移动中选取可以使得MIN-VALUE值最大的那一步 将比分做少者同理

```
function MAX-VALUE(state):      # 用于获取
    if TERMINAL(state)
        return UTILITY(state)   # 如果游戏已经结束 则直接通过UTILITY函数获取当前状态值
    v = -∞
    for action in Action(state):
    v = MAX(v,MIN-VALUE(RESULT(action,state)))  # 遍历每一种可能的状态 获取可获得的最大值 可以通过剪枝进行优化
    return v
```

### Alpha-Beta Pruning
其实就对搜索过程进行剪枝优化的算法

### Depth-Limited Minimax
对搜索过程的进一步优化 简单来说就是搜索到一定程度就及时回头 不再继续往下搜索

#### evaluation function
评估当前状态的函数 引入评估函数的是 在实际应用中比如井字棋 这过程中需要计算的中间状态是非常多 不可能全部进行 则需要评估函数判断哪些状态更可能赢
(比如在井字棋游戏中 如果状态1表示赢 那么对于游戏过程中的状态存在0.8 0.9 0.99 这些中间状态可以评估哪些状态更可能赢)
而这个评估函数的优秀程度 其实也就相当于AI的优秀程度
评估函数越优秀 则AI在游戏中的表现肯定是越优秀的
