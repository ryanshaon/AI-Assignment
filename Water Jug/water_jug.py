from bfs import bfs
from dfs import dfs

# -----------------------------
# Water Jug Problem Definition
# -----------------------------

CAP_A = 4
CAP_B = 3
START = (0, 0)
GOAL = 2  # goal amount in either jug

def is_goal(state):
    a, b = state
    return a == GOAL or b == GOAL

def neighbors(state):
    a, b = state
    nxt = []

    # 1) Fill A
    if a < CAP_A:
        nxt.append(((CAP_A, b), "Fill A"))

    # 2) Fill B
    if b < CAP_B:
        nxt.append(((a, CAP_B), "Fill B"))

    # 3) Empty A
    if a > 0:
        nxt.append(((0, b), "Empty A"))

    # 4) Empty B
    if b > 0:
        nxt.append(((a, 0), "Empty B"))

    # 5) Pour A -> B
    if a > 0 and b < CAP_B:
        pour = min(a, CAP_B - b)
        nxt.append(((a - pour, b + pour), f"Pour A->B ({pour})"))

    # 6) Pour B -> A
    if b > 0 and a < CAP_A:
        pour = min(b, CAP_A - a)
        nxt.append(((a + pour, b - pour), f"Pour B->A ({pour})"))

    return nxt

# -----------------------------
# Printing results nicely
# -----------------------------

def show_result(result, name):
    print(f"\n===== {name} =====")

    if not result["found"]:
        print("No solution found.")
        print(f"Nodes expanded: {result['expanded']}")
        return

    print(f"Solution found ✅")
    print(f"Steps: {result['steps']}")
    print(f"Nodes expanded: {result['expanded']}")
    print("\nPath:")

    path = result["path"]
    actions = result["actions"]

    print(f"{path[0]}  (start)")
    for i in range(1, len(path)):
        print(f"{path[i]}  <- {actions[i-1]}")

def main():
    bfs_result = bfs(START, is_goal, neighbors)
    dfs_result = dfs(START, is_goal, neighbors)

    show_result(bfs_result, "BFS")
    show_result(dfs_result, "DFS")

    print("\n===== Comparison =====")
    if bfs_result["found"] and dfs_result["found"]:
        print(f"BFS steps: {bfs_result['steps']} (shortest guaranteed)")
        print(f"DFS steps: {dfs_result['steps']} (not guaranteed shortest)")
    print("BFS explores level-by-level using a queue.")
    print("DFS explores deep first using a stack.")

if __name__ == "__main__":
    main()
