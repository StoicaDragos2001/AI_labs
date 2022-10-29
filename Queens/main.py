import ast


def read_from_file():
    f = open("block-15-21-570.param", "r")
    text = f.read()
    text_without_spaces = text.replace(" ", "")
    split_text = text_without_spaces.split("=")
    return ((split_text[1].split("\n"))[0]), ((split_text[2].split('\n'))[0])


def satisfies_constraint(state, position):
    line, col = position
    size = len(state[0])
    if line > size - 1 or col > size - 1:
        return "Bad input"
    if (line, col) in state[-1]:
        return "Can't place because of blockage"
    for _ in state[0]:
        if col == _:
            return "Can't place because there is a queen attacking"
    for _ in range(len(state[0])):
        if abs(state[0][_] - col) == abs(_ - line):
            return "Can't place because there is a queen attacking"
    return "Good configuration"


def initialize_state(size, blocks):
    state = []
    possible_positions = []
    visited_queens = []
    for _ in range(size):
        state.append(-1)  # -1 means the queen isn't yet placed
        positions_for_local_queen = []
        for i in range(size):
            if (_, i) not in blocks:
                positions_for_local_queen.append(i)
        possible_positions.append(positions_for_local_queen)
    return state, possible_positions, visited_queens


def mrv(size, possible_positions, visited_queens):
    queen = -1
    option = 999999
    for i in range(0, size):
        if i not in visited_queens:
            if len(possible_positions[i]) < option:
                option = len(possible_positions[i])
                queen = i
    return queen


def show_solution(size, state):
    for row in range(size):
        print(row, end=' ')
        for column in range(size):
            if column != state[row]:
                print('-', end=' ')
            else:
                print('👑', end=' ')
        print('')


def forward_checking(step, size, possible_positions, visited_queens, state):
    if step == size:
        show_solution(size, state)
        exit()
    queen = mrv(size, possible_positions, visited_queens)
    visited_queens.append(queen)
    future_blocked_position = []
    for column in possible_positions[queen]:
        for i in range(size):
            future_blocked_position.append([])
        for new_queen in range(size):
            if new_queen not in visited_queens:
                future_blocked_position = is_attacked(new_queen, column, queen, future_blocked_position,
                                                      possible_positions)
        state[queen] = column
        forward_checking(step + 1, size, possible_positions, visited_queens, state)
        for new_queen in range(size):
            for position in future_blocked_position[new_queen]:
                possible_positions[new_queen].append(position)


def is_attacked(new_queen, column, queen, future_blocked_position, possible_positions):
    x = abs(new_queen - queen)
    if column - x in possible_positions[new_queen]:
        possible_positions[new_queen].remove(column - x)
        future_blocked_position[new_queen].append(column - x)
    if column + x in possible_positions[new_queen]:
        possible_positions[new_queen].remove(column + x)
        future_blocked_position[new_queen].append(column + x)
    if column in possible_positions[new_queen]:
        possible_positions[new_queen].remove(column)
        future_blocked_position[new_queen].append(column)
    return future_blocked_position


if __name__ == '__main__':
    size, blocks = read_from_file()
    blocks = ast.literal_eval(blocks)
    blocks = [tuple(block) for block in blocks]
    blocks = [(item[0] - 1, item[1] - 1) for item in blocks]
    print(blocks)
    size = int(size)
    state, possible_positions, visited_queens = initialize_state(size, blocks)
    print(state, possible_positions)
    forward_checking(0, size, possible_positions, visited_queens, state)
