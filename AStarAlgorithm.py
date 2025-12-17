from pyamaze import maze, agent, textLabel, COLOR
from queue import PriorityQueue

# Heuristic function: Manhattan distance between two cells.
def h(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)

# A* search algorithm with logging of the search process.
def aStar(m):
    # start = (3,3)  # changed start cell to (3,3) #!!
    start = (m.rows,m.cols)  # changed start cell to (3,3) #!!
    goal = (1, 1)   # goal cell (top-left)

    # Initialize scores for each cell.
    g_score = {cell: float('inf') for cell in m.grid}
    g_score[start] = 0
    f_score = {cell: float('inf') for cell in m.grid}
    f_score[start] = h(start, goal)
    
    open_list = PriorityQueue()
    open_list.put((h(start, goal), h(start, goal), start))
    
    aPath = {}            # For backtracking the final path.
    search_process = []   # List to record the order in which cells are expanded.

    # Main search loop.
    while not open_list.empty():
        currCell = open_list.get()[2]
        search_process.append(currCell)  # Record this cell in the search process.
        
        if currCell == goal:
            break

        # Explore in the order: East, South, North, West.
        for d in 'ESNW':
            if m.maze_map[currCell][d]:
                if d == 'E':
                    childCell = (currCell[0], currCell[1] + 1)
                elif d == 'W':
                    childCell = (currCell[0], currCell[1] - 1)
                elif d == 'N':
                    childCell = (currCell[0] - 1, currCell[1])
                elif d == 'S':
                    childCell = (currCell[0] + 1, currCell[1])
                    
                temp_g_score = g_score[currCell] + 1
                temp_f_score = temp_g_score + h(childCell, goal)
                
                if temp_f_score < f_score[childCell]:
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_f_score
                    open_list.put((temp_f_score, h(childCell, goal), childCell))
                    aPath[childCell] = currCell

    # Reconstruct the final path by backtracking from the goal.
    fwdPath = {}
    cell = goal
    while cell != start:
        fwdPath[aPath[cell]] = cell
        cell = aPath[cell]

    return search_process, aPath, fwdPath

# Create and load the maze.
m = maze(5, 5)
m.CreateMaze(loadMaze='maze.csv')

# Run the A* algorithm and record the search process and final path.
search_process, aPath, fwdPath = aStar(m)

# Create agents:
#   - A red agent to trace the search process. 
#   - A default agent to trace the final path.
# Both agents are now started at (3,3) instead of the default (m.rows, m.cols)
# search_agent = agent(m, 3,3, footprints=True, color=COLOR.red, shape='square', filled=True) #!!
# path_agent   = agent(m, 3,3, footprints=True) #!!
search_agent = agent(m,footprints=True, color=COLOR.red, shape='square', filled=True) #!!
path_agent   = agent(m,footprints=True) #!!

# Trace the search process and final path.
m.tracePath({search_agent: search_process}, delay=100)  # Red agent for search process.
m.tracePath({path_agent: fwdPath}, delay=100)             # Final A* path.

# Add a text label to show the length of the final path.
l = textLabel(m, 'A* Path Length', len(fwdPath) + 1)

# Optionally print the maze map (for debugging).
print("Maze map:")
print(m.maze_map)

# Run the maze visualization.
m.run()
