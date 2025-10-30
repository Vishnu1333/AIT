def aStarAlgo(start_node, stop_node):
    open_set = set([start_node])
    closed_set = set()
    g = {}  # store distance from starting node
    parents = {}  # parents contain an adjacency map of all nodes

    # distance of starting node from itself is zero
    g[start_node] = 0
    # start_node is the root node, so it has no parent nodes
    # so start_node is set to its own parent node
    parents[start_node] = start_node

    n = None # Initialize n outside the loop
    
    while len(open_set) > 0:
        n = None
        # node with the lowest f() is found
        for v in open_set:
            if n is None or g[v] + heuristic(v) < g[n] + heuristic(n):
                n = v

        # *** CORRECTION 4: Simplified loop break condition ***
        if n == stop_node:
            break

        # This for loop is now safe because of Correction 3
        for m, weight in get_neighbors(n):
            # nodes 'm' not in open_set and closed_set are added to open_set
            # n is set as its parent
            if m not in open_set and m not in closed_set:
                open_set.add(m)
                parents[m] = n
                g[m] = g[n] + weight
            # for each node m, compare its distance from start i.e g(m)
            # to the from start through n node
            else:
                if g[m] > g[n] + weight:
                    # update g(m)
                    g[m] = g[n] + weight
                    # change parent of m to n
                    parents[m] = n
                    # if m is in closed_set, remove and add to open_set
                    if m in closed_set:
                        closed_set.remove(m)
                        open_set.add(m)

        # remove n from the open_set and add it to closed_set
        # because all of its neighbors were inspected
        open_set.remove(n)
        closed_set.add(n)

    # *** CORRECTION 5: Corrected post-loop failure check ***
    if n != stop_node:
        print('Path does not exist!')
        return None

    # if the current node is the stop_node,
    # then we begin reconstructing the path from it to the start_node
    if n == stop_node:
        path = []
        while parents[n] != n:
            path.append(n)
            n = parents[n]
        path.append(start_node)
        path.reverse()
        print('Path found:', path)
        return path

    print('Path does not exist!')
    return None

# define function to return neighbors and their distances from the passed node
def get_neighbors(v):
    if v in Graph_nodes:
        return Graph_nodes[v]
    else:
        # *** CORRECTION 3: Return an empty list, not None ***
        return []

# for simplicity, we'll consider heuristic distances given
# and this function returns heuristic distance for all nodes
def heuristic(n):
    h_dist = {
        'A': 11,
        'B': 6,
        'C': 99,
        'D': 1,
        'E': 7,
        'G': 0
    }
    # *** CORRECTION 2: Use .get() for safety ***
    # Return infinity if node not in heuristic map
    return h_dist.get(n, float('inf'))

# Describe your graph here
Graph_nodes = {
    'A': [('B', 2), ('E', 3)],
    'B': [('A', 2), ('C', 1), ('G', 9)],
    'C': [('B', 1)],
    'D': [('E', 6), ('G', 1)],
    'E': [('A', 3), ('D', 6)],
    'G': [('B', 9), ('D', 1)]
}

print("Following is the A* Algorithm:")
# *** CORRECTION 1: Removed the invalid text ***
aStarAlgo('A', 'G')