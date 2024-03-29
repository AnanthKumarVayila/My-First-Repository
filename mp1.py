#!/usr/bin/env python
# coding: utf-8

# In[3]:


"""
Name: [Ananth kumar vayila]
Date: [04-02-2024]
Course Name: Artificial Intelligence
Semester: Spring 2024
Assignment Name: MP1: Robot Navigation
"""

import numpy as np
import queue
import heapq

class MazeState:
    """Stores information about each visited state within the search"""
    # Define constants
    SPACE = 0
    WALL = 1
    EXIT = 2
    VISITED = 3
    PATH = 4
    START_MARK = 5
    END_MARK = 6

    MAZE_FILE = 'maze2024.txt'
    maze = np.loadtxt(MAZE_FILE, dtype=np.int32)
    start = tuple(np.array(np.where(maze == 5)).flatten())
    ends = np.where(maze == 2)
    move_num = 0  # Used by show_path() to count moves in the solution path

    def reset_state():
        """Reset the maze state to its initial configuration"""
        MazeState.maze = np.loadtxt(MazeState.MAZE_FILE, dtype=np.int32)
        MazeState.start = tuple(np.array(np.where(MazeState.maze == 5)).flatten())
        MazeState.ends = np.where(MazeState.maze == 2)
        MazeState.move_num = 0

    def __init__(self, conf=start, g=0, pred_state=None, pred_action=None):
        """Initialize the state with information passed from the arguments"""
        self.pos = conf         # Configuration of the state - current coordinates
        self.gcost = g          # Path cost
        self.pred = pred_state  # Predecessor state
        self.action_from_pred = pred_action  # Action from predecessor state to current state

    def __hash__(self):
        """Return a hash code so that it can be stored in a set data structure"""
        return hash(self.pos)

    def is_goal(self):
        """Check if the current position is the exit position"""
        return self.maze[self.pos] == MazeState.EXIT

    def __eq__(self, other):
        """Check for equality of states by positions only"""
        return self.pos == other.pos

    def __lt__(self, other):
        """Allow for ordering the states by the path (g) cost"""
        return self.gcost < other.gcost

    def __str__(self):
        """Return the maze representation of the state"""
        a = np.array(self.maze)
        a[self.start] = MazeState.START_MARK
        a[self.ends] = MazeState.EXIT
        return str(a)

    move_num = 0  # Used by show_path() to count moves in the solution path
    def show_path(self):
        """Recursively output the list of moves and states along the path"""
        if self.pred is not None:
            self.pred.show_path()

        if MazeState.move_num == 0:
            print('START')
        else:
            print(f'Move {MazeState.move_num} ACTION: {self.action_from_pred}')
        MazeState.move_num += 1
        self.maze[self.pos] = MazeState.PATH

    def get_new_pos(self, move):
        """Return a new position from the current position and the specified move"""
        if move == 'up':
            new_pos = (self.pos[0] - 1, self.pos[1])
        elif move == 'down':
            new_pos = (self.pos[0] + 1, self.pos[1])
        elif move == 'left':
            new_pos = (self.pos[0], self.pos[1] - 1)
        elif move == 'right':
            new_pos = (self.pos[0], self.pos[1] + 1)
        else:
            raise ValueError('Wrong direction for checking move')
        return new_pos

    def can_move(self, move):
        """Check if the agent can move in the given direction"""
        new_pos = self.get_new_pos(move)
        if new_pos[0] < 0 or new_pos[0] >= self.maze.shape[0] or new_pos[1] < 0 or new_pos[1] >= self.maze.shape[1]:
            return False
        else:
            return self.maze[new_pos] != MazeState.WALL

    def gen_next_state(self, move):
        """Generate a new MazeState object by taking move from the current state"""
        new_pos = self.get_new_pos(move)
        if self.maze[new_pos] != MazeState.EXIT:
            self.maze[new_pos] = MazeState.VISITED
        return MazeState(new_pos, self.gcost + 1, self, move)


# Display the heading info
print('Artificial Intelligence')
print('MP1: Robot navigation')
print('SEMESTER: Spring 2024')
print('NAME: [Ananth kumar Vayiala]')
print()

print('INITIAL MAZE')

# Load start state onto frontier priority queue
frontier = queue.PriorityQueue()
start_state = MazeState()
frontier.put(start_state)
print(start_state)

# Keep a closed set of states to which optimal path was already found
closed_set = set()

# Expand state (up to 4 moves possible)
possible_moves = ['left', 'right', 'down', 'up']

num_states = 0
while not frontier.empty():
    # Choose state at front of priority queue
    next_state = frontier.get()
    num_states += 1

    # If goal then quit and return path
    if next_state.is_goal():
        next_state.show_path()
        break

    # Add state chosen for expansion to closed_set
    closed_set.add(next_state)

    # Expanding the node
    for move in possible_moves:
        if next_state.can_move(move):
            neighbor = next_state.gen_next_state(move)
            if neighbor in closed_set:
                continue
            if neighbor not in frontier.queue:
                frontier.put(neighbor)
            else:
                if neighbor.gcost < frontier.queue[frontier.queue.index(neighbor)].gcost:
                    frontier.queue[frontier.queue.index(neighbor)] = neighbor
                    heapq.heapify(frontier.queue)

print(start_state)
print('\nNumber of states visited =', num_states)
move_path_length = MazeState.move_num - 1
print('\nLength of shortest path = ', move_path_length)


# In[ ]:




