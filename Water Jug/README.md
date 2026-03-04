# BFS vs DFS on Water Jug Problem (Uninformed Search)

This project implements two uninformed search strategies:
- BFS (Breadth First Search)
- DFS (Depth First Search)

Problem chosen: Water Jug problem.

## Problem statement (example used here)
You have two jugs:
- Jug A capacity = 4 liters
- Jug B capacity = 3 liters
Start state = (0, 0)
Goal = get exactly 2 liters in either jug.

State representation:
(a, b) where
a = water in Jug A
b = water in Jug B

Allowed actions:
- Fill A
- Fill B
- Empty A
- Empty B
- Pour A -> B
- Pour B -> A

## How to run
Make sure all 3 files are in the same folder:
- bfs.py
- dfs.py
- water_jug.py

Run:
python water_jug.py

## What you will see
For BFS and DFS:
- Whether solution found
- Steps in solution
- Nodes expanded
- Path of states + actions

## Key comparison
- BFS guarantees the shortest solution (minimum number of moves).
- DFS does not guarantee shortest; it may go deep in one direction and find a longer path.
