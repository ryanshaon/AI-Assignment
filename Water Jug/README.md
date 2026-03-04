# Uninformed Search: BFS vs DFS on Water Jug Problem

This repo implements:
- BFS (Breadth First Search)
- DFS (Depth First Search)

Example: Water Jug Problem (Milk/Water jug).

## Run
python main.py

## Output
- Solution path (states + actions)
- Steps in solution
- Nodes expanded
- Max frontier size (memory-ish)
- Time taken (ms)

Why this is useful:
- BFS guarantees shortest solution (fewest moves) in unweighted graphs.
- DFS may find a solution faster sometimes but does NOT guarantee shortest, and can go deep unnecessarily.
