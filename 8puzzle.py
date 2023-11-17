import random
from queue import PriorityQueue

class Puzzle:
    def __init__(self, size):
        self.size = size
        self.state = self.generate_puzzle()

    def generate_puzzle(self):
        numbers = list(range(1, self.size**2)) + ['_']  # Usamos '_' para representar el espacio en blanco
        random.shuffle(numbers)
        puzzle = [numbers[i:i+self.size] for i in range(0, len(numbers), self.size)]
        return puzzle

    def print_puzzle(self):
        for row in self.state:
            print(row)
        print()

    def is_goal(self):
        goal = list(range(1, self.size**2)) + ['_']
        return self.flatten(self.state) == goal

    def flatten(self, puzzle):
        return [num for row in puzzle for num in row]

    def find_blank(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j] == '_':
                    return i, j

    def get_neighbors(self):
        neighbors = []
        blank_i, blank_j = self.find_blank()

        # Mover el espacio en blanco arriba
        if blank_i > 0:
            neighbor = [row[:] for row in self.state]
            neighbor[blank_i][blank_j], neighbor[blank_i - 1][blank_j] = neighbor[blank_i - 1][blank_j], neighbor[blank_i][blank_j]
            neighbors.append(neighbor)

        # Mover el espacio en blanco abajo
        if blank_i < self.size - 1:
            neighbor = [row[:] for row in self.state]
            neighbor[blank_i][blank_j], neighbor[blank_i + 1][blank_j] = neighbor[blank_i + 1][blank_j], neighbor[blank_i][blank_j]
            neighbors.append(neighbor)

        # Mover el espacio en blanco a la izquierda
        if blank_j > 0:
            neighbor = [row[:] for row in self.state]
            neighbor[blank_i][blank_j], neighbor[blank_i][blank_j - 1] = neighbor[blank_i][blank_j - 1], neighbor[blank_i][blank_j]
            neighbors.append(neighbor)

        # Mover el espacio en blanco a la derecha
        if blank_j < self.size - 1:
            neighbor = [row[:] for row in self.state]
            neighbor[blank_i][blank_j], neighbor[blank_i][blank_j + 1] = neighbor[blank_i][blank_j + 1], neighbor[blank_i][blank_j]
            neighbors.append(neighbor)

        return neighbors

def manhattan_distance(puzzle, goal):
    distance = 0
    for i in range(puzzle.size):
        for j in range(puzzle.size):
            num = puzzle.state[i][j]
            if num != '_':
                goal_i, goal_j = divmod(goal.index(num), puzzle.size)
                distance += abs(i - goal_i) + abs(j - goal_j)
    return distance

def a_star_search(initial_state):
    queue = PriorityQueue()
    puzzle = Puzzle(len(initial_state))
    goal_state = list(range(1, puzzle.size**2)) + ['_']  # Configuración objetivo
    queue.put((0 + manhattan_distance(puzzle, goal_state), id(initial_state), initial_state))

    while not queue.empty():
        _, _, current_state = queue.get()

        puzzle.state = current_state

        if puzzle.is_goal():
            return puzzle

        for neighbor in puzzle.get_neighbors():
            queue.put((len(puzzle.flatten(neighbor)) + manhattan_distance(Puzzle(len(neighbor)), goal_state), id(neighbor), neighbor))

# Crear un puzzle desordenado
initial_puzzle = Puzzle(3)
print("Configuración desordenada:")
initial_puzzle.print_puzzle()

# Resolver el puzzle
solution = a_star_search(initial_puzzle.state)

# Imprimir el puzzle ordenado
print("Configuración ordenada:")
solution.print_puzzle()




