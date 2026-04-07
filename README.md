# Maze Visualiser

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

A Python project built with Pygame to visualise various maze generation and graph traversal algorithms in real time.

The project is designed to be an interactive learning tool, helping users understand how different algorithms behave by showing their execution step by step.

## Maze Generation Algorithms
### Iterative Backtracker
A depth-first search algorithm that uses a stack to track the current path. It moves randomly between unvisited neighbours and backtracks when there are no surrounding neighbours left to visit. This results in mazes with long winding passages and a low number of branches.

![Backtracker](examples/maze_backtracker.gif)

### Eller's Algorithm
A set-based algorithm that generates one row at a time, only requiring knowledge of the previous row to generate the current row. Vertical and horizontal connections are made with a guarantee that sets are either merged together or survive until the next row, preventing isolations and loops. Passages are generally short, with lots of branches.

![Eller's Algorithm](examples/maze_eller.gif)

### Kruskal's Algorithm
Another set-based algorithm that begins with each cell in a unique set. Walls are randomly removed between cells of different sets, then joining the sets until only one remains. Produces a minimal spanning tree with a variety of passage lengths and number of branches.

![Kruskal's Algorithm](examples/maze_kruskal.gif)

### Prim's Algorithm
An algorithm that grows from the starting cell, removing adjacent walls that are only divided by a single visited cell. Also produces a minimal spanning tree, however passages are generally shorter than mazes generated using Kruskal's algorithm.

![Prim's Algorithm](examples/maze_prim.gif)

### Aldous-Broder Algorithm
A random walk algorithm that moves between cells randomly, carving a passage when an unvisited cell is discovered. This results in a uniform spanning tree, but at the cost of efficiency because cells may be visited many times before the maze is fully generated.

![Aldous-Broder Algorithm](examples/maze_aldous_broder.gif)

### Wilson's Algorithm
This algorithm generates mazes using loop-erased random walks from unvisited cells to the existing maze. It also produces a uniform spanning tree and is more efficient that the Aldous-Broder algorithm, as cells are not revisited unless a loop is created.

![Wilson's Algorithm](examples/maze_wilson.gif)

## Graph Traversal Algorithms:
- A* Pathfinding
- Dijkstra's Algorithm
- Dead-End Filler
- Backtracking Algorithm
- Random Mouse

## Controls
- Select different generation/solving algorithms by clicking the buttons in the options panel
- ↑ / ↓ - Increase / decrease maze height
- ← / → - Increase / decrease maze width
- Click “Speed” button - Cycle through generation speeds

## Getting Started
1. Clone the repository:
   ```bash
   git clone https://github.com/dean-ba/maze-visualiser.git
   cd maze-visualiser
   ```
2. Install dependencies:  
   ```bash
   pip install pygame
   ```
3. Run the project:  
   ```bash
   python main.py
   ```
