# 1Knowledge_Notes 
    根据现有的知识 推导出相应的结论 在AI中进行应用

# Knowledge
##  Knowledge-Based Agents
    根据一些现有的信息 从而推理出结果的AI对象
## Sentence
    断言 
    A sentence is how AI stores knowledage and uses it to infer new information

# Propositional Logic
    数理逻辑
- Propositional Symbols: 命题符号 P Q R
- Logical Connectives: 逻辑连接符 Not (¬) And (∧) Or (∨) Implication (→) Biconditional (↔) 
- Model: 模型是对每个命题的赋值(就是对当给定PQ是true或false 然后带入对命题进行解释)
- Knowledge Base(KB): 就是AI 已经可以进行判断的所有Knowledge
- Entailment: 蕴含  A entails B 那么A true 则 B 为 true

# Inference
    从旧sentence 中 推导出新的sentence 
    以上名词的学习 最终都是为了在代码中进行应用 通常不需要手动去做什么推到了 有专门的库的

## Model checking Algorithm
    总的来说 就是类似于真值表 枚举所有 P Q的值 然后获取所有的结果
执行Model checking Algorithm 所需要的条件
- KB (要通过KB判断值)
- a query, or the proposition 就是每次进行要判断结果的命题
- Symbols
- Model


## python 中表示 knowledge 和 logic
```pycon
from logic import *

# Create new classes, each having a name, or a symbol, representing each proposition.
rain = Symbol("rain")  # It is raining.
hagrid = Symbol("hagrid")  # Harry visited Hagrid
dumbledore = Symbol("dumbledore")  # Harry visited Dumbledore

# Save sentences into the KB
knowledge = And(  # Starting from the "And" logical connective, becasue each proposition represents knowledge that we know to be true.

    Implication(Not(rain), hagrid),  # ¬(It is raining) → (Harry visited Hagrid)

    Or(hagrid, dumbledore),  # (Harry visited Hagrid) ∨ (Harry visited Dumbledore).

    Not(And(hagrid, dumbledore)),  # ¬(Harry visited Hagrid ∧ Harry visited Dumbledore) i.e. Harry did not visit both Hagrid and Dumbledore.

    dumbledore  # Harry visited Dumbledore. Note that while previous propositions contained multiple symbols with connectors, this is a proposition consisting of one symbol. This means that we take as a fact that, in this KB, Harry visited Dumbledore.
    )
```
总的来说 通常意义上的P Q 就由 Symbol() 进行定义  然后 通过现成的提供的 各种Or Implication Not等库 组成语句 然后存储到KB

## Model Checking Algorithm
```pycon

def check_all(knowledge, query, symbols, model):

    # If model has an assignment for each symbol
    # (The logic below might be a little confusing: we start with a list of symbols. The function is recursive, and every time it calls itself it pops one symbol from the symbols list and generates models from it. Thus, when the symbols list is empty, we know that we finished generating models with every possible truth assignment of symbols.)
    if not symbols:

        # If knowledge base is true in model, then query must also be true
        if knowledge.evaluate(model):
            return query.evaluate(model)
        return True
    else:

        # Choose one of the remaining unused symbols
        remaining = symbols.copy()
        p = remaining.pop()

        # Create a model where the symbol is true
        model_true = model.copy()
        model_true[p] = True

        # Create a model where the symbol is false
        model_false = model.copy()
        model_false[p] = False

        # Ensure entailment holds in both models
        return(check_all(knowledge, query, remaining, model_true) and check_all(knowledge, query, remaining, model_false))

```

# Knowledge Engineering
## Clue 
    就是寻找 谁是凶手的一个游戏 
- People: Mustard Plum Scarlet
- tools: knife revolver wrench 
- location: ballroom kitchen library
然后 游戏过程中会不断给出相关信息 然后我们通过这些信息 谁是凶手 何处通过什么作案工具作案的结论
其实转换到代码上就是
1. 将people tools location 转换为 symbol
2. 将相关语句 通过 库中的 and or not 等组成sentence
3. 然后加入 KB中

## Mastermind game
    就是给一组图案 但是其顺序是打乱的(可能有1-n个顺序是不对的) 然后给出多组 然后推断出原来的顺序

# Inference Rules
    Model Checking的性能不行 需要考虑的情况太多 所以引入Inference Rules 
    这个其实就是sentence 的转换(通常是简化)
- Modus Ponens
- And Elimination
- Double Negation Elimination
- Implication Elimination
- Biconditional Elimination
- De Mogran's Law
- Distribute Property
以上就是几个常用的 推理公式

## Knowledge and Search Problems
    从搜索算法的角度来演示这个推理的过程

```



```



