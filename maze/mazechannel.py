from typing import Dict

from classes.channel import Channel
from classes.user import User
from maze.maze import Maze, Point, Compass


class MazeChannel(Channel):
    maze: Dict[str,Maze] = {}
    location: Dict[str,Point] = {}

    def join(self, user:User):
        user.protocol.join(user.name(),"#maze")
        if user.nick not in self.maze.keys():
            self.maze[user.nick] = Maze(10,10)
            self.maze[user.nick].generate()
            self.location[user.nick] = Point(0,0)



    def send(self,user:User, message : str):
        print(message)
        args = message.lower().split()

        match args:
            #

            case ["move"|"m", direction]:
                try:
                    comp = Compass[direction.capitalize()]
                except NameError:
                    user.protocol.privmsg("The_Dungeon_Master","#maze",f"{direction} is not a valid direction")
                    return

                pos = self.location[user.nick]
                if not self.maze[user.nick].can_go(pos.x,pos.y,comp):
                    user.protocol.privmsg("The_Dungeon_Master","#maze",f"You cannot go in the direction {direction}! The heavy walls block you!")
                    return

                new = [(-1,0),(0,1),(1,0),(0,-1)][comp.value]
                new_x, new_y = pos.x + new[1], pos.y + new[0]

                self.location[user.nick]  = Point(new_x,new_y)

                user.protocol.privmsg("The_Dungeon_Master","#maze",f"You moved {direction}")

            case ["dirs"|"d"]:
                pos = self.location[user.nick]
                user.protocol.privmsg("The_Dungeon_Master","#maze",f"You can move {", ".join([i.name for i in sorted(self.maze[user.nick].explore(pos.x,pos.y), key=lambda x: x.value)])}")
            case ["map"]:
                pos = self.location[user.nick]
                user.protocol.privmsg("The_Dungeon_Master", "#maze","you consult the map")

                lines = self.maze[user.nick].map(pos)
                print(lines.split("\n"))
                for line in lines.split("\n"):
                    if line.strip(" ") != "":
                        user.protocol.privmsg("map","#maze",line)









