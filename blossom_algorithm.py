def find_lowest_common_ancestor(match, base, parent, vertex_a, vertex_b):
    """Find the lowest common ancestor in the blossom tree."""
    visited = [False] * len(match)
    # Mark the path from vertex_a to the root
    while True:
        vertex_a = base[vertex_a]
        visited[vertex_a] = True
        if match[vertex_a] == -1:
            break  # Reached the root of the tree
        vertex_a = parent[match[vertex_a]]

    # Find the first visited vertex on the path from vertex_b to the root
    while True:
        vertex_b = base[vertex_b]
        if visited[vertex_b]:
            return vertex_b
        vertex_b = parent[match[vertex_b]]


def mark_blossom_path(match, base, blossom_marked, parent, vertex, blossom_base, child):
    """Mark the path from the vertex to the base of the blossom."""
    while base[vertex] != blossom_base:
        blossom_marked[base[vertex]] = blossom_marked[base[match[vertex]]] = True
        parent[vertex] = child
        child = match[vertex]
        vertex = parent[match[vertex]]


def find_augmenting_path(graph, match, parent, root):
    """Find an augmenting path in the graph starting from the root."""
    num_vertices = len(graph)
    used = [False] * num_vertices
    parent[:] = [-1] * num_vertices
    base = list(range(num_vertices))
    used[root] = True
    queue = [root]

    # A modified breadth-first search (BFS) to handle blossoms
    while queue:
        current_vertex = queue.pop(0)
        for neighbor in graph[current_vertex]:
            if (
                base[current_vertex] == base[neighbor]
                or match[current_vertex] == neighbor
            ):
                # If the current_vertex and neighbor are in the same blossom or if they are already matched, the edge is skipped
                continue
            if neighbor == root or (
                match[neighbor] != -1 and parent[match[neighbor]] != -1
            ):
                # If neighbor is either the root or matched with a vertex not yet considered, it could be part of a blossom

                # Find the base of the potential blossom
                cur_base = find_lowest_common_ancestor(
                    match, base, parent, current_vertex, neighbor
                )
                blossom_marked = [False] * num_vertices
                # Mark the path from both current_vertex and neighbor to this base, effectively identifying the blossom
                mark_blossom_path(
                    match,
                    base,
                    blossom_marked,
                    parent,
                    current_vertex,
                    cur_base,
                    neighbor,
                )
                mark_blossom_path(
                    match,
                    base,
                    blossom_marked,
                    parent,
                    neighbor,
                    cur_base,
                    current_vertex,
                )
                # if any vertex is part of the identified blossom, its base is updated to cur_base,
                # and if it hasn't been used already, it's added to the queue
                for i in range(num_vertices):
                    if blossom_marked[base[i]]:
                        base[i] = cur_base
                        if not used[i]:
                            used[i] = True
                            queue.append(i)
            elif parent[neighbor] == -1:
                parent[neighbor] = current_vertex
                if match[neighbor] == -1:
                    return neighbor  # Found an augmenting path.
                neighbor = match[neighbor]
                used[neighbor] = True
                queue.append(neighbor)
    return -1


def blossom_algorithm_max_matching(graph):
    """Implement the Blossom algorithm for maximum matching in a general graph."""
    num_vertices = len(graph)
    match = [-1] * num_vertices
    parent = [0] * num_vertices
    for vertex in range(num_vertices):
        if match[vertex] == -1:
            augmenting_path_vertex = find_augmenting_path(graph, match, parent, vertex)
            while augmenting_path_vertex != -1:
                parent_vertex = parent[augmenting_path_vertex]
                previous_parent_vertex = match[parent_vertex]
                match[augmenting_path_vertex] = parent_vertex
                match[parent_vertex] = augmenting_path_vertex
                augmenting_path_vertex = previous_parent_vertex
    return match
