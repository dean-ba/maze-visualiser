import pygame
import sys

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
SETTINGS_PANEL_WIDTH = 200
GRAPH_PANEL_WIDTH = WINDOW_WIDTH - SETTINGS_PANEL_WIDTH

BACKGROUND_COLOUR = (255, 255, 255)
GRAPH_PANEL_COLOUR = (50, 50, 50)
SETTINGS_PANEL_COLOUR = (40, 80, 160)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Graph Algorithms Visualiser")

font = pygame.font.SysFont("arial", 18)
clock = pygame.time.Clock()

def draw_settings_panel():
    pygame.draw.rect(screen, SETTINGS_PANEL_COLOUR, (0, 0, SETTINGS_PANEL_WIDTH, WINDOW_HEIGHT))

    screen.blit(font.render("Generation Algorithm", True, WHITE), (10, 20))
    screen.blit(font.render("Solving Algorithm",    True, WHITE), (10, 50))
    screen.blit(font.render("Width:",               True, WHITE), (10, 80))
    screen.blit(font.render("Height:",              True, WHITE), (10, 110))

def draw_graph_panel():
    pygame.draw.rect(screen, GRAPH_PANEL_COLOUR, (SETTINGS_PANEL_WIDTH, 0, GRAPH_PANEL_WIDTH, WINDOW_HEIGHT))

def main():
    running = True

    while running:
        clock.tick(60)
        screen.fill(BACKGROUND_COLOUR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_settings_panel()
        draw_graph_panel()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
