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
## frontier(可以理解容器吧 可以是stack\queue\priority_queue)
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
### DFS
    frontier --- stack
- Cons:
    - 不一定是最优解
    - 运气不好的话 开销过大
### BFS
    frontier --- queue
- Cons:
    - 可以找到最优解 但耗时过长
### GBFS
    
