import pygame.mouse


class Button:
    def __init__(self, size, color, text, position, function):
        self.size = size
        self.color = color
        self.hovercolor = [value - 60 for value in self.color]
        self.text = text
        self.position = position
        self.function = function
        self.font = pygame.font.SysFont("arial_narrow_7.ttf", 30, False)
        self.button_text = self.font.render(text, True, (255, 255, 255) if (color[0]+color[1]+color[2])//3 < 125 else (0, 0, 0))

    def update(self, screen):
        self.is_hovered = self.hovered()
        if self.is_hovered:
            pygame.draw.rect(screen, self.hovercolor, (self.position[0], self.position[1], self.size[0], self.size[1]), border_radius=10)

        else:
            pygame.draw.rect(screen, self.color, (self.position[0], self.position[1], self.size[0], self.size[1]), border_radius=10)
        screen.blit(self.button_text, (self.position[0]+self.size[0]//2-20, self.position[1]+self.size[1]//2-15))


    def hovered(self):
        if (self.position[0] < pygame.mouse.get_pos()[0] < self.position[0]+self.size[0]
            and self.position[1] < pygame.mouse.get_pos()[1] < self.position[1]+self.size[1]):
            return True
        else:
            return False

    def click(self):
        self.function()
