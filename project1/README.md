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

#### Search Algorithms
- BFS
- DFS
- DFS Limited (explicit depth limit)
- Iterative Deepening Search
- Uniform Cost Search
- Greedy Best-First Search
- A* Search
- Weighted A* Search

#### Graphical User Interface
- The ``Read from file`` option allows the user to input the name of the file with the board values. The board is loaded when pressing the ``Confirm`` button or the enter button on the keyboard. Afterwards, the user can choose to solve this instance with one of the algorithms or solve it themselves. After using that board for one of the tasks, it is shuffled, so to use it again there is a need to choose the ``Read from file`` option once again.
- The ``Difficulty`` option allows the user to choose the difficulty of the board that will be generated.
- The ``Leaderboard`` option shows the local leaderboard (ordered first by number of moves, then by time).
- The ``Algorithms`` option allows the user to choose one of the algorithms to solve a board. Unless the board was chosen with ``Read from file``, it will be randomized. After choosing the algorithm, the user can personalize some of its values. After loading, the user is presented with the statistics of the algorithm and can choose to watch a play by play of the solution. The user can alter the playback speed (slow, normal or fast) and can rewatch it however many times they want.
- The ``Play`` option shows the board and allows the player to directly interact with it.
	- The ``?`` button shows the commands (left and right arrow to rotate the pieces, click the purple circle to rotate it).
	- The ``Undo`` button undoes the last (and only the last) movement done.
	- The ``Hint Settings`` button allows customization of the algorithm used to calculate the next hints (which of the algorithms, heuristics, cost, etc.)
	- The ``Hint`` button highlights in red the set of pieces the user should rotate next, according to the algorithm chosen.
- The ``Win`` screen (encountered after winning a game through the ``Play`` option) allows the user to check this game's statistics, as well as the leaderboard.
- The ``Lose`` screen (encountered after pressing the ``Quit`` button in the ``Play`` state) lets the user retry the game (the board is reset and the user is taken back the the ``Play`` state) or go back to the main menu (a new board is generated).
- All menus (except for the main one) have ``Back`` buttons (or some variable) that allows the user to go back to the previous screen.

### Input and Output Files

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
- Input files must be put in the ``instances`` folder and contain only letters, numbers and _.


### Authors
- Camila de Almeida Correia - up202304507@up.pt
- Leonor Alexandra Costa Azevedo - up202304040@up.py
- Maria Nobrega E Alberich Mota - up202309537@up.pt
