# Architecture

## bfs.py
- Implements BFS using a queue (FIFO).
- Explores level by level.
- Guarantees shortest path in an unweighted state graph.

## dfs.py
- Implements DFS using a stack (LIFO).
- Explores deep first.
- Does NOT guarantee shortest path.

## water_jug.py
- Defines the Water Jug state space:
  - Start state
  - Goal test
  - Neighbor generation (all valid moves)
- Calls BFS and DFS and prints results.
