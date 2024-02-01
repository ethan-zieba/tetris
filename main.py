import pygame
import random
import constants
import ui_elements
import json

class Block:
    def __init__(self):
        self.lock_sound = pygame.mixer.Sound("assets/sound/lock_effect.mp3")
        self.lock_sound.set_volume(0.3)
        self.color = constants.COLORS[random.choice(list(constants.COLORS))]
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


    def move_down(self):
        self.gridposition[0] += 1

    def move_left(self):
        self.gridposition[1] -= 1

    def move_right(self):
        self.gridposition[1] += 1

    def check_lock(self, grid):
        for coord in self.shape:
            if self.gridposition[0] + coord[0] + 1 >= 20:
                self.lock_sound.play()
                return True
            if grid.grid[self.gridposition[0] + coord[0] + 1][self.gridposition[1] + coord[1]]== 1:
                self.lock_sound.play()
                return True

    def check_horizontal_lock(self, grid):
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

    def draw(self, screen):
        for i in range(self.rows):
            for u in range(self.columns):
                if self.grid[i][u] == 1:
                    pygame.draw.rect(screen, (0, 0, 0),
                                     (u * 30, i * 30 + 30, 30, 30))
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (u * 30 + 1, i * 30 + 30 - 1, 28, 28))

    def add_to_grid(self, block):
        for coord in block.shape:
            self.grid[block.gridposition[0]+coord[0]][block.gridposition[1]+coord[1]] = 1


class Game:
    def __init__(self):
        pygame.init()
        downspeed = 5
        pygame.mixer.music.load("assets/sound/menu_music.mp3")
        pygame.mixer.music.set_volume(0.2)
        self.DOWNEVENT = pygame.USEREVENT+1
        pygame.time.set_timer(self.DOWNEVENT, (10//downspeed)*100)
        self.row_sound = pygame.mixer.Sound("assets/sound/row_sound.mp3")
        self.row_sound.set_volume(0.3)
        self.screen = pygame.display.set_mode((300, 630))
        self.clock = pygame.time.Clock()
        self.running = True
        self.grid = Grid()
        self.block = Block()
        self.score = 0
        self.menu_button = ui_elements.Button((100, 80), (255, 255, 255), "Play", (100, 150), self.start_game)
        self.in_menu = True
        with open("high_score.json", "r") as jsonfile:
            self.highestscore = json.load(jsonfile)["assets/font/highest_score"]
        self.font = pygame.font.SysFont("arial_narrow_7.ttf", 40)
        self.menu_title = self.font.render("TETISSE", True, constants.COLORS["white"])
        self.high_score_title = self.font.render(f"Meilleur score: {self.highestscore}", True, constants.COLORS["white"])
        self.is_game_over = False


    def start_game(self):
        self.in_menu = False
        self.run()

    def menu(self):
        pygame.mixer.music.play()
        while self.in_menu:
            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/images/menu_background.png"), (350, 600)), (0, 0))
            self.screen.blit(self.menu_title, (90, 60))
            self.screen.blit(self.high_score_title, (40, 500))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_score()
                    self.in_menu = False
                if event.type == pygame.MOUSEBUTTONUP:
                    self.menu_button.click()
            self.menu_button.update(self.screen)
            pygame.display.flip()
            self.clock.tick(24)

    def draw_score(self):
        scoretext = self.font.render(str(self.score), True, constants.COLORS["white"])
        self.screen.blit(scoretext, (150, 20))

    def save_score(self):
        if self.score > self.highestscore:
            with open("high_score.json", "w") as jsonfile:
                json.dump({"highest_score": self.score}, jsonfile, indent=3)

    def game_over(self):
        self.menu_title = self.font.render("GAME OVER", True, constants.COLORS["white"])
        self.running = False
        while self.is_game_over:
            pygame.mixer.music.play()
            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/images/menu_background.png"), (350, 600)), (0, 0))
            self.screen.blit(self.menu_title, (90, 60))
            self.screen.blit(self.high_score_title, (40, 500))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_score()
                    self.is_game_over = False
            pygame.display.flip()
            self.clock.tick(24)

    def run(self):
        pygame.mixer.music.load("assets/sound/game_music.mp3")
        pygame.mixer.music.play()
        while self.running:
            self.draw_score()
            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/images/background.png"), (1500, 750)), (0, 0))
            self.draw_score()
            if self.block.check_lock(self.grid):
                self.grid.add_to_grid(self.block)
                self.block.reset()
            game_over = not self.block.check_game_over(self.grid)
            if game_over:
                self.save_score()
                self.is_game_over = True
                self.game_over()
            self.grid.draw(self.screen)
            self.block.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and self.block.check_horizontal_lock(self.grid) != "right":
                        self.block.move_right()
                    if event.key == pygame.K_LEFT and self.block.check_horizontal_lock(self.grid) != "left":
                        self.block.move_left()
                    if event.key == pygame.K_UP:
                        self.block.rotate()
                    if event.key == pygame.K_DOWN:
                        self.block.move_down()
                if event.type == self.DOWNEVENT:
                    self.block.move_down()
                if event.type == pygame.QUIT:
                    self.save_score()
                    self.running = False
            self.remove_full_row()
            pygame.display.flip()
            self.clock.tick(50)

    def remove_full_row(self):
        for i in range(self.grid.rows):
            if self.full_row(i):
                self.row_sound.play()
                self.clear_row(i)
                self.grid.grid.insert(0, self.grid.grid.pop(i))
                self.score += 1

    def clear_row(self, row):
        for column in range(self.grid.columns):
            self.grid.grid[row][column] = 0

    def full_row(self, row):
        for column in range(self.grid.columns):
            if self.grid.grid[row][column] == 0:
                return False
        return True


if __name__ == "__main__":
    game = Game()
    game.menu()