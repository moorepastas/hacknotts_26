import random
from dataclasses import dataclass
from enum import Enum
from typing import List, NamedTuple


class Point(NamedTuple):
    x: int
    y: int





class Compass(Enum):
    North =0 # -1,0
    East=1 # 0,1
    South =2 # 1,0

    West=3 # 0,-1



@dataclass
class Place:
    Directions: List[Compass]
    visited: bool




class Maze:
    _maze: List[List[Place]]
    x:int
    y:int
    start: Point



    def __init__(self,x:int,y:int):
        self.x = x
        self.y = y
        self.start = None
        self._maze = None

    def display(self):

        print("+-"*self.x+'+')
        for r in self._maze:
            self._display_row(r)
            self._display_in_between(r)

    # generate a maze using recurrsive backtracking
    def generate(self):
        self._maze = [[Place([], False,) for _ in range(self.x)] for _ in range(self.y)]
        stack: List[Point] =[None]

        start_x = random.randint(0,self.x-1)
        start_y = random.randint(0,self.y-1)
        # chose a random starting point
        current = Point(start_x,start_y)
        self.start = current



        while current is not None:
            self._maze[current.y][current.x].visited = True
            # check that all adjacent walls have not been gone through
            good = []
            for direction in [(Compass.North,(-1,0)),(Compass.South,(1,0)),(Compass.East,(0,1)),(Compass.West,(0,-1))]:
                new_x,new_y = current.x + direction[1][1] , current.y+direction[1][0]

                # quick bounds check
                if 0<=new_x<self.x and 0<=new_y<self.y:
                    if self._maze[new_y][new_x].visited:
                        continue
                    else:
                        good.append(direction)


            if len(good) == 0:
                #can't go anywhere so backtrack
                current = stack.pop()
                continue
            else:
                # choose a random place to go to
                c = random.choice(good)
                new_x,new_y = current.x + c[1][1] , current.y+c[1][0]

                curr_dir = c[0]
                second = Compass((curr_dir.value+2) % 4)

                self._maze[current.y][current.x].Directions.append(curr_dir)
                self._maze[new_y][new_x].Directions.append(second)







                stack.append(current)
                current = Point(new_x,new_y)
        # reset the visited metrix for the user to use
        for y in range(self.y):
            for x in range(self.x):
                self._maze[y][x].visited = False



    # 'explores' a point and returns all the directions you can travel in
    def explore(self,x,y) -> List[Compass]:
         return self._maze[y][x].Directions

    def can_go(self,x,y,direction: Compass)->bool:
        return direction in self._maze[y][x].Directions


    def _display_row(self,row: List[Place]):
        print("|" if not Compass.West in row[0].Directions else " ",end="")
        for p in row:
            print(" ",end="")
            print("|" if not Compass.East in p.Directions else " ",end="")
        print()



    # the row is the one above
    def _display_in_between(self,row: List[Place]):
        print("+", end="")
        for p in row:
            print("-" if not Compass.South in p.Directions else " ",end="")
            print("+",end="")
        print()


    # display map for the user, checks to see if a node has been visited before displaying it
    def map(self,current:Point):
        buf = ""
        for y in range(self.y):
            for x in range(self.x):
                n = self._maze[y][x]

                if current.x == x and current.y == y:
                    buf += "O"
                elif n.visited:
                    buf += "X"
                else:
                    buf += " "

                if (n.visited and Compass.East in n.Directions) or (x < self.x-1 and self._maze[y][x+1].visited and Compass.West in self._maze[y][x+1].Directions):
                    buf += " - "
                else:
                    buf+="   "
            buf+="\n"
            # generate the in between
            for x in range(self.x):
                if y == self.y-1:
                    # bottom
                    break
                n = self._maze[y][x]
                n1 = self._maze[y+1][x]

                if (n.visited and Compass.South in n.Directions) or (n1.visited and Compass.North in n.Directions):
                    buf+="|"
                else:
                    buf += " "
                buf += "   "
            buf+= "\n"

        return buf




if __name__ == '__main__':
    m = Maze(10,10)
    m.generate()

    m.display()

    print(m.map(Point(0,0)))