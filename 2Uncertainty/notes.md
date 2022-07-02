# 2Uncertainty_Notes
    主要是概率论的内容然后加上个 贝叶斯网络 和 马尔可夫链(Markov) (后面两个基本上就是在AI中的运用了) 
    还是蛮有意思的这一章的内容 整个内容连贯下来 然后再应用到项目上
## Uncertainty
    在上一章 已经学习了通过AI 表示各种现实世界的Knowledge 然后使用sentence语句 从而对事物做出判断解决实际问题
    然后AI 无法获得完全准确且全面的konwledge 这中间难免会存在一些误差 以及所谓的uncertainty 
    这也是本章节所要解决的问题 因为在实际问题的应用中 我们总希望AI 可以基于现有的konwlegde 达到最优解

## Probability
    通常将可能发生的事件用omega ω表示 
    P(ω) 即该事件所发生的概率
### Axioms in Probability
公理:
- 0<P(ω)<1
- P(ω)=0 不可能事件
- P(ω)=1 必然事件
- ∑ P(ω) = 1 (取遍ω的值)

### Unconditional Probability
    事件发生不依赖之前事件的概率 (如:骰子连续两次6)
## Conditional Probability 
    条件概率 P(a | b)  a在b发生的前提下 发生的概率 (如 在昨天下雨的情况 今天下雨的概率)
    P(a | b) = P(ab) / P(b)

## Random Variables
    随机变量
    简而言之 就是表示P(w)的值
### Independence 
    发生事件之间 互相不影响的性质
    P(ab) = P(a) * P(b)

## Bay's Rule
    P(a | b) = P(ab) / P(b)
    P(b | a) = P(ba) / P(a) => P(ab) = P(ba) = P(b | a)*P(a)
    故有 P(a | b) = P(b | a) * P(a) / P(b) 即 Bay's Rule
    以前做题的时候套公式感觉没啥存在感 其实这个蛮重要的用处蛮多的...
    有的时候某些变量的概率很难算 有些又很容易知道 用这个公式就会很方便

## Joint Probability 
    联合概率
    列表格 展示多个事件发生的可能性
    (其实用处也蛮大)
    可以通过联合概率 来推导出条件概率(因为 P(ab) P(a) P(b)的值均是可以从中获得的)

## Probability Rules
常用概率公式:
- P(a) = 1 - P(!a)
- P(a ∪ b) = P(a) + P(b) - P(ab)
- Marginalization: 联合概率表 扩展一列其值为前几列的加和 其值即为边缘概率 P(X = xi) =  ∑P(X = xi,Y = yj) (取遍j的值)
- Conditioning: P(X = xi) =  ∑P(X = xi | Y = yj) P(Y=yj) (取遍j的值)

## Bayesian Network
    其实就是展示事件之间发生关系(单向关系)的图(当然每件事情的发生是有概率的 事件在前一个事件的基础上发生则又构成条件概率)
基本性质:
- 有向图
- 每个节点代表一个随机变量(即事件)
- X->Y 代表X的发生依赖于B
- 每个节点值 为该节点事件在其父节点事件 所发生的条件概率 P(X | Parents(X))
总的来说在项目中应用一下就基本明白了 课后作业基本提供了封装好的类 实现起来还是难度不大的 

### Inference
    将Bayesian Network 与之前所学 Konwledge章节 的那些数理逻辑的内容结合起来
    就可以通过一些可能发生的事件推理判断出新的信息(之前是必须明确知道的Knowledge 才嫩加入KB中进行推理) 

```markdown
- Query X: the variable for which we want to compute the probability distribution.
  就是随需要求值的随机变量
- Evidence variables E: one or more variables that have been observed for event e. For example, we might have observed that there is light rain, and this observation helps us compute the probability that the train is delayed.
  相当于Knowledge章节中的 Sentence 用于对Query 进行判断
- Hidden variables Y: variables that aren’t the query and also haven’t been observed. For example, standing at the train station, we can observe whether there is rain, but we can’t know if there is maintenance on the track further down the road. Thus, Maintenance would be a hidden variable in this situation.
  简而言之 就是当前未知的变量 但也不是所要求的变量
- The goal: calculate P(X | e). For example, compute the probability distribution of the Train variable (the query) based on the evidence e that we know there is light rain.
  最终所要计算的条件概率 这和Query不一样 最终要计算的目标是在基于之前的事件基础上所发生的可能性
```
### Inference By Enumeration
    这个求解的过程 基本上是 先根据已知的evidence 列出联合概率 然后根据已知的值推导出 hidden variable 这样转换成evidence
    然后重复这个过程 直到获取需要 计算出目标的所有值 从而求得最终解
    P(X  | e) = αP(X,e) = α∑P(X,e,y) (y遍历所有hidden varible的值) (α的意思 就是将计算出来的所有值 按比例调整为最终加和为1)
看起来比较复杂 不过这些都有基本库 提供好了 实际操作起来 调用函数就完事了 