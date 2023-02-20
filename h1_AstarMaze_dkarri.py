from pyamaze import maze,agent,textLabel
from queue import PriorityQueue

# Creating heuristic function using manhatten distance
def h(node_1,node_2): #node_1 and node_2 are two blocks at manhatten distance h
    x1,y1 = node_1
    x2,y2 = node_2

    return abs(x1-x2) + abs(y1-y2)

def A_Star(m):
    start=(m.rows,m.cols) # since the starting block is always bottom right most block for pyamaze.
    g = {cell:float('inf') for cell in m.grid}
    g[start] = 0
    f = {cell:float('inf') for cell in m.grid}
    f[start] = h(start,(1,1)) + g[start]

    queue = PriorityQueue()
    queue.put((h(start,(1,1)),h(start,(1,1)),start)) #each element in the queue has (A* cost = f(n),heuristic cost = h(n),cell coordinate = (x_{n},y_{n}))
    Path={}

    while not queue.empty():
        current_pos = queue.get()[2]
        if current_pos==(1,1):
            break
        for direction in 'ESNW':
            if m.maze_map[current_pos][direction]==True:
                if direction=='E':
                    nextCell = (current_pos[0],current_pos[1]+1)
                if direction=='W':
                    nextCell = (current_pos[0],current_pos[1]-1)
                if direction=='N':
                    nextCell = (current_pos[0]-1,current_pos[1])
                if direction=='S':
                    nextCell = (current_pos[0]+1,current_pos[1])

                temp_g = g[current_pos]+1
                temp_f = temp_g + h(nextCell,(1,1))

                if temp_f < f[nextCell]:
                    g[nextCell] = temp_g
                    f[nextCell] = temp_f
                    queue.put((f[nextCell],h(nextCell,(1,1)),nextCell))
                    Path[nextCell]=current_pos
    
    fwdPath = {}
    cell = (1,1)
    while cell!=start:
        fwdPath[Path[cell]]=cell
        cell=Path[cell]
    return fwdPath

if __name__ == "__main__":
    m = maze(5,5) # change maze dimension here
    m.CreateMaze() # create a maze with one path

    path = A_Star(m)
    a=agent(m,footprints=True)
    m.tracePath({a:path})
    path_length=textLabel(m,'A* path lenght', len(path)+1)

    m.run()