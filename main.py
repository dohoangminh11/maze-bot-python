import turtle as tt

"""
-----------------------------------------------------------------------------
i11_Nunu_DoNguyen_project.py: Project Report "MAZE EXPLORATION WITH TURTLE", minINT

Nunu Daniel <Daniel.Nunu@etu.univ-grenoble-alpes.fr>
Do Nguyen Hoang Minh <Hoang-Minh.Do-Nguyen@etu.univ-grenoble-alpes.fr>
-----------------------------------------------------------------------------
"""

def labyFromFile(fn):
    f = open(fn)
    laby = []
    indline = 0
    for fileline in f:
        labyline = []
        inditem = 0
        for item in fileline:
            if item == ".":
                labyline.append(0) 
            elif item == "#":
                labyline.append(1)  
            elif item == "x":
                labyline.append(0)  
                mazeIn = [indline, inditem]
            elif item == "X":
                labyline.append(0)  
                mazeOut = [indline, inditem]
            inditem += 1
        laby.append(labyline)
        indline += 1
    f.close()
    return laby, mazeIn, mazeOut

def cell2pixel(row, column, gameDict):
    cell_size = gameDict["cell_size"]
    x_origin, y_origin = gameDict["origin"]
    x = x_origin + (column * cell_size) + (cell_size // 2)
    y = y_origin - (row * cell_size) - (cell_size // 2)
    return x, y

def typeCellule(row, column, gameDict):
    maze = gameDict["maze"]
    if not (0 <= row < len(maze)) or not (0 <= column < len(maze[0])):
        return "outside"
    if [row, column] == gameDict["entrance"]:
        return "entrance"
    elif [row, column] == gameDict["exit"]:
        return "exit"
    elif maze[row][column] == 1:
        return "wall"
    neighbors = [
        (row - 1, column),
        (row + 1, column),
        (row, column - 1),
        (row, column + 1),
    ]
    path_count = sum(
        0 <= r < len(maze) and 0 <= c < len(maze[0]) and maze[r][c] == 0
        for r, c in neighbors
    )
    if path_count == 1:
        return "dead-end"
    elif path_count >= 3:
        return "crossing"
    return "standard-path"

def handleSpecialCell(row, column, gameDict, player_turtle):
    cell_type = typeCellule(row, column, gameDict)
    colors = {
        "crossing": "pink",
        "dead-end": "blue",
        "entrance": "orange",
        "exit": "green",
        "standard-path": "black"}
    player_turtle.color(colors[cell_type])
    if cell_type == "exit":
        print("Victory!")

def graphicDisplay(gameDict):
    screen = tt.Screen()
    screen.tracer(0)
    screen.setup(700, 700)
    drawer = tt.Turtle()
    drawer.speed(0)
    drawer.penup()
    drawer.hideturtle()
    cell_size = gameDict["cell_size"]
    for i, row in enumerate(gameDict["maze"]):
        for j, cell in enumerate(row):
            x, y = cell2pixel(i, j, gameDict)
            drawer.goto(x - cell_size // 2, y - cell_size // 2) #Updates position for each square to bottom right pixel
            if cell == 1:
                drawer.fillcolor("black")
            elif [i, j] == gameDict["entrance"]:
                drawer.fillcolor("yellow")
            elif [i, j] == gameDict["exit"]:
                drawer.fillcolor("red")
            else:
                drawer.fillcolor("white")
            drawer.begin_fill()
            for _ in range(4):
                drawer.forward(cell_size)
                drawer.left(90)
            drawer.end_fill()
    screen.update()
    screen.tracer(1)
    
def textDisplay(laby):
    line = ''
    for a in range(len(laby['maze'])):
        for b in range(len(laby['maze'][0])):
            temp = laby['maze'][a][b]
            if temp == 1:
                line += '#'
            elif a == laby['entrance'][0] and b == laby['entrance'][1]:
                line += 'X'
            elif a == laby['exit'][0] and b == laby['exit'][1]:
                line += 'O'
            elif temp == 0:
                line += ' '       
        print(line)
        line = ''
        
def move(x, y, gameDict,direction):
    global turtle_pos

    new_pos = [turtle_pos[0] + y, turtle_pos[1] + x] 
    cell_type = typeCellule(new_pos[0], new_pos[1], gameDict) #Evaluates the position of the cell we want to move to    
    path_history.append(direction) # Saving the commands in a list
    if cell_type in ["wall", "outside"]:
        print("It's a wall or outside the maze!")
        player_turtle.color("red")
    else:
        turtle_pos = new_pos
        x, y = cell2pixel(turtle_pos[0], turtle_pos[1], gameDict)
        player_turtle.showturtle()
        player_turtle.goto(x, y)
        if direction == 'l':
            player_turtle.setheading(180)
        elif direction == 'r':
            player_turtle.setheading(0)
        elif direction == 'u':
            player_turtle.setheading(90)
        else:
            player_turtle.setheading(270)
        handleSpecialCell(turtle_pos[0], turtle_pos[1], gameDict, player_turtle)

# This only works because of the lambda function, which allows us to call a function with pre-determined parameters.
def enableManualControl(gameDict):
    '''This function listens to the user's input and calls the move() function with the correct parameters'''
    tt.listen()
    tt.onkeypress(lambda: move(-1, 0, gameDict, direction='l'), "Left")
    tt.onkeypress(lambda: move(1, 0, gameDict, direction='r'), "Right")
    tt.onkeypress(lambda: move(0, -1, gameDict, direction='u'), "Up")
    tt.onkeypress(lambda: move(0, 1, gameDict, direction='d'), "Down")
        
def suivre_chemin(path, gameDict):
    '''Input: a list with directions
        Output: none, but moves the turtle according to the directions'''
    for elem in path:
        if elem == 'l':
            move(-1, 0, gameDict, direction='l')
        elif elem == 'r':
            move(1, 0, gameDict, direction='r')
        elif elem == 'u':
            move(0, -1, gameDict, direction='u')
        else:
            move(0, 1, gameDict, direction='d')

def restart():
    '''Re-executes the main function, resetting the path list'''
    print('Restart')
    player_turtle.ht()
    runMainProgram()
    
def stop():
    '''Closes the game window'''
    tt.bye()               

# def explorer_left(gameDict):  # This function follows the Hand-On-Wall algorithm
#     global turtle_pos, player_turtle
#     player_turtle.goto(cell2pixel(turtle_pos[0], turtle_pos[1], gameDict))
#     while turtle_pos != gameDict['exit']:
#         if player_turtle.getHeading() == 0: # if turtle is facing right
#             left_cell = [turtle_pos[0],turtle_pos[1]-1]
#             front_cell = [turtle_pos[0]+1,turtle_pos[1]]
#             right_cell = [turtle_pos[0],turtle_pos[1]+1]
#             if typeCellule(left_cell[0],left_cell[1],gameDict) in ('standard path','crossing'):
#                 move(0, -1, gameDict, direction='u')
#             elif typeCellule(front_cell[0],front_cell[1],gameDict) == 'wall':
#                 if typeCellule(right_cell[0],right_cell[1],gameDict) == 'wall':
#                     move(-1, 0, gameDict, direction='l')
#                 else:
#                     move(0, 1, gameDict, direction='d')
#             else:
#                 move(1, 0, gameDict, direction='r')
#         if player_turtle.getHeading() == 90: # if turtle is facing up (north)
#             left_cell = [turtle_pos[0]-1,turtle_pos[1]]
#             front_cell = [turtle_pos[0],turtle_pos[1]+1]
#             right_cell = [turtle_pos[0]+1,turtle_pos[1]]
#             if typeCellule(left_cell[0],left_cell[1],gameDict) in ('standard path','crossing'):
#                 move(-1, 0, gameDict, direction='l')
#             elif typeCellule(front_cell[0],front_cell[1],gameDict) == 'wall':
#                 if typeCellule(right_cell[0],right_cell[1],gameDict) == 'wall':
#                     move(0, 1, gameDict, direction='d')
#                 else:
#                     move(0, -1, gameDict, direction='u')
#             else:
#                 move(1, 0, gameDict, direction='r')
#         if player_turtle.getHeading() == 180: # if turtle is facing left
#             left_cell = [turtle_pos[0],turtle_pos[1]+1]
#             front_cell = [turtle_pos[0]-1,turtle_pos[1]]
#             right_cell = [turtle_pos[0],turtle_pos[1]-1]
#             if typeCellule(left_cell[0],left_cell[1],gameDict) in ('standard path','crossing'):
#                 move(0, 1, gameDict, direction='d')
#             elif typeCellule(front_cell[0],front_cell[1],gameDict) == 'wall':
#                 if typeCellule(right_cell[0],right_cell[1],gameDict) == 'wall':
#                     move(1, 0, gameDict, direction='r')
#                 else:
#                     move(0, -1, gameDict, direction='u')
#             else:
#                 move(-1, 0, gameDict, direction='l')
#         if player_turtle.getHeading() == 0: # if turtle is facing down (south)
#             left_cell = [turtle_pos[0]+1,turtle_pos[1]]
#             front_cell = [turtle_pos[0],turtle_pos[1]-1]
#             right_cell = [turtle_pos[0]-1,turtle_pos[1]]
#             if typeCellule(left_cell[0],left_cell[1],gameDict) in ('standard path','crossing'):
#                 move(1, 0, gameDict, direction='r')
#             elif typeCellule(front_cell[0],front_cell[1],gameDict) == 'wall':
#                 if typeCellule(right_cell[0],right_cell[1],gameDict) == 'wall':
#                     move(0, -1, gameDict, direction='u')
#                 else:
#                     move(-1, 0, gameDict, direction='l')
#             else:
#                 move(0, 1, gameDict, direction='d')
# The above function is not functional, and we will attempt to explain why in the presentation.

def explorer(gameDict):
    global turtle_pos
    visited = set()
    path_route = []
    dfs(turtle_pos, gameDict, visited, path_route)
    return path_route
# Depth first search algorithm


def dfs(pos, gameDict, visited, path_stack):
    if tuple(pos) in visited:
        return False
    visited.add(tuple(pos))
    if pos == gameDict["exit"]:
        print("Exit found!")
        return True
    # Up direction
    new_pos = [pos[0] - 1, pos[1]]  # Move up
    if typeCellule(new_pos[0], new_pos[1], gameDict) not in ["wall", "outside"] and tuple(new_pos) not in visited:
        path_stack.append("u")
        if dfs(new_pos, gameDict, visited, path_stack):
            return True
        path_stack.pop()
    # Down direction
    new_pos = [pos[0] + 1, pos[1]]  # Move down
    if typeCellule(new_pos[0], new_pos[1], gameDict) not in ["wall", "outside"] and tuple(new_pos) not in visited:
        path_stack.append("d")
        if dfs(new_pos, gameDict, visited, path_stack):
            return True
        path_stack.pop()
    # Left direction
    new_pos = [pos[0], pos[1] - 1]  # Move left
    if typeCellule(new_pos[0], new_pos[1], gameDict) not in ["wall", "outside"] and tuple(new_pos) not in visited:
        path_stack.append("l")
        if dfs(new_pos, gameDict, visited, path_stack):
            return True
        path_stack.pop()
    # Right direction
    new_pos = [pos[0], pos[1] + 1]  # Move right
    if typeCellule(new_pos[0], new_pos[1], gameDict) not in ["wall", "outside"] and tuple(new_pos) not in visited:
        path_stack.append("r")
        if dfs(new_pos, gameDict, visited, path_stack):
            return True
        path_stack.pop()
    return False    

def screenClick(x, y):
    '''Function which checks if the x,y coordinates correspond to a button'''
    button_x = 300  
    button_width = 60  
    if button_x - button_width < x < button_x + button_width:
        if 80 < y < 120:  # "Manual Mode" button
            enableManualControl(gameDict)
        elif 30 < y < 70:  # "Auto Mode" button
            shortest_path = explorer(gameDict)
            print("Shortest Path:", shortest_path)
            suivre_chemin(shortest_path, gameDict)
            tt.done()
        elif -20 < y < 20:  # "Restart" button
            restart()
        elif -70 < y < -30:  # "Exit" button
            stop()

def drawButton(label, x, y):
    '''Input: message=string variable; x=x position of the square; y=y position of the square
        Output: draws a square and stretches it to twice the size of a cell in width and 5* in length'''
    drawer = tt.Turtle()
    drawer.speed(0)
    drawer.penup()
    drawer.goto(x, y)
    drawer.shape("square")
    drawer.shapesize(stretch_wid=2, stretch_len=6) 
    drawer.fillcolor("lightgray")
    drawer.stamp()
    drawer.goto(x, y - 10)
    drawer.write(label, align="center", font=("Arial", 12, "bold"))
    drawer.hideturtle()


# Loading the maze
filepath = input("Enter the filename of the maze to load  ")
maze, mazeIn, mazeOut = labyFromFile(filepath)
cell_size = 20
maze_width = len(maze[0]) * cell_size
maze_height = len(maze) * cell_size

origin_x = -maze_width // 2
origin_y = maze_height // 2
gameDict = {
    "maze": maze,
    "entrance": mazeIn,
    "exit": mazeOut,
    "cell_size": cell_size,
    "origin": (origin_x, origin_y)}


def runMainProgram():
    global player_turtle, turtle_pos, path_history, gameDict

    graphicDisplay(gameDict)

    turtle_pos = mazeIn
    player_turtle = tt.Turtle(shape="turtle", visible=False)
    player_turtle.penup()
    player_turtle.goto(cell2pixel(gameDict["entrance"][0], gameDict["entrance"][1], gameDict))

    path_history = []

    button_x = 300 
    drawButton("Manual Mode", button_x, 100)
    drawButton("Auto Mode", button_x, 50)
    drawButton("Restart", button_x, 0)
    drawButton("Exit", button_x, -50)

    screen = tt.Screen()
    screen.onclick(screenClick)

    tt.done()



if __name__ == "__main__":
    runMainProgram()