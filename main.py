import pygame
import random
import constants

class Block:
    def __init__(self):
        self.color = constants.COLORS[random.choice(list(constants.COLORS))]
        print(self.color)
        self.gridposition = [0, 5]
        self.shapeindex = random.randint(0, 5)
        self.current_rotation = 0
        self.shape = self.get_shape(self.shapeindex)[self.current_rotation]

    def get_shape(self, index):
        shapes = [
            # L
            [[(0, 0), (1, 0), (2, 0), (2, 1)],
             [(2, 0), (2, 1), (2, 2), (1, 2)],
             [(0, 1), (0, 2), (1, 2), (2, 2)],
             [(0, 0), (1, 0), (0, 1), (0, 2)]],
            # T
            [[(0, 1), (1, 0), (1, 1), (1, 2)],
             [(1, 0), (0, 1), (1, 1), (2, 1)],
             [(1, 0), (2, 1), (1, 1), (1, 2)],
             [(0, 1), (2, 1), (1, 1), (1, 2)]],
            # I
            [[(0, 0), (1, 0), (2, 0), (3, 0)],
             [(2, 0), (2, 1), (2, 2), (2, 3)],
             [(0, 3), (1, 3), (2, 3), (3, 3)],
             [(0, 0), (0, 1), (0, 2), (0, 3)]],
            # O
            [[(0, 0), (0, 1), (1, 0), (1, 1)],
             [(0, 0), (0, 1), (1, 0), (1, 1)],
             [(0, 0), (0, 1), (1, 0), (1, 1)],
             [(0, 0), (0, 1), (1, 0), (1, 1)]],
            # S
            [[(0, 1), (0, 2), (1, 0), (1, 1)],
             [(0, 1), (0, 2), (1, 0), (1, 1)],
             [(0, 1), (0, 2), (1, 0), (1, 1)],
             [(0, 1), (0, 2), (1, 0), (1, 1)]],
            # Z
            [[(0, 0), (0, 1), (1, 1), (1, 2)],
             [(0, 0), (0, 1), (1, 1), (1, 2)],
             [(0, 0), (0, 1), (1, 1), (1, 2)],
             [(0, 0), (0, 1), (1, 1), (1, 2)]]
        ]
        return shapes[index]

    def draw(self, screen):
        for coord in self.shape:
            pygame.draw.rect(screen, (0, 0, 0),
                             ((self.gridposition[1] + coord[1]) * 30, (self.gridposition[0] + coord[0]) * 30 + 30, 30, 30))
            pygame.draw.rect(screen, self.color,
                             ((self.gridposition[1] + coord[1]) * 30 + 1, (self.gridposition[0] + coord[0]) * 30 + 30 + 1, 28, 28))

    def reset(self):
        self.current_rotation = 0
        self.shapeindex = random.randint(0, 5)
        self.color = constants.COLORS[random.choice(list(constants.COLORS))]
        self.shape = self.get_shape(self.shapeindex)[self.current_rotation]
        self.gridposition = [0, 5]

    def rotate(self):
        self.current_rotation = self.current_rotation + 1 if self.current_rotation < 3 else 0
        self.shape = self.get_shape(self.shapeindex)[self.current_rotation]
        print(self.current_rotation)


    def move_down(self):
        self.gridposition[0] += 1

    def move_left(self):
        self.gridposition[1] -= 1

    def move_right(self):
        self.gridposition[1] += 1

    def check_lock(self, grid):
        for coord in self.shape:
            if self.gridposition[0] + coord[0] + 1 >= 20:
                return True
            if grid.grid[self.gridposition[0] + coord[0] + 1][self.gridposition[1] + coord[1]]== 1:
                return True

    def check_horizontal_lock(self, grid):
        print(self.gridposition[1])
        for coord in self.shape:
            if self.gridposition[1] == 0:
                return "left"
            if self.gridposition[1] + coord[1] + 1 == 10:
                return "right"

            if grid.grid[self.gridposition[0]+coord[0]][self.gridposition[1]+coord[1]+1] == 1:
                return "right"
            if grid.grid[self.gridposition[0]+coord[0]][self.gridposition[1]+coord[1]-1] == 1:
                return "left"

    def check_game_over(self, grid):
        if self.gridposition[0] == 0 and self.check_lock(grid):
            return False
        return True

class Grid:
    def __init__(self):
        self.rows = 20
        self.columns = 10
        self.grid = [[0 for i in range(self.columns)] for u in range(self.rows)]
        print(self.grid)

    def draw(self, screen):
        for i in range(self.rows):
            for u in range(self.columns):
                if self.grid[i][u] == 1:
                    pygame.draw.rect(screen, (0, 0, 0),
                                     (u * 30, i * 30 + 30, 30, 30))
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (u * 30 + 1, i * 30 + 30 - 1, 28, 28))
                    print(i, u)

    def add_to_grid(self, block):
        for coord in block.shape:
            self.grid[block.gridposition[0]+coord[0]][block.gridposition[1]+coord[1]] = 1
        print(self.grid)


block = Block()
grid = Grid()
running = True
screen = pygame.display.set_mode((300, 630))
clock = pygame.time.Clock()
while running:
    screen.blit(pygame.transform.scale(pygame.image.load("background.png"), (1500, 750)), (0, 0))
    block.move_down()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and block.check_horizontal_lock(grid) != "right":
        block.move_right()
    if keys[pygame.K_LEFT] and block.check_horizontal_lock(grid) != "left":
        block.move_left()
    if keys[pygame.K_UP]:
        block.rotate()
    if block.check_lock(grid):
        grid.add_to_grid(block)
        block.reset()
    running = block.check_game_over(grid)
    grid.draw(screen)
    block.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick(5)