# Artificial Intelligence

**Course**: Artificial Intelligence
**Institution**: Faculty of Engineering of the University of Porto
**Academic Year**: 2025/2026

## Practical Assignment 1
### Project Overview

This project was developed within the Artificial Intelligence course at FEUP. The goal of the assignment is to design and implement a complete AI-based system capable of solving a search or optimization problem, while allowing performance comparison between different algorithms and strategies.

Our group implemented a solution based on one of the proposed topics, focusing on algorithmic design, performance analysis, and user interaction through a graphical interface.

The system is able to:
- Solve problem instances using different AI algorithms
- Compare algorithm performance
- Read problem instances from text files
- Store detailed results in text files
- Provide a graphical interface for interaction and visualization

The project emphasizes correctness, efficiency, scalability, and clear experimental evaluation.

### Main Objectives

- Implement and compare multiple AI algorithms
- Evaluate solution quality
- Measure execution time and memory usage
- Analyze the number of explored states
- Experiment with different configurations and parameters
- Provide a user-friendly graphical interface

### Features

#### Algorithmic Component

Depending on the selected topic, the system includes implementations of several AI approaches such as:

- Uninformed search strategies
- Heuristic search strategies
- Adversarial search methods
- Metaheuristic optimization techniques

Each algorithm can be configured and evaluated under different conditions.

#### Performance Evaluation

For every execution, the system records:

- Final solution quality
- Number of explored states
- Execution time
- Memory consumption
- Game or optimization metrics depending on the problem

Results are automatically saved to text files for later analysis.

#### Graphical User Interface

The application includes a GUI that allows:

- Visualization of the problem state evolution
- Selection of algorithms and parameters
- Switching between different modes
- Interactive gameplay when applicable
- Requesting hints from the AI system

The interface was designed to make experimentation intuitive and accessible.

### Input and Output

#### Input

- Problem instances are read from structured text files
- Different instance sizes and difficulty levels are supported

#### Output

- Solution details
- Algorithm performance metrics
- Logs of moves or optimization steps
- Final results stored in text files

### Technologies Used

The project was implemented using:

- Python
- Relevant libraries depending on the problem requirements
- File handling for input and output management
- GUI framework for visualization and interaction

### Project Structure

```código
/src
    algorithms/
    gui/
    utils/
    main.py

/instances
/results
```

- algorithms/ contains all implemented AI methods
- gui/ manages the graphical interface
- utils/ includes helper functions
- instances/ stores problem definitions
- results/ stores experimental outputs

### Development Approach

We followed a progressive development strategy:

1. Implement a simplified version of the problem
2. Validate correctness using small instances
3. Add more advanced algorithms
4. Extend to larger and more complex instances
5. Perform systematic performance evaluation
6. This allowed us to ensure reliability before increasing complexity.

### Authors

- Camila de Almeida Correia– Up202304507@up.pt
- Leonor Alexandra Costa Azevedo – Leonor.costa.azevedo@gmail.com (up202304040)
- Maria Nóbrega E Alberich Mota – up202309537@up.pt

## Practical Assignment 2
