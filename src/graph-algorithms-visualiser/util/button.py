import pygame

class Button:
    """Class to create rectangular buttons with rounded corners and a border."""

    def __init__(self, rect, text, callback, font, colour, border_colour):
        self.colour = colour
        self.border_colour = border_colour
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.font = font

    def draw(self, surface):
        border_radius = 10
        border_width = 2

        pygame.draw.rect(surface, self.colour, self.rect, border_radius=border_radius)
        pygame.draw.rect(surface, self.border_colour, self.rect, width=border_width, border_radius=border_radius)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        surface.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()
