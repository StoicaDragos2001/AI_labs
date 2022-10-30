import pandas as pd
from collections import Counter

def read_from_file():
    df = pd.read_csv("game.csv", index_col=0)
    return df.to_dict("dict")


if __name__ == '__main__':
    data = read_from_file()
    dict_A = {}
    dict_B = {}
    for key in data.keys():
        for intern_key in data[key]:
            splitting = data[key][intern_key].split('/')
            dict_A[(intern_key, key)] = splitting[0]
            dict_B[(intern_key, key)] = splitting[1]
    print(f"Player A: {dict_A}")
    print(f"Player B: {dict_B}")
    max_values_for_A = [i for i in dict_A if dict_A[i] == max(list(dict_A.values()))]
    counter_max_values_A = dict(Counter(elem[1] for elem in max_values_for_A))
    dominant_strategy_A = [i for i in counter_max_values_A if
                           counter_max_values_A[i] == max(list(counter_max_values_A.values()))]
    print(dominant_strategy_A, " represents a dominant strategy for player A")
    max_values_for_B = [i for i in dict_B if dict_B[i] == max(list(dict_B.values()))]
    counter_max_values_B=dict(Counter(elem[1] for elem in max_values_for_B))
    dominant_strategy_B=[i for i in counter_max_values_B if counter_max_values_B[i] == max(list(counter_max_values_B.values()))]
    print(dominant_strategy_B, " represents a dominant strategy for player B")
    solution = set(max_values_for_A).intersection(set(max_values_for_B))
    if len(solution) > 0:
        print(solution, " represents a Nash equilibrium")
    else:
        print("Nash equilibrium doesn't exist")
