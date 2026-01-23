"""
Graphs (Part 1): Topological Sort/BFS Patterns
Focus: May 1 - May 14, 2026
"""

from collections import defaultdict, deque

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)
    
    def add_edge(self, u, v):
        """Add directed edge from u to v"""
        pass
    
    def bfs(self, start):
        """Breadth-first search traversal"""
        pass
    
    def dfs(self, start):
        """Depth-first search traversal"""
        pass
    
    def topological_sort(self):
        """Topological sort using DFS (Kahn's Algorithm variant)"""
        pass
    
    def detect_cycle(self):
        """Detect cycle in directed graph"""
        pass

def course_schedule(num_courses, prerequisites):
    """Determine if courses can be completed (topological sort application)"""
    pass

def alien_dictionary(words):
    """Determine order of characters in alien language (topological sort)"""
    pass
