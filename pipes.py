# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 21:42:48 2024

@author: Maya
"""
import pandas as pd
from collections import deque

pipe_file = pd.read_csv('C:\\Users\\Maya\\Downloads\\coding_qual_input.txt', sep=' ', names=["type", "x", "y"])

# Identify the coordinates for source (*)
source = pipe_file[pipe_file['type'] == '*'].iloc[0]
source_x = source['x']
source_y = source['y']

# Initialize a set to add visited coordinates
visited = set()
visited.add((source_x, source_y))

# Define directions for movement
directions = {
    '╠': [(-1, 0), (0, 1), (1, 0)],    # Up, Right, Down
    
    '╝': [(-1, 0), (0, -1)],   # Up, Left
    
    '║': [(-1, 0), (1, 0)],    # Up, Down

    '╔': [(1, 0), (0, 1)],      # Down, Right
    
    '╦': [(1, 0), (0, 1), (0, -1)], # Left, Right, Down
    
    '╚': [(-1, 0), (0, 1)], # Up, Right
    
    '═': [(0, -1), (0, 1)],   # Left, Right
    
    '╣': [(0, -1), (1, 0), (-1, 0)],    # Left, Up, Down
    
    '╩': [(-1, 0), (0, 1), (0, -1)],    # Up, Right, Left
    
    '╗': [(1, 0), (0, -1)],   # Down, Left
}

# Function to perform BFS from the water source
def bfs_pipes(source_x, source_y):
    queue = deque([(source_x, source_y)])
    
    while queue:
        x, y = queue.popleft()
        current_pipe = pipe_file.iloc[x]['type']
        possible_directions = directions.get(current_pipe, [])
        
        # Explore every direction
        for dx, dy in possible_directions:
            nx, ny = x + dx, y + dy
            
            # Check if the new position is within bounds
            if 0 <= nx < len(pipe_file) and 0 <= ny < len(pipe_file):
                next_pipe = pipe_file.iloc[nx]['type']
                # Check if the cell has not been visited and is traversable (pipe)
                if (nx, ny) not in visited and next_pipe != ' ':
                    if (-dx, -dy) in directions.get(next_pipe, []):
                        visited.add((nx, ny))
                        queue.append((nx, ny))

# Determine which sinks (letters) are reachable
    reachable_sinks = set()
    for index, row in pipe_file.iterrows():
        if row['type'].isalpha() and (row['x'], row['y']) in visited:
            reachable_sinks.add(row['type'])
            
    result = ''.join(sorted(reachable_sinks))
    return result

sinks_with_water = bfs_pipes(source_x, source_y)

