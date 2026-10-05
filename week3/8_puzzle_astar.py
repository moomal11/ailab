import heapq
import copy

class PuzzleNode:
    def __init__(self, matrix, g_score, h_score, parent=None, move="Start"):
        self.matrix = matrix
        self.g_score = g_score
        self.h_score = h_score
        self.f_score = g_score + h_score
        self.parent = parent
        self.move = move

    def __lt__(self, other):
        return self.f_score < other.f_score

def find_blank(matrix):
    for r in range(3):
        for c in range(3):
            if matrix[r][c] == 0:
                return r, c

def get_misplaced_tiles(matrix, goal_matrix):
    misplaced = 0
    for r in range(3):
        for c in range(3):
            value = matrix[r][c]
            if value != 0 and value != goal_matrix[r][c]:
                misplaced += 1
    return misplaced

def matrix_to_tuple(matrix):
    return tuple(tuple(row) for row in matrix)

def get_neighbors(node, goal_matrix):
    neighbors = []
    r, c = find_blank(node.matrix)

    moves = {
        "Up": (r - 1, c),
        "Down": (r + 1, c),
        "Left": (r, c - 1),
        "Right": (r, c + 1)
    }

    for move_name, (nr, nc) in moves.items():
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_matrix = copy.deepcopy(node.matrix)
            new_matrix[r][c], new_matrix[nr][nc] = new_matrix[nr][nc], new_matrix[r][c]

            h_score = get_misplaced_tiles(new_matrix, goal_matrix)
            neighbor_node = PuzzleNode(
                matrix=new_matrix,
                g_score=node.g_score + 1,
                h_score=h_score,
                parent=node,
                move=move_name
            )
            neighbors.append(neighbor_node)

    return neighbors

def solve_8_puzzle(initial_matrix, goal_matrix):
    start_h = get_misplaced_tiles(initial_matrix, goal_matrix)
    start_node = PuzzleNode(initial_matrix, 0, start_h)

    open_set = []
    counter = 0
    heapq.heappush(open_set, (start_node.f_score, counter, start_node))

    closed_set = set()

    while open_set:
        _, _, current_node = heapq.heappop(open_set)

        if current_node.matrix == goal_matrix:
            path = []
            while current_node:
                path.append(current_node)
                current_node = current_node.parent
            return path[::-1]

        state_tuple = matrix_to_tuple(current_node.matrix)
        if state_tuple in closed_set:
            continue

        closed_set.add(state_tuple)

        for neighbor in get_neighbors(current_node, goal_matrix):
            if matrix_to_tuple(neighbor.matrix) not in closed_set:
                counter += 1
                heapq.heappush(open_set, (neighbor.f_score, counter, neighbor))

    return None

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(str(x) if x != 0 else "_" for x in row))

initial_input = [
    [2, 8, 3],
    [1, 6, 4],
    [7, 0, 5]
]

final_input = [
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5]
]

solution_nodes = solve_8_puzzle(initial_input, final_input)

if solution_nodes:
    print(f"Puzzle solved in {len(solution_nodes) - 1} moves using Misplaced Tiles heuristic!\n")
    print("=" * 30)
    for step, node in enumerate(solution_nodes):
        print(f"Step {step} | Action: {node.move}")
        print(f" -> g(n) = {node.g_score} (Path Cost)")
        print(f" -> h(n) = {node.h_score} (Misplaced Tiles)")
        print(f" -> f(n) = {node.f_score} (Total Evaluation Cost)")
        print("-" * 30)
        print_matrix(node.matrix)
        print("=" * 30)
else:
    print("This specific puzzle state is unsolvable.")
