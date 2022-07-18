# Learning
# Machine Learning
    机器学习
# Supervised Learning
    supervised Learning is the process of learning with traning label
    label 即表明了数据的一些特性
    总的来说 supervised learning 是在知道正确答案的情况下对AI的一种训练过程
    比如 判断给出的图片中的水果是苹果还是梨子 不断给AI提供图片进行判断 AI初始时会进行随机判断然后 然后每次将判断结果和实际结果进行比对
    然后一些方法不断提高准确性 
classification 就是其中一种 将输入的数据进行分类 
会有一个函数f将输入值 将输入值映射为一个离散值(例如 下雨或不下雨) 我们的要做的就是实现一个函数 可用于测试这个函数f的准确性

## Nearest-Neighbor Classification
    简而言之 就是 对于输入后离散化的数据 根据其在坐标系中最近的点的值 来决定它的值
    (比如说 这个输入 离散化后 在坐标系中距离最近的一个点 为下雨 那么这个点就是下雨)
k-nearest-neighbors classification 作为Nearest-Neighbor Classification的升级版
主要是解决了 Nearest-Neighbor Classification 的缺陷  当一个点最近的是A 但是其他10稍微远一些的点为B 此时按照Nearest-Neighbor Classification 
则会将这个点归为A 但其实是应该是B 更准确些 当然这个方法的关键在于确定k的值、
## Perceptron Learning  
同样的事物 不同的人感知可能是不同的 Perceptron 中文就是感知器的意思 不同对不同事物的感知不同
Perceptron Learning 是着眼于全局的数据  去确立决策的原则
基本思想如下
input {x1 , x2 , x3}
weights {w1 , w2 , w3}
为输入的数据 赋权 
然后设置一个 bias 或者说是 threshold (就是一个函数 用于判断结果)
将所有输入值 与其权值相乘 然后根据给定的函数即可判断出结果
1. hard threshold 的情况下 (和间断函数差不多) 那么所得值就只能是 0 或 1
2. soft threshold 的情况下 (正常单调不减函数 从 0 - 1) 就可以获取 0 1 中间值 判断这个值是更接近0 还是 1

## Support Vector Machines 
    用一组额外的向量组 去确定数据分类时的边界   因为二维空间中 两团不同的数据之间的分界线可以有无数条 但其中是有最优解的
    Maximum Margin Separator : 这种分界方法会与每组数据都保持最大距离 从而新加入变量进行判断时 可以有最为公平的结果

# Regression
    根据现有数据 根据一个h 去尝试估计现有行为f 生成一条线 依据现有的输入预测其输出
## Loss function
    Regression 最重要其实就是 h 即 hypothesis function 因为整条线就是依据这个h生成的
    所以评估h 的性能就非常重要 也就是用到 loss function 去进行评估
loss function 有很多种 比如说 将预测值 与实际值相比较 如果错误 则加入 function 
0-1 Loss Function
可以用于classification 问题中 
```
L(actual, predicted):
    0 if actual = predicted
    1 otherwise
```
总的来说 L 只能返回两个值 true false 即预测值是否正确 适用于一些 只有两种情况(离散)的问题 比如说 今天是否下雨 那么只有结论只有 是与不是
但有时要解决一些连续变量的问题 比如说 实际收益为1000 而预计可能为2000 5000 虽然2000 5000都不是结果 但显然2000 要更符合要求一些 这两个值显然是不同的
```
L₁: L(actual, predicted) = |actual - predicted|
L₂: L(actual, predicted) = (actual - predicted)²
```
L1 返回差值的绝对值 
L2 返回差值的绝对值的平方 相当于将放大了偏差值

## Overfitting
    过度拟合
生成的曲线过度贴合数据 表现loss function很小甚至为0 但是这样的所生成曲线在面对新数据时可能会出现差错

