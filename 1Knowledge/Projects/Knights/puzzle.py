from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# 基本上 仿照clue 那个例子就可以写出来
# 最关键 是要写出基础的 game condition
# 1.任何一个角色只可能是 Knight 或者 Knave
# ((A is Knight) or (A is Knave)) and not((A is Knight) and (A is Knave))
# 这个 画个真值表 就可以了理解 其实就是 （P | Q) & !(P & Q) 只有当 P Q 其中一个为true时候 整个式子的值为true
# 2. Knight 说的话一定是对的
# 3. Knave 所说一定为谎言

# Puzzle 0
# A says "I am both a knight and a knave."
sentence0_A = And(AKnight, AKnave)
knowledge0 = And(
    # TODO
    # 写出 初始情况的KB
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # 根据A 所提供的信息写出表达式
    # 如果 A Knight 那么 则A 所说的就一定是对的
    Implication(AKnight, sentence0_A)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
sentence1_A = And(AKnave, BKnave)
knowledge1 = And(
    # TODO
    # 写出初始情况的KB
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),

    # 根据A 提供的信息 写出条件
    # 如果A 为 Knave 那么A 所说的一定为谎言
    Implication(AKnave, Not(sentence1_A)),

    # 如果A 为 Knight 那么A 所说一定是对的
    Implication(AKnight, sentence1_A)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
sentence2_A = Or(And(AKnight, BKnight), And(AKnave, BKnave))
sentence2_B = Or(And(AKnight, BKnave), And(AKnave, BKnight))
knowledge2 = And(
    # TODO
    # 先写出 基础的KB
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),

    # 根据A 提供的信息 写出条件
    Implication(AKnight, sentence2_A),
    Implication(AKnave, Not(sentence2_A)),

    # 根据B 提供的信息 写出条件
    Implication(BKnight, sentence2_B),
    Implication(BKnave, Not(sentence2_B))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

# 注意这里 A says 这边 其实是有些坑的 是A 说了 他要么是Knight 或者 是knave 这和says nothing是不一样的
# 这里还可以再推一步 那就是无论如何 A所说都一定是 I am a knight 因为如果A 说的是 I am a knave 那这就矛盾了
sentence3_A = And(Implication(AKnight, AKnight), Implication(AKnave, Not(AKnight)))
# 这里 B says A says 不等于 B says A
sentence3_B = And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)), CKnave)
sentence3_C = AKnight
knowledge3 = And(
    # TODO
    # 先写出 基础KB
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),

    Implication(AKnight,sentence3_A),
    Implication(AKnave,Not(sentence3_A)),

    Implication(BKnight,sentence3_B),
    Implication(BKnave,Not(sentence3_B)),

    Implication(CKnight,sentence3_C),
    Implication(CKnave,Not(sentence3_C))

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
