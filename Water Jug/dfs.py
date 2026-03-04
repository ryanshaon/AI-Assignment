def _reconstruct(parent, action, end_state):
    path = []
    actions = []
    cur = end_state

    while cur is not None:
        path.append(cur)
        actions.append(action.get(cur))
        cur = parent.get(cur)

    path.reverse()
    actions.reverse()


    if actions and actions[0] is None:
        actions = actions[1:]

    return path, actions

def dfs(start, is_goal, neighbors):
    stack = [start]
    parent = {start: None}
    action = {start: None}

    expanded = 0

    while stack:
        s = stack.pop()
        expanded += 1

        if is_goal(s):
            path, actions = _reconstruct(parent, action, s)
            return {
                "found": True,
                "path": path,
                "actions": actions,
                "steps": len(actions),
                "expanded": expanded
            }

        for ns, act in reversed(neighbors(s)):
            if ns not in parent:  # visited check
                parent[ns] = s
                action[ns] = act
                stack.append(ns)

    return {"found": False, "expanded": expanded}
