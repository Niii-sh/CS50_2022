# Optimization
    Local Seartch, Linear Promgraming, Constraint satisfaction 三种寻找最优解的方式
    重要的是后面两种 第一种局限性很大 跟AI 也没太大关系
## Local Search
    局部搜索
术语定义:
- Objective Function: 用于求解最大化值的函数
- Cost Function: 用于求解最小化值的函数
- Current State: 当前函数在处理的状态
- Neighbor State:  current state 可以转化过去的状态

### Hill Climbing
```
function Hill-Climb(problem):   
    current = initial state of problem
    repeat:
        neighbor = best valued neighbor of current
        if neighbor not better than current:
            return current
    current = neighbor
```
就是局部寻找最优解 随机选取一个节点开始 寻找这个节点的最优解 然后再以那个最优解的节点再重复寻找 当当前节点周围没有更优解时 则结束算法
有很多局限性 解决方法就是尽可能考虑多的多可能性
#### Hill Climbing Variants
    就是在Hill Climbing的基础 再多考虑几种情况
- Steepest-ascent: 每次都选则值最大的neighbor (这个就是基础情况)
- Stochastic: 随机从附近的更大值选择一个(因为可能一个值是引向局部最高 另外一个是引向全局最高值)
- First-Choice: 只选择第一个较高值
- Random-restart: 多次进行Hill Climbing算法 但每次都选择不同的初始值 最终从多次最终值中选取结果值
- Local Beam Search: 每次进行扩展时选择k个值更大的节点

## Simulated Annealing
    上述Hill Climbing算法所共同存在的缺陷在于都只能找到局部最优解 Simulated Annealing算法就可以用来解决这个问题 
```
function Simulated-Annealing(problem, max):
    current = initial state of problem
    for t = 1 to max:
        T = Temperature(t)                      # Temperature(t)返回在之前迭代过程中更高或更低的值(更接近最优解的值)
        neighbor = random neighbor of current   
        ΔE = how much better neighbor is than current # ΔE代表计算neighbor与当前解相比 更接近最优解的程度
        if ΔE > 0:
            current = neighbor
        with probability e^(ΔE/T) set current = neighbor    
    return current
```

## Linear Programming
    线性规划: 通过线性方程去获取最优解
Linear Programming will have the following components:
- A cost function that we want to minimize: c₁x₁ + c₂x₂ + … + cₙxₙ. Here, each x₋ is a variable and it is associated with some cost c₋.
    目标函数  最终要求解的值
- A constraint that’s represented as a sum of variables that is either less than or equal to a value (a₁x₁ + a₂x₂ + … + aₙxₙ ≤ b) or precisely equal to this value (a₁x₁ + a₂x₂ + … + aₙxₙ = b)
    线性约束条件
- Individual bounds on variables (for example, that a variable can’t be negative) of the form lᵢ ≤ xᵢ ≤ uᵢ.
    每个变量之间的限制关系
实际一些线性规划的算法时候直接调库就行了 比如:Simplex and Interior-Point.(证明涉及到线性代数 和 图形学的内容 不展开)
总的来说 能用库 其实这个复杂的问题实际操作起来就比较简单了

## Constraint Satisfaction
    在限定条件下 为变量赋值
Constraints satisfaction problems have the following properties:
- Set of variables (x₁, x₂, …, xₙ)  
    变量
- Set of domains for each variable {D₁, D₂, …, Dₙ}
    每个变量的值域(或解释为可选值)
- Set of constraints C
    限制条件

补充:
- Hard Constraint: 在最终实现时必须满足的限制条件
- Soft Constraint: 表示更优解的解决方案
- Unary Constraint: 只涉及一个变量的约束
- Binary Constraint: 涉及两个变量的约束

## Node Consistency
    指变量值域中所有变量的约束均满足 unary constraint

## Arc Consistency
    指变量值域中所有变量的约束均满足 binary constraint
可以用下面的revised算法 将不符合arc consietency 两个变量 修改为符合条件的:
```
function Revise(csp, X, Y):
    revised = false
    for x in X.domain:
        if no y in Y.domain satisfies constraint for (X,Y):
            delete x from X.domain
            revised = true
    return revised
```

通过 AC-3 可以将整个问题中 不符合arc-constraint的所有变量转换为符合arc-constraint的
```
function AC-3(csp):
    queue = all arcs in csp
    while queue non-empty:
        (X, Y) = Dequeue(queue)
        if Revise(csp, X, Y):           # 如果revise return true 那么代表已经从X的值域中删除了不符合约束条件的值
            if size of X.domain == 0:   # 如果X的值域为 空 则代表 X 没有符合约束条件的解 整个问题无解返回false
                return false
        for each Z in X.neighbors - {Y}:    # 遍历除了Y以外 所有X周围的变量 入队
            Enqueue(queue, (Z,X))
    return true
```
## Backtracking Search
    宽泛来讲 就是回溯
将 constraint satisfaction 视为一个 search problem 来解决则有:
- Initial state: empty assignment (all variables don’t have any values assigned to them).
    初始状态: 空集 即不给变量赋值
- Actions: add a {variable = value} to assignment; that is, give some variable a value.
- Transition model: shows how adding the assignment changes the assignment. 
There is not much depth to this: the transition model returns the state that includes the assignment following the latest action.
    Transition model: 在解决constraint satisfaction的问题中 transition model返回的应该是最近的action执行后的状态
- Goal test: check if all variables are assigned a value and all constraints are satisfied.
    检查每个变量是否已被赋值 以及是否满足约束条件
- Path cost function: all paths have the same cost. As we mentioned earlier, 
as opposed to typical search problems, optimization problems care about the solution and not the route to the solution.
    所有路径的cost相同 constraint satisfaction问题只关心结果 不关注获得结果的过程消耗

```
function Backtrack(assignment, csp): 
    if assignment complete:
        return assignment
    var = Select-Unassigned-Var(assignment, csp)
    for value in Domain-Values(var, assignment, csp):
        if value consistent with assignment:
            add {var = value} to assignment
            result = Backtrack(assignment, csp)
            if result ≠ failure:
                return result
            remove {var = value} from assignment
    return failure
   
```
### Inference
    对于backtracking 算法进一步改进
核心思想始终维护 arc-consistency 即 Maintaining Arc-Consistency algorithm
即在backtracking 每次进行赋值的时候都会调用 AC-3 algorithm 来维护 arc-consistency 
从而可以减少后续无效的赋值尝试(因为在backtracking search中很有可能你赋的那个值是完全无效的 即在后续过程违背了arc-consistency)
```
function Backtrack(assignment, csp):
    if assignment complete:     # 如果赋值已经完成 则直接返回 
        return assignment
    var = Select-Unassigned-Var(assignment, csp)
    for value in Domain-Values(var, assignment, csp):
        if value consistent with assignment:
            add {var = value} to assignment                 # 优化就在这两段
            inferences = Inference(assignment, csp)         # 将合法值加入后 通过Inference(...) 即调用AC-3去维护了加入新值后的arc-consistency 
            if inferences ≠ failure:
                add inferences to assignment
            result = Backtrack(assignment, csp)
            if result ≠ failure:
                return result
        remove {var = value} and inferences from assignment
    return failure
```
#### Minimum Remaining Values (MRV) 
    在以上基础还可以进一步优化 上面的算法在选择变量进行赋值这一步是完全随机 但可以通过启发函数的方式 优化这个选择 从而进一步提高效率
    这个函数就是MRV
总的来说 就是两点:
1. 未确定的变量中 优先选取可选择值域范围最小的
2. 如果未确定的变量中 每个变量的值域均相同 则有优先选择弧(arc) 最多的那个变量

#### Least Constraining Values
    也是一种启发函数
总的来说就是 在对未确定变量赋值时 尽量选取对其他未确定变量影响小的值






