# blossom-algorithm

The Blossom Algorithm is a fundamental approach to finding maximum matchings in general graphs with a time complexity of $O(n^3)$. It iteratively improves the matching by finding augmenting paths. A unique feature of this algorithm is its handling of blossoms. When an augmenting path encounters a blossom, the algorithm contracts the blossom into a single vertex and continues the search.

This implementation of the Blossom Algorithm includes:

* find_lowest_common_ancestor: Identifies the base of a blossom.
* mark_blossom_path: Marks the vertices involved in a blossom.
* find_augmenting_path: A modified BFS approach to find augmenting paths, handling blossoms dynamically.
* blossom_algorithm_max_matching: The main function that orchestrates the algorithm to find the maximum matching.

References

https://en.wikipedia.org/wiki/Blossom_algorithm
https://www.youtube.com/watch?v=3roPs1Bvg1Q
https://codeforces.com/blog/entry/92339
https://networkx.org/documentation/stable/_modules/networkx/algorithms/matching.html
https://medium.com/@ckildalbrandt/demystifying-edmonds-blossom-algorithm-with-python-code-6353eb043311
