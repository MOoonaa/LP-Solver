#  Linear Programming Solver

##  Overview
This project implements **Linear Programming (LP) techniques** for solving constrained optimization problems using Python.  
It provides two solving approaches:
- **Graphical Method** → for problems with 2 variables, visualized with plots.  
- **Simplex Method** → for higher-dimensional problems using tableau operations.  

The project also features a **Tkinter-based GUI** where users can input problem data and get solutions both visually and textually.


## Requirements
- Python **3.8+**
- Libraries:
  - `numpy`
  - `matplotlib`
  - `tkinter` (built-in with Python)
  - `Pillow`


## Features
- Handles maximization & minimization problems
- Detects feasibility, unboundedness, and multiple optima
- Provides both textual output and visual plots
- Interactive GUI with dynamic variable/constraint inputs

## Project Structure
project/
│── main.py                 # Entry point to launch the application
│── ui.py                   # GUI (LPSolverApp) – builds tabs for Graphical & Simplex solvers
│── graphical_solver.py     # Solves LP problems using the graphical method
│── simplex_solver.py       # Implements the simplex algorithm
│── report/                 
│    └── Non Linear Optimization Project_Report.docx   # Detailed project report


## How it Works

### 1.main.py

Entry point of the application.

Creates the Tkinter root window and launches the LPSolverApp class from ui.py.

### 2.ui.py

Defines LPSolverApp, which builds the GUI using Tkinter.

Contains two main tabs:

Graphical Solver → calls functions from graphical_solver.py.

Simplex Solver → calls the SimplexSolver class in simplex_solver.py.

Dynamically updates the number of variables/constraints based on user input.

### 3.graphical_solver.py

Implements the Graphical Method for solving LP problems with 2 variables.

Steps:

Plot constraints and feasible region.

Check feasibility, unboundedness, or infeasibility.

Highlight the optimal solution on the graph.

### 4.simplex_solver.py

Implements the Simplex Method using tableau form.

Handles:

Adding slack variables (for ≤ constraints).

Pivot operations, entering/leaving variable selection.

Detecting optimal, infeasible, or unbounded solutions.