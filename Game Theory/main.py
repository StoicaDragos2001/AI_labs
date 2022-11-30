import pandas as pd


def read_from_file():
    df = pd.read_csv("game.csv", index_col=0)
    return df.to_dict("dict")


def dominant_strategy(player, dict_for_player):
    if player == 0:
        player += 1
        ok = 0
    elif player == 1:
        player -= 1
        ok = 1
    dict_max_moves_columns = {}
    for i in dict_for_player:
        if i[player] not in dict_max_moves_columns or dict_max_moves_columns[i[player]] < dict_for_player[i]:
            dict_max_moves_columns[i[player]] = dict_for_player[i]
    max_values_for_player = []
    for i in dict_for_player:
        if i[player] in dict_max_moves_columns and dict_for_player[i] == dict_max_moves_columns[i[player]]:
            max_values_for_player.append(i[ok])
    dict_with_counts = {}
    for i in set(max_values_for_player):
        dict_with_counts[i] = max_values_for_player.count(i)
    dominant_value_for_player = [i for i in dict_with_counts if
                                 dict_with_counts[i] == max(list(dict_with_counts.values()))]
    if len(dominant_value_for_player) == 1:
        print(f"Dominant strategy for player {'B' if ok else 'A'} is {dominant_value_for_player}")
    else:
        print("Dominant strategy doesn't exist")


def nash_equilibrum(dict_player_A, dict_player_B):
    dict_max_moves_rows_A = {}
    for i in dict_player_A:
        if i[0] not in dict_max_moves_rows_A or dict_max_moves_rows_A[i[0]] < dict_player_A[i]:
            dict_max_moves_rows_A[i[0]] = dict_player_A[i]
    dict_max_moves_rows_B = {}
    for i in dict_player_B:
        if i[1] not in dict_max_moves_rows_B or dict_max_moves_rows_B[i[1]] < dict_player_B[i]:
            dict_max_moves_rows_B[i[1]] = dict_player_B[i]
    list_max_states_A = []
    for i in dict_player_A:
        if i[0] in dict_max_moves_rows_A and dict_player_A[i] == dict_max_moves_rows_A[i[0]]:
            list_max_states_A.append(i)
    list_max_states_B = []
    for i in dict_player_B:
        if i[1] in dict_max_moves_rows_B and dict_player_B[i] == dict_max_moves_rows_B[i[1]]:
            list_max_states_B.append(i)
    solution = set(list_max_states_A).intersection(set(list_max_states_B))
    if len(solution) == 1:
        print(solution, " represents a Nash equilibrium")
    else:
        print("Nash equilibrium doesn't exist")


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
    dominant_strategy(0, dict_A)
    dominant_strategy(1, dict_B)
    nash_equilibrum(dict_A, dict_B)
    
