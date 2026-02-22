import pygame
import sys
from util.button import Button
from util.node_type import NodeType
from generator.backtracker import BacktrackerGenerator
from solver.astar import Astar

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
SETTINGS_PANEL_WIDTH = 200
GRAPH_PANEL_WIDTH = WINDOW_WIDTH - SETTINGS_PANEL_WIDTH
GRAPH_INFO_PANEL_HEIGHT = 200
GRAPH_PANEL_HEIGHT = WINDOW_HEIGHT - GRAPH_INFO_PANEL_HEIGHT

BACKGROUND_COLOUR = (255, 255, 255)
GRAPH_PANEL_COLOUR = (50, 50, 50)
SETTINGS_PANEL_COLOUR = (40, 40, 40)
WHITE = (255, 255, 255)

generation_algorithm = None
solving_algorithm = None
generator = None
generating = False
solver = None
solving = False
graph = None
graph_width = 3
graph_height = 3
cell_size = 0

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Graph Algorithms Visualiser")

font = pygame.font.SysFont("arial", 18)
clock = pygame.time.Clock()

def select_backtracker():
    global generation_algorithm
    generation_algorithm = "Backtracker"
    print("backtracker")

def select_astar():
    global solving_algorithm
    solving_algorithm = "A*"
    print("astar")

def generate():
    global generator, generating, cell_size

    if generation_algorithm == "Backtracker":
        generator = BacktrackerGenerator(graph_height, graph_width)
        cell_size = min(GRAPH_PANEL_WIDTH // (graph_width), GRAPH_PANEL_HEIGHT // (graph_height))
        generating = True
    print("generate")

def solve():
    global solver, solving

    if solving_algorithm == "A*":
        solver = Astar(graph)
        solving = True
    print("solve")

buttons = [
    Button((10, 50, 150, 40), "Backtracker", select_backtracker, font, WHITE),
    Button((10, 130, 150, 40), "A*", select_astar, font, WHITE),
    Button((10, 360, 150, 40), "Generate", generate, font, WHITE),
    Button((10, 410, 150, 40), "Solve", solve, font, WHITE),
]

def draw_settings_panel():
    pygame.draw.rect(screen, SETTINGS_PANEL_COLOUR, (0, 0, SETTINGS_PANEL_WIDTH, WINDOW_HEIGHT))

    screen.blit(font.render("Generation Algorithm",     True, WHITE), (10, 20))
    screen.blit(font.render("Solving Algorithm",        True, WHITE), (10, 100))
    screen.blit(font.render(f"Width: {graph_width}",    True, WHITE), (10, 580))
    screen.blit(font.render(f"Height: {graph_height}",  True, WHITE), (10, 510))

    for button in buttons:
        button.draw(screen)

def handle_change_graph_size(event):
    global graph_height, graph_width

    match event.key:
        case pygame.K_DOWN:
            graph_height -= 2 if graph_height > 3 else 0
        case pygame.K_UP:
            graph_height += 2
        case pygame.K_LEFT:
            graph_width -= 2 if graph_width > 3 else 0
        case pygame.K_RIGHT:
            graph_width += 2
        case _:
            return


def draw_graph_panel():
    global cell_size
    pygame.draw.rect(screen, GRAPH_PANEL_COLOUR, (SETTINGS_PANEL_WIDTH, 0, GRAPH_PANEL_WIDTH, GRAPH_PANEL_HEIGHT))
    
    if graph is None:
        return
    
    rows = len(graph)
    cols = len(graph[0])

    left = ((WINDOW_WIDTH + SETTINGS_PANEL_WIDTH) / 2 - cols * cell_size / 2)
    top = (GRAPH_PANEL_HEIGHT / 2 - rows * cell_size / 2)

    for row in range(rows):
        for col in range(cols):
            match graph[row][col]:
                case NodeType.WALL:
                    colour = (0, 0, 0)
                case NodeType.EMPTY:
                    colour = (255, 255, 255)
                case NodeType.PATH:
                    colour = (255, 0, 0)
                case NodeType.VISITED:
                    colour = (50, 50, 50)
                case _:
                    colour = (255, 255, 255)

            rect = pygame.Rect(
                left + col * cell_size,
                top + row * cell_size,
                cell_size,
                cell_size
            )
            pygame.draw.rect(screen, colour, rect)

def main():
    global generation_algorithm, solving_algorithm, generator, generating, solver, solving, graph
    generation_algorithm = None
    solving_algorithm = None
    generator = None
    generating = False
    solver = None
    solving = False
    graph = None
    running = True

    while running:
        clock.tick(20)
        screen.fill(BACKGROUND_COLOUR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                handle_change_graph_size(event)
            
            for button in buttons:
                button.handle_event(event)

        if generating and generator:
            done = generator.step()
            graph = generator.grid

            if done:
                generating = False
                generator = None
        
        if solving and solver and not generating:
            solvable = solver.step()
            graph = solver.graph
            solved = solver.solved

            if solved or not solvable:
                solving = False

        if solver and solver.path_node != None:
            graph[solver.path_node.pos[0]][solver.path_node.pos[1]] = NodeType.PATH
            solver.path_node = solver.path_node.parent
            if not solver.path_node:
                solver = None
                

        draw_settings_panel()
        draw_graph_panel()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
