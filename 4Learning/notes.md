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
