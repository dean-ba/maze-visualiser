import pygame

# class to create a rectangular button with text that calls a function when clicked
class Button:
    def __init__(self, rect, text, callback, font, colour):
        self.colour = colour
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.font = font

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)
        text_surf = self.font.render(self.text, True, (0,0,0))
        surface.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()