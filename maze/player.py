from maze.maze import Maze, Point


class Player:
    maze :Maze
    pos: Point

    def __init__(self):
        self.maze = Maze(10, 10)
        self.maze.generate()
        self.pos = Point(0,0)