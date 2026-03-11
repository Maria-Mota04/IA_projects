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

#### Algorithmic Component
- State representation through board and game-state abstractions.
- Move operator based on segment reversal.
- Planned algorithm set:
	- Uninformed search: BFS, DFS, Iterative Deepening, Uniform Cost Search.
	- Heuristic search: Greedy, A*, Weighted A*.
- Visited-state control and solution path reconstruction.

#### Performance Evaluation
- For each algorithm and puzzle instance, the project compares:
	- Solution quality (cost, number of moves, solution depth).
	- Number of explored/generated states.
	- Maximum memory usage.
	- Execution time.
- Experiments are intended to cover multiple board sizes and difficulty levels.

#### Graphical User Interface
- Board visualization and interaction controls.
- Manual play controls (human mode).
- Solver controls (algorithm, heuristic, execution).
- Hint support (suggested next move).
- Display of final solution and run statistics.

### Input and Output

#### Input
- Puzzle instance files stored in [project1/instances](project1/instances).
- Typical instance data:
	- Board size N.
	- Segment size K (default 4).
	- Initial tile permutation.
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
- GUI toolkit integration (planned/ongoing)

### Project Structure
- [project1/src/main.py](project1/src/main.py): entry point (scaffolded).
- [project1/src/game/game.py](project1/src/game/game.py): game controller and runtime integration.
- [project1/src/states/board.py](project1/src/states/board.py): board representation and primitive operations.
- [project1/src/states/game_state.py](project1/src/states/game_state.py): state transitions, equality/hash, move history.
- [project1/src/algorithms/search.py](project1/src/algorithms/search.py): search algorithms.
- [project1/src/utils/game_stats.py](project1/src/utils/game_stats.py): statistics and performance metrics.
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

## Practical Assignment 2
To be defined in the second phase of the course.

### Chosen Topic
TBD

### Chosen Project
TBD

### Project Overview
TBD

### Main Objectives
TBD

### Features

#### Algorithmic Component
TBD

#### Performance Evaluation
TBD

#### Graphical User Interface
TBD

### Input and Output

#### Input
TBD

#### Output
TBD

### Technologies Used
TBD

### Project Structure
TBD

### Development Approach
TBD

### Authors
- Camila de Almeida Correia - Up202304507@up.pt
- Leonor Alexandra Costa Azevedo - Leonor.costa.azevedo@gmail.com (up202304040)
- Maria Nobrega E Alberich Mota - up202309537@up.pt
