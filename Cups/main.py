from collections import deque


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def is_solvable(state):
    if state[2] < state[-1] and state[3] < state[-1]:
        return False
    if state[2] == 0 and state[3] == 0:
        if state[-1] == 0:
            return True
        else:
            return False
    if state[-1] % gcd(state[2], state[3]) == 0:
        return True
    return False


def initialize_state(m, n, b):
    return [0, 0, m, n, b]


def is_final_state(state):
    if state[4] == state[0] or state[4] == state[1]:
        return True
    return False


def validate_transfer(state, from_jug, to_jug):
    if from_jug not in [1, 2]:
        return False
    if to_jug not in [1, 2]:
        return False
    if from_jug == to_jug:
        return False
    if from_jug == 0:
        return False
    if to_jug == 1:
        if to_jug == state[2]:
            return False
    else:
        if to_jug == state[3]:
            return False
    return True


def transfer(state, from_jug, to_jug):
    if validate_transfer(state, from_jug, to_jug):
        virtual_state = state.copy()
        if from_jug == 1:
            to_transfer = min(virtual_state[0], virtual_state[3] - virtual_state[1])
            virtual_state[0] -= to_transfer
            virtual_state[1] += to_transfer
        elif to_jug == 1:
            to_transfer = min(virtual_state[1], virtual_state[2] - virtual_state[0])
            virtual_state[0] += to_transfer
            virtual_state[1] -= to_transfer
        return virtual_state
    return state


def validate_fill(state, to_fill):
    if to_fill not in [1, 2]:
        return False
    if to_fill == 1:
        if state[0] == state[2]:
            return False
    else:
        if state[1] == state[3]:
            return False
    return True


def fill(state, to_fill):
    if validate_fill(state, to_fill):
        virtual_state = state.copy()
        if to_fill == 1:
            to_transfer = virtual_state[2] - virtual_state[0]
            virtual_state[0] += to_transfer
        else:
            to_transfer = virtual_state[3] - virtual_state[1]
            virtual_state[1] += to_transfer
        return virtual_state
    return state


def validate_empty(state, to_empty):
    if to_empty not in [1, 2]:
        return False
    if to_empty == 1:
        if state[0] == 0:
            return False
    else:
        if state[1] == 0:
            return False
    return True


def empty(state, to_empty):
    if validate_empty(state, to_empty):
        virtual_state = state.copy()
        if to_empty == 1:
            virtual_state[0] -= virtual_state[0]
        else:
            virtual_state[1] -= virtual_state[1]
        return virtual_state
    return state


visited = []


def bkt(state):
    if is_final_state(state):
        print(f"-final state={state}")
        return True
    if state not in visited:
        visited.append(state)
        return [bkt(fill(state, 1)), bkt(fill(state, 2)), bkt(empty(state, 1)), bkt(empty(state, 2)), bkt(
            transfer(state, 1, 2)), bkt(transfer(state, 2, 1))]
    else:
        return False


def bfs(state):
    path = []
    queue = deque()
    queue.append(state)
    while len(queue) > 0:
        current = queue.popleft()
        if current not in path:
            if is_final_state(current):
                print(f"-final state={current}")
                break
            path.append(current)
            queue.append(fill(current, 2))
            queue.append(fill(current, 1))
            queue.append(transfer(current, 2, 1))
            queue.append(transfer(current, 1, 2))
            queue.append(empty(current, 2))
            queue.append(empty(current, 1))


def score(state):
    return state[-1] - min(abs(state[-1] - state[0]), abs(state[-1] - state[1]))


def generate_best_neighbour(state):
    solutions = []
    solutions_scores = []
    solutions.append(fill(state, 1))
    solutions.append(fill(state, 2))
    solutions.append(transfer(state, 2, 1))
    solutions.append(transfer(state, 1, 2))
    solutions.append(empty(state, 2))
    solutions.append(empty(state, 1))
    for solution in solutions:
        solutions_scores.append(score(solution))
    best_score = max(solutions_scores)
    for i in range(len(solutions)):
        if solutions_scores[i] == best_score:
            return solutions[i]


def hillclimber(state):
    best = state.copy()
    iteration = 0
    if is_final_state(best):
        return ("-final state: ", best)
    while iteration < 100:
        candidate = generate_best_neighbour(state)
        if score(candidate) > score(best):
            best = candidate.copy()
            if is_final_state(best):
                return ("-final state: ", best)
        iteration += 1
    return ("-plateau state: ", best)


def a_star_search(state):
    open_set = [tuple(state)]
    open_set = set(open_set)
    closed_set = set()
    g = {}
    parents = {}
    g[tuple(state)] = 0
    parents[tuple(state)] = tuple(state)
    while len(open_set) > 0:
        n = None
        for v in open_set:
            if n is None or g[tuple(v)] + score(v) < g[tuple(n)] + score(n):
                n = v
        if is_final_state(n):
            print(f"-final state={n}")
            break
        else:
            for (m, weight) in get_neighbors(list(n)):
                if tuple(m) not in open_set and tuple(m) not in closed_set:
                    open_set.add(tuple(m))
                    parents[tuple(m)] = n
                    g[tuple(m)] = g[n] + weight
                else:
                    if g[tuple(m)] > g[n] + weight:
                        g[tuple(m)] = g[n] + weight
                        parents[tuple(m)] = n
                        if tuple(m) in closed_set:
                            closed_set.remove(m)
                            open_set.add(m)
        open_set.remove(n)
        closed_set.add(n)
    return None


def get_neighbors(current):
    neighbors = []
    neighbor = [fill(current, 2), score(fill(current, 2))]
    neighbors.append(neighbor)
    neighbor = [fill(current, 1), score(fill(current, 1))]
    neighbors.append(neighbor)
    neighbor = [transfer(current, 2, 1), score(transfer(current, 2, 1))]
    neighbors.append(neighbor)
    neighbor = [transfer(current, 1, 2), score(transfer(current, 1, 2))]
    neighbors.append(neighbor)
    neighbor = [empty(current, 2), score(empty(current, 2))]
    neighbors.append(neighbor)
    neighbor = [empty(current, 1), score(empty(current, 1))]
    neighbors.append(neighbor)
    return neighbors


def menu():
    print("\033[1m Welcome to water jug problems! \033[0m")
    jug1 = int(input("Enter capacity of jug 1 : "))
    jug2 = int(input("Enter capacity of jug 2 : "))
    final_liters = int(input("Enter the final number of liters : "))
    initial_state = initialize_state(jug1, jug2, final_liters)
    option = 0
    if is_solvable(initial_state):
        while option != 5:
            print("Press 1 for \033[1;32m BKT Algorithm \033[0m")
            print("Press 2 for \033[1;32m BFS Algorithm \033[0m")
            print("Press 3 for \033[1;32m A* Algorithm \033[0m")
            print("Press 4 for \033[1;32m Hillclimber Algorithm (best neighbour) \033[0m")
            print("Press 5 for \033[1;32m exit \033[0m")
            option = int(input("\033[1m Choose an algorithm: \033[0m"))
            if option == 1:
                bkt(initial_state)
            elif option == 2:
                bfs(initial_state)
            elif option == 3:
                a_star_search(initial_state)
            elif option == 4:
                state_type, result = hillclimber(initial_state)
                print(state_type + str(result))
            elif option == 5:
                exit()
            else:
                print("Incorrect option")
            print("------------------------------------------------------------------")


if __name__ == '__main__':
    menu()
