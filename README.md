# Artificial Intelligence

**Course**: Artificial Intelligence  
**Institution**: Faculty of Engineering of the University of Porto  
**Academic Year**: 2025/2026

## Practical Assignment 1

### Chosen Topic
Topic 1: Heuristic Search Methods for One-Player Solitaire Games

### Chosen Project
Top Spin Puzzle Solver and Player

### Project Overview
This project models and solves the Top Spin solitaire puzzle as a state-space search problem. The board is represented as a circular sequence of numbered tiles, and the main operator reverses a fixed-size segment (default size: 4) starting at a chosen position.

The application supports two modes:
- Human mode: the user plays the puzzle interactively.
- Solver mode: the computer solves puzzle instances using the selected algorithm and configuration.

The objective is to transform the initial board into the ordered sequence (1..N), while collecting performance data for algorithm comparison.

### Main Objectives
- Implement a complete game model (state representation, legal moves, goal test).
- Implement and compare uninformed and informed search algorithms.
- Design and evaluate suitable heuristics for Top Spin.
- Measure quality and computational performance of each approach.
- Support reproducible experiments through text-based instance files and result files.
- Provide a GUI for interactive gameplay, visualization, and solver execution.

### Features

#### Current Implementation Status
- Board representation implemented in `Board` and `GameState` classes.
- Core board operators implemented:
	- Segment reversal (`reverse_segment`).
	- Wheel rotation (`rotate_wheel`).
- Goal test implemented (`is_goal` / ordered board check).
- Hashing and equality for state deduplication implemented (`__hash__`, `__eq__`).
- Parent tracking implemented in search tree nodes (`TreeNode.parent`).
- Search strategy enum extracted to a dedicated module (`search_strategy.py`).

#### Search Algorithms (Implemented)
- BFS
- DFS
- DFS Limited (explicit depth limit)
- Iterative Deepening Search
- Uniform Cost Search
- Greedy Best-First Search
- A* Search
- Weighted A* Search

#### Solver and Game Layer (In Progress)
- `Solver.solve(...)` already supports multiple game modes and search strategies.
- `Game.solve(...)` delegates solving to the solver and syncs game state.
- Heuristics and move-cost functions in `Solver` are still placeholders.
- Some utility methods are still stubs (`undo_move`, `show_solution`, next-best-move logic).

#### Graphical User Interface (Partial)
- Pygame-based scaffold exists.
- Oval Top Spin board rendering exists (`game_graphics.py`).
- Basic input loop exists (keyboard rotation and click action in `player_control.py`).
- Menu and advanced controls/statistics panels are not complete yet.

### Input and Output

#### Input
- Puzzle instance files stored in [project1/instances](project1/instances).
- Typical instance data:
	- Board size N.
	- Segment size K (default 4).
	- Initial tile permutation.
- Instance file format (`.txt`):
```
N K
t1 t2 ... tN
```
Example (`instances/puzzle_8.txt`):
```
8 4
3 1 4 2 7 5 6 8
```
- Solver configuration selected by the user:
	- Search algorithm.
	- Heuristic (when applicable).
	- Optional depth/time limits.

#### Output
- Results stored in [project1/results](project1/results), including:
	- Algorithm and heuristic used.
	- Solved/unsolved status.
	- Solution path (move sequence).
	- Solution depth / move count.
	- States explored.
	- Maximum memory observed.
	- Execution time.
- Runtime feedback through console and/or GUI.

### Technologies Used
- Python 3
- Object-oriented design
- Search and heuristic methods implemented from scratch
- Pygame for GUI prototyping

### Project Structure
- [project1/src/main.py](project1/src/main.py): current app entry point (pygame menu bootstrap).
- [project1/src/game/game.py](project1/src/game/game.py): game controller and solver integration.
- [project1/src/game/solver.py](project1/src/game/solver.py): strategy/mode-aware solve pipeline (work in progress).
- [project1/src/game/game_modes.py](project1/src/game/game_modes.py): gameplay mode enum.
- [project1/src/states/board.py](project1/src/states/board.py): board representation and primitive operations.
- [project1/src/states/game_state.py](project1/src/states/game_state.py): state transitions, equality/hash, move history.
- [project1/src/algorithms/search.py](project1/src/algorithms/search.py): search algorithm implementations.
- [project1/src/algorithms/search_strategy.py](project1/src/algorithms/search_strategy.py): search strategy enum.
- [project1/src/algorithms/tree_node.py](project1/src/algorithms/tree_node.py): tree node with parent/cost/path tracking.
- [project1/src/gui/game_graphics.py](project1/src/gui/game_graphics.py): board rendering on oval track.
- [project1/src/gui/menu.py](project1/src/gui/menu.py): menu scaffold.
- [project1/src/gui/player_control.py](project1/src/gui/player_control.py): basic interactive control loop.
- [project1/src/utils/game_stats.py](project1/src/utils/game_stats.py): runtime statistics container.
- [project1/instances](project1/instances): input puzzle instances.
- [project1/results](project1/results): experiment outputs.

### Development Approach
- Start with small instances and validate correctness first.
- Incrementally implement algorithms:
	- BFS/DFS
	- IDS/UCS
	- Greedy/A*/Weighted A*
- Add heuristics progressively and validate behavior.
- Instrument code early for timing/memory/state metrics.
- Compare algorithms under equivalent conditions and summarize trade-offs.


### Dependencies
- Python 3.10+
- pygame

Install dependencies:

```bash
pip install -r requirements.txt
```

### How to run the game

From repository root:

```bash
python3 project1/app.py
```

Notes:
- The GUI layer is currently a prototype and still under active development.
- Some solver/game helper methods are placeholders and may not expose full gameplay/analysis flows yet.


## Practical Assignment 2
To be defined in the second phase of the course.

### Chosen Topic
TODO

### Chosen Project
TODO

### Project Overview
TODO

### Main Objectives
TODO

### Features

#### Algorithmic Component
TODO

#### Performance Evaluation
TODO

#### Graphical User Interface
TODO

### Input and Output

#### Input
TODO

#### Output
TODO

### Technologies Used
TODO

### Project Structure
TODO

### Development Approach
TODO

### Authors
- Camila de Almeida Correia - Up202304507@up.pt
- Leonor Alexandra Costa Azevedo - Leonor.costa.azevedo@gmail.com (up202304040)
- Maria Nobrega E Alberich Mota - up202309537@up.pt
