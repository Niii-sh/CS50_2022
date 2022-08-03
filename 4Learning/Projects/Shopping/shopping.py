import csv
import sys
# pandas 是一个用于数据分析的库 读csv数据进行操作的时候会比较方便
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.

    总的来说 这个函数的主要功能就是 载入数据然后对数据进行转化 因为  nearest-neighbor classifier 对数据是有要求的
    evidence : 就是传入的和user相关的所有数据 要根据要求将其转换为相应的类型 int float
    label : int 根据顾客最后有没有购买为 1 或 0 其实就是最后一列Revenue
    所以总的操作也很简单 就是遍历csv 1-16数据根据要求封装到 evidence 里面 17列 封装到label里面 然后返回即可
    """

    # 将用户访问时的月份 转换为数字
    data = pd.read_csv('shopping.csv', header=0)
    d = {
        'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5,
        'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11
    }

    data.Month = data.Month.map(d)

    # 将是否是否返回访问者信息的判断变量 VisitorType 转换为boolean值
    data.VisitorType = data.VisitorType.map(lambda x: 1 if x == 'Returning_Visitor' else 0)

    # 将是否周末访问的变量转换为 boolean值
    data.Weekend = data.Weekend.map(lambda x: 1 if x == True else 0)

    # 将消费者最终是否消费的变量转换为 boolean值
    data.Revenue = data.Revenue.map(lambda x: 1 if x == True else 0)

    # 将需要用 int 和 float 的存储的变量存入 数组 方便后续检查时 进行转换
    # 具体直接去上面的要求中去看即可
    ints = ['Administrative','Informational','ProductRelated','OperatingSystems','Browser','Region','TrafficType',]
    floats = ['Administrative_Duration','Informational_Duration','ProductRelated_Duration','BounceRates','ExitRates',
              'PageValues','SpecialDay']

    for value in ints:
        if data[value].dtype != 'int64':
            data = data.astype({value:'int64'})

    for value in floats:
        if data[value].dtype != 'float64':
            data = data.astype({value : 'float'})

    evidence = data.iloc[:,:-1].values.tolist()
    labels = data.iloc[:,-1].values.tolist()

    return (evidence,labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.

    使用 k-nearest neighbor 算法对模型进行训练
    """

    # 直接调用 sklearn库中的函数 创建 classifier
    model = KNeighborsClassifier(n_neighbors=1)

    # 训练模型
    model.fit(evidence,labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.

    将实际的数据与预测的数据相比较 从而计算出该模型的性能
    sensitivity(正确识别的数据种类所占比例) specificity(错误识别的数据种类所占比例) 两个衡量性能指标
    actual positive 是分类目标且正确识别的
    actual negative 非分类目标但且没有被识别的
    说实话这两个概念有些奇怪 我不知道为啥不直接叫 true positive  true negative
    """

    # 获取 labels 中 actual positives 的数量
    positives = labels.count(1)
    # 获取 labels 中 actual negatives 的数量
    negatives = labels.count(0)


    sens = 0
    spec = 0

    for label , pred in zip(labels,predictions):
        if label == 1:
            if label == pred:
                sens+=1
        else:
            if label == pred:
                spec+=1

    sensitivity = sens / positives
    specificity = spec / negatives

    return  (sensitivity,specificity)

if __name__ == "__main__":
    main()
