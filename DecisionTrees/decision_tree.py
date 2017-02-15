from collections import Counter

my_data = [['slashdot', 'USA', 'yes', 18, 'None'],
           ['google', 'France', 'yes', 23, 'Premium'],
           ['digg', 'USA', 'yes', 24, 'Basic'],
           ['kiwitobes', 'France', 'yes', 23, 'Basic'],
           ['google', 'UK', 'no', 21, 'Premium'],
           ['(direct)', 'New Zealand', 'no', 12, 'None'],
           ['(direct)', 'UK', 'no', 21, 'Basic'],
           ['google', 'USA', 'no', 24, 'Premium'],
           ['slashdot', 'France', 'yes', 19, 'None'],
           ['digg', 'USA', 'no', 18, 'None'],
           ['google', 'UK', 'no', 18, 'None'],
           ['kiwitobes', 'UK', 'no', 19, 'None'],
           ['digg', 'New Zealand', 'yes', 12, 'Basic'],
           ['slashdot', 'UK', 'no', 21, 'None'],
           ['google', 'UK', 'yes', 18, 'Basic'],
           ['kiwitobes', 'France', 'yes', 19, 'Basic']]


class DicisionNode:
    """docstring for DicisionNode"""

    def __init__(self, feature_index=-1, feature_value=None, result=None, left_child=None, right_child=None):
        super(DicisionNode, self).__init__()
        self.feature_index = feature_index
        self.feature_value = feature_value
        self.result = result
        self.left_child = left_child
        self.right_child = right_child


def split_data(data, feature, value):
    # 判断特质是不是 str，str 按照分类来处理
    if isinstance(value, str):
        split_func = lambda x: x == value
    else:
        split_func = lambda x: x > value

    set1 = [row for row in data if split_func(row[feature])]
    set2 = [row for row in data if not split_func(row[feature])]
    return set1, set2


def class_counts(data):
    class_ = [row[-1] for row in data]
    return dict(Counter(class_))


def entropy(data):
    from math import log2
    class_results = class_counts(data)
    ent = 0
    for number in class_results.values():
        p = number / len(data)
        ent -= p * log2(p)
    return ent


def gini(data):
    class_results = class_counts(data)
    gini_score = 0
    for number in class_results.values():
        p = number / len(data)
        gini_score += p * (1 - p)
    return gini_score


def build_tree(data, score_func=entropy):
    best_gain = 0
    best_criteria = None
    best_set = None
    current_entropy = score_func(data)

    for col in range(len(data[0]) - 1):
        values = [row[col] for row in data]
        values = Counter(values).keys()
        for value in values:
            set1, set2 = split_data(data, col, value)
            ent1 = score_func(set1)
            ent2 = score_func(set2)
            ent_gain = current_entropy - len(set1) / len(data) * ent1 - len(set2) / len(data) * ent2

            if best_gain < ent_gain and set1 and set2:
                best_gain = ent_gain
                best_set = [set1, set2]
                best_criteria = (col, value)

    if best_gain > 0:
        left_child = build_tree(best_set[0])
        right_child = build_tree(best_set[1])
        return DicisionNode(best_criteria[0], best_criteria[1], None, left_child, right_child)
    else:
        return DicisionNode(result=class_counts(data))


def print_tree(tree, indent=' '):
    if tree.result:
        print(str(tree.result))
    else:
        print('decision col: ', tree.feature_index, ' best split value: ', tree.feature_value)
        print(indent + 'Left child ->', end=' ')
        print_tree(tree.left_child, indent + '    ')
        print(indent + 'Right child ->', end=' ')
        print_tree(tree.right_child, indent + '    ')


# set1, set2 = split_data(my_data, 3, 20)
# print(class_counts(set1), entropy(set1), entropy(set2), entropy(my_data))
print_tree(build_tree(my_data))
