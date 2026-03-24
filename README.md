# Maze Explorer 🐢

A Python maze game built with Turtle graphics. Navigate a maze manually 
or let the algorithm solve it automatically.

## Features
- **Manual mode** — arrow key controls
- **Auto mode** — automatic solving with Depth-First Search (DFS)
- Color-coded cells: crossings (pink), dead-ends (blue), 
  entrance (orange), exit (green)

## How to run
```bash
python main.py
```
Then enter the maze filename when prompted (e.g. `maze1.laby`).

## Maze file format
Create a `.laby` text file using:
- `#` → wall
- `.` → open path
- `x` → entrance
- `X` → exit

Example:
```
########
#x..#..#
#.##...#
#....#.#
##.#...#
#...##.#
#.#....#
#....#X#
########
```

## Algorithm
The auto-solver uses **Depth-First Search (DFS)** — recursively explores 
all paths, backtracking when hitting dead ends, until the exit is found.

## Authors
- Do Nguyen Hoang Minh
- Nunu Daniel
