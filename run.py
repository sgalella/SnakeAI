import pygame
import random


class SnakeCollisionError(Exception):
    def __init__(self):
        super().__init__(f"Snake collided!")


class NoPathError(Exception):
    def __init__(self):
        super().__init__(f"Snake could not find any possible path")


class GameExitedError(Exception):
    def __init__(self):
        super().__init__(f"You exited the game!")


class GridWorld:
    def __init__(self, rows=12, columns=12, color=(128, 128, 128)):
        self.rows = rows
        self.columns = columns
        self.color = color

    def draw(self, screen, width, margin):
        for row in range(self.rows):
            for col in range(self.columns):
                pygame.draw.rect(screen, self.color, ((width + margin) * col + margin, (width + margin) * row + margin, width, width))


class Snake:
    def __init__(self, row=0, column=0, color=(255, 255, 255)):
        self.row = row
        self.column = column
        self.color = color
        self.tail = [(self.row, self.column)]
        self.direction = (0, 0)
        self.path = []

    def draw(self, screen, width, margin):
        for row, column in self.tail:
            pygame.draw.rect(screen, self.color, ((width + margin) * column + margin, (width + margin) * row + margin, width, width))
        for row, column in self.path:
            pygame.draw.rect(screen, (70, 130, 180), ((width + margin) * column + margin, (width + margin) * row + margin, width, width))

    def move(self, grid, food):
        if not self.path:
            self.path = self.get_path(grid, food)
        last_position = self.tail[0]
        self.tail[0] = self.path.pop(-1)
        self.row, self.column = self.tail[0]
        self.direction = self.row - last_position[0], self.column - last_position[1]
        for position in range(1, len(self.tail)):
            self.tail[position], last_position = last_position, self.tail[position]

    def grow(self):
        last_row, last_column = self.tail[-1]
        if len(self.tail) > 1:
            second_last_row, second_last_column = self.tail[-2]
            direction_row, direction_column = (second_last_row - last_row), (second_last_column - last_column)
        else:
            direction_row, direction_column = self.direction
        self.tail.append((last_row - direction_row, last_column - direction_column))

    def generate_path(self, best_path, current_node):
        full_path = [current_node]
        while current_node in best_path.keys():
            current_node = best_path[current_node]
            full_path.append(current_node)
        return full_path[:-1]

    def get_path(self, grid, food, cost=1):
        current_row, current_column = self.tail[0]
        cost = abs(food.row - current_row) + abs(food.column - current_column) + cost
        open_nodes = [((current_row, current_column), cost, self.direction)]
        goal_node = (food.row, food.column)
        closed_nodes = []
        best_path = {}
        while open_nodes:
            current_node, _, current_direction = open_nodes.pop(0)
            if (current_node == goal_node):
                return self.generate_path(best_path, current_node)
            closed_nodes.append(current_node)
            for (next_node, next_direction) in self.get_actions(grid, current_node, current_direction):
                next_row, next_column = next_node
                next_cost = abs(food.row - current_row) + abs(food.column - current_column) + cost
                if self.check_next_node(open_nodes, next_node, next_cost) and next_node not in closed_nodes:
                    best_path[next_node] = current_node
                    open_nodes.append((next_node, next_cost, next_direction))
            open_nodes.sort(key=lambda x: x[1])
        raise NoPathError

    def check_next_node(self, open_nodes, next_state, next_cost):
        costs = any([pair[0] == next_state for pair in open_nodes])
        if costs:
            return False
        return True

    def get_actions(self, grid, current_node, current_direction):
        current_row, current_column = current_node
        possible_actions = []
        if current_direction == (0, -1):  # Left
            actions = [(0, -1), (-1, 0), (1, 0)]
        elif current_direction == (0, 1):  # Right
            actions = [(0, 1), (-1, 0), (1, 0)]
        elif current_direction == (-1, 0):  # Up
            actions = [(0, -1), (0, 1), (-1, 0)]
        elif current_direction == (1, 0):  # Down
            actions = [(0, -1), (0, 1), (1, 0)]
        else:  # Start
            actions = [(0, -1), (0, 1), (1, 0)]
        for action in actions:
            action_row, action_column = action
            next_row = current_row + action_row
            next_column = current_column + action_column
            if (next_row >= 0 and next_row < grid.rows and next_column >= 0 and next_column < grid.rows
                    and (next_row, next_column) not in self.tail):
                possible_actions.append(((next_row, next_column), action))
        return possible_actions


class Food:
    def __init__(self, row=5, column=5, color=(255, 0, 0)):
        self.row = row
        self.column = column
        self.color = color

    def draw(self, screen, width, margin):
        pygame.draw.rect(screen, self.color, ((width + margin) * self.column + margin, (width + margin) * self.row + margin, width, width))

    def reallocate(self, grid, snake):
        self.row = random.randint(0, grid.rows - 1)
        self.column = random.randint(0, grid.columns - 1)
        while (self.row, self.column) in snake.tail:
            self.row = random.randint(0, grid.rows - 1)
            self.column = random.randint(0, grid.columns - 1)


class GameWindow:
    def __init__(self, rows=12, columns=12, width=20, margin=2):
        self.rows = rows
        self.columns = columns
        self.width = width
        self.margin = margin
        self.score = 0
        self.size = ((self.width + self.margin) * self.columns + self.margin, (self.width + self.margin) * self.rows + self.margin)

    def run(self, mode="AI"):
        # Initialize pygame
        self.start()
        pygame.display.set_caption(f"Score: {self.score}")
        self.screen = pygame.display.set_mode(self.size)

        # Create grid
        grid = GridWorld(rows=self.rows, columns=self.columns)
        snake = Snake(row=random.randint(0, grid.rows - 1), column=random.randint(0, grid.columns - 1))
        food = Food(row=random.randint(0, grid.rows - 1), column=random.randint(0, grid.columns - 1))
        while (snake.row == food.row and snake.column == food.column):
            food.reallocate(grid, snake)

        # Run loop
        clock = pygame.time.Clock()
        is_running = True
        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise GameExitedError

            # Move
            snake.move(grid, food)

            # Check collisions
            if (snake.row < 0 or snake.row > grid.rows - 1 or snake.column < 0 or snake.column > grid.columns - 1
                    or (snake.row, snake.column) in snake.tail[2:]):
                raise SnakeCollisionError

            # Eat
            if (snake.row == food.row and snake.column == food.column):
                snake.grow()
                self.score += 1
                pygame.display.set_caption(f"Score: {self.score}")
                if self.score == self.rows * self.columns - 1:
                    break
                else:
                    food.reallocate(grid, snake)

            # Draw
            grid.draw(self.screen, self.width, self.margin)
            snake.draw(self.screen, self.width, self.margin)
            food.draw(self.screen, self.width, self.margin)
            pygame.display.flip()
            clock.tick(10)

    def start(self):
        pygame.init()

    def close(self):
        pygame.quit()


if __name__ == "__main__":
    window = GameWindow(rows=12, columns=12, width=20, margin=2)
    window.run()
