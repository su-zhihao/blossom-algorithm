"""
Part of the problem statement from the challenge :)

You will set up simultaneous thumb wrestling matches. In each match, two trainers will pair off to thumb wrestle. 
The trainer with fewer bananas will bet all their bananas, and the other trainer will match the bet. 
The winner will receive all of the bet bananas. You don't pair off trainers with the same number of bananas (you will see why, shortly). 
You know enough trainer psychology to know that the one who has more bananas always gets over-confident and loses. 
Once a match begins, the pair of trainers will continue to thumb wrestle and exchange bananas, until both of them have the same number of bananas. 
Once that happens, both of them will lose interest and go back to supervising the bunny workers, and you don't want THAT to happen!

For example, if the two trainers that were paired started with 3 and 5 bananas, 
after the first round of thumb wrestling they will have 6 and 2 (the one with 3 bananas wins and gets 3 bananas from the loser).
After the second round, they will have 4 and 4 (the one with 6 bananas loses 2 bananas). At that point they stop and get back to training bunnies.

How is all this useful to distract the bunny trainers? Notice that if the trainers had started with 1 and 4 bananas, 
then they keep thumb wrestling! 1, 4 -> 2, 3 -> 4, 1 -> 3, 2 -> 1, 4 and so on.

Now your plan is clear. You must pair up the trainers in such a way that the maximum number of trainers go into an infinite thumb wrestling loop!

Write a function solution(banana_list) which, given a list of positive integers depicting the amount of bananas the each trainer starts with, 
returns the fewest possible number of bunny trainers that will be left to watch the workers. 
Element i of the list will be the number of bananas that trainer i (counting from 0) starts with.

The number of trainers will be at least 1 and not more than 100, and the number of bananas each trainer starts with will be a positive integer 
no more than 1073741823 (i.e. 2^30 -1). Some of them stockpile a LOT of bananas.
"""


def gcd(a, b):
    """Compute the greatest common divisor of a and b using Euclidean algorithm."""
    while b:
        a, b = b, a % b
    return a


def reduce_pair(a, b):
    """Reduce the pair (a, b) to its simplest form by dividing both numbers by their GCD."""
    gcd_value = gcd(a, b)
    return a // gcd_value, b // gcd_value


def is_power_of_two(n):
    """Check if n is a power of two by checking if n has exactly one bit set in its binary representation."""
    return n > 0 and (n & (n - 1)) == 0


def check_pair(a, b):
    """Check if the sum of the reduced pair (a, b) is a power of two.

    If it is not, the two trainers will end up in an infinite loop of thumb wrestling.
    How we reach this conclusion?

    WLOG, assume one has x bananas, the other has y with x < y
    first observation: we can reduce the pair into to a simpler form by taking the gcd without affecting the outcome
    For example, 3x and 3y will just follow a similar loop with each pair being 3 times greater than the original one
    second observation: if x + y is odd, then we can never evenly split the bananas, i.e. never reach the equal case
    third observation: if x + y is even, then x and y has the same parity (both even case can be reduced to both odd with 1st observation)

    Now we only have to check when two odd number will not result in an infinite loop
    To reach a conclusion of the pattern, I write down few states with x < y assumption and gcd(x,y)=1 <-- powered by observation1.
    For example, after first match, it will become 2x,y-x and then if 2x<y-x, we have 4x, y-3x; otherwise, we have 3x-y,y+x
    For it to stop, we need 2x=y-x which implies 3x=y, x+y=4x. With some reasoning, we realize x must be 1 or it is not fully "reduced"
    Otherwise if it is coprime then the multiple conditions (like y=3x) will never satisfy
    Writing down a few states with similar reasoning, we noticed that if x+y results in a power of 2, then the loop will terminate
    As the termination condition will be y=3x, y=7x, y=15x ... when solving the equal state
    Note that for cases like 3x-y, y+x; it will never terminate as x=y is the terminate condition which contradicts the assumption
    """
    reduced_a, reduced_b = reduce_pair(a, b)
    return not is_power_of_two(reduced_a + reduced_b)


def host_tournament(banana_list):
    """Construct an undirected graph for the wrestling tournament

    Finding trainers to distract is a maximum matching problem. We can view all the trainers as vertices
    and there is an edge between two trainers if and only if they end up in a neverending thumb wrestling match when pair up
    """
    number_of_trainers = len(banana_list)
    graph = {i: [] for i in range(number_of_trainers)}

    for i in range(number_of_trainers):
        for j in range(i + 1, number_of_trainers):
            if check_pair(banana_list[i], banana_list[j]):
                graph[i].append(j)
                graph[j].append(i)

    return graph


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


def distract_the_trainer(graph):
    """Distract the trainers by figuring out the optimal pairing that maximizes the number of trainers stuck in the infinite loop

    To solve the maximum matching problem, I will attempt to implement the Blossom Algorithm and return the number of distracted pairs
    using helper functions I created above by identifying and contracting the blossoms (odd cycles) within the graph for a maximum matching

    When an augmenting path intersects a blossom, the algorithm locates the base of the blossom using the find_lowest_common_ancestor function.
    It then contracts the blossom into a single vertex through the mark_blossom_path function, simplifying the graph.
    This contraction allows the continuation of the search for augmenting paths in a modified graph where the blossom is treated as a single unit.
    After finding an augmenting path, the algorithm reverses the contraction, expanding the blossoms back to their original form and updating the matching accordingly.
    This process iterates until no augmenting paths are left, ensuring the maximum matching is found. Time Complexity is O(n^3).
    """
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
    # Returns number of undistracted trainers in graph
    return sum(1 for x in match if x == -1)


def solution(banana_list):
    """Find the number of guards that are not distracted"""
    graph = host_tournament(banana_list)
    num_of_undistracted_trainers = distract_the_trainer(graph)
    return num_of_undistracted_trainers
