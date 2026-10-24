from typing import Dict

from classes.channel import Channel
from classes.user import User
from maze.maze import Point, Compass
from maze.player import Player


class MazeChannel(Channel):
    players: Dict[str,Player] = {}


    def join(self, user:User):
        user.protocol.join(user.name(),"#maze")
        if user.nick not in self.players.keys():
            self.players[user.nick] = Player()



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

                pos = self.players[user.nick].pos
                if not self.players[user.nick].maze.can_go(pos.x,pos.y,comp):
                    user.protocol.privmsg("The_Dungeon_Master","#maze",f"You cannot go in the direction {direction}! The heavy walls block you!")
                    return

                new = [(-1,0),(0,1),(1,0),(0,-1)][comp.value]
                new_x, new_y = pos.x + new[1], pos.y + new[0]

                self.players[user.nick].pos  = Point(new_x,new_y)

                user.protocol.privmsg("The_Dungeon_Master","#maze",f"You moved {direction}")

            case ["dirs"|"d"]:
                pos = self.players[user.nick].pos
                user.protocol.privmsg("The_Dungeon_Master","#maze",f"You can move {", ".join([i.name for i in sorted(self.players[user.nick].maze.explore(pos.x,pos.y), key=lambda x: x.value)])}")
            case ["map"]:
                pos = self.players[user.nick].pos
                user.protocol.privmsg("The_Dungeon_Master", "#maze","you consult the map")

                lines = self.players[user.nick].maze.map(pos)
                print(lines.split("\n"))
                for line in lines.split("\n"):
                    if line.strip(" ") != "":
                        user.protocol.privmsg("map","#maze",line)









