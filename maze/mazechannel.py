import math
import random
from typing import Dict

from classes.channel import Channel
from classes.user import User

from maze.battle import Enemy, Battle, Elements
from maze.maze import Point, Compass
from maze.player import Player, State


class MazeChannel(Channel):
    players: Dict[str,Player] = {}


    def join(self, user:User):
        user.protocol.join(user.name(),"#maze")
        if user.nick not in self.players.keys():
            self.players[user.nick] = Player()



    def send(self,user:User, message : str):
        player = self.players[user.nick]

        match player.state:
            case State.EXPLORING:
                self.exploring(message,player,user)
            case State.BATTLING:
                self.battling(message,player,user)


    def exploring(self,message,player,user):
        args = message.lower().split()

        match args:
            #

            case ["move"|"m", direction]:
                try:
                    comp = Compass[direction.capitalize()]
                except NameError:
                    user.protocol.privmsg("The_Dungeon_Master","#maze",f"{direction} is not a valid direction")
                    return


                pos = player.pos
                if not player.maze.can_go(pos.x,pos.y,comp):
                    user.protocol.privmsg("The_Dungeon_Master","#maze",f"You cannot go in the direction {direction}! The heavy walls block you!")
                    return

                new = [(-1,0),(0,1),(1,0),(0,-1)][comp.value]
                new_x, new_y = pos.x + new[1], pos.y + new[0]



                player.pos  = Point(new_x,new_y)

                user.protocol.privmsg("The_Dungeon_Master","#maze",f"You moved {direction}")
                new, dirs = player.maze.explore(pos.x,pos.y)
                user.protocol.privmsg("The_Dungeon_Master", "#maze",
                                      f"You can move {", ".join([i.name for i in sorted(dirs, key=lambda x: x.value)])}")

                player.counter = max(player.counter - (10 if new else 2),0)

                # if it hits a 0 it should trigger an encounter
                if random.randint(0,player.counter) == 0:
                    self.encounter()





            case ["dirs"|"d"]:
                pos = self.players[user.nick].pos
                user.protocol.privmsg("The_Dungeon_Master","#maze",f"You can move {", ".join([i.name for i in sorted(self.players[user.nick].maze.explore(pos.x,pos.y)[1], key=lambda x: x.value)])}")
            case ["map"]:
                pos = self.players[user.nick].pos
                user.protocol.privmsg("The_Dungeon_Master", "#maze","you consult the map")

                lines = self.players[user.nick].maze.map(pos)
                print(lines.split("\n"))
                for line in lines.split("\n"):
                    if line.strip(" ") != "":
                        user.protocol.privmsg("map","#maze",line)


    # triggers when encoutering a battle with an enemy
    def encounter(self,player:Player, user:User):
        name = random.choice(["ogre", "slime", "izangi","golden_hand"])

        difficulty = int(math.sqrt((player.pos.y**2)+(player.pos.x**2)))

        enemy = Enemy(int(math.sqrt(difficulty)),name=name)

        battle = Battle(enemy,difficulty)

        player.battle = battle
        player.health = player.max_health

        user.protocol.privmsg("The_Dungeon_Master","#maze",f"{name} has appeared, take e'm down.")
        player.state = State.BATTLING

    def battling(self, message, player, user:User):
        args = message.lower().split()

        match args:
            case [("rock"|"paper"|"scissors")]:
                user.protocol.privmsg("The_Dungeon_Master", "#maze", f"You played {args[0]}")

                e_choice = Elements(random.randint(0,2))
                user.protocol.privmsg("The_Dungeon_Master", "#maze", f"{player.battle.enemy.name} played {e_choice.name.lower()}")
                p_choice = Elements[args[0].capitalize()]

                if (e_choice==p_choice):
                    user.protocol.privmsg("The_Dungeon_Master", "#maze",
                                          f"It appears you drew, nothing happened.")
                elif ((e_choice+1)%3 == p_choice):
                    user.protocol.privmsg("The_Dungeon_Master", "#maze",
                                          f"It appears you lost, it hurt.")
                    player.health-=1
                elif ((p_choice+1)%3 == e_choice):
                    user.protocol.privmsg("The_Dungeon_Master", "#maze",
                                          f"It appears you won, the enemy got hurt.")
                    player.battle.enemy.health-=1

            case ["skills"]:
                for skill in player.skills:
                    user.protocol.privmsg("The_Dungeon_Master", "#maze", skill)

            case _:
                return


        if player.battle.enemy.health == 0:
            user.protocol.privmsg("The_Dungeon_Master", "#maze", "The enemy has been defeated, you may return to exploring!")
            player.state = State.EXPLORING
            player.battle = None
            return

        if player.health == 0:
            user.protocol.privmsg("The_Dungeon_Master", "#maze", "Game over, hopefully your replacement will be better than you!")
            del self.players[user.nick]
            self.join(user)
            return


        # print the hud
        health_print  = lambda health : "# "*health
        user.protocol.privmsg("The_Dungeon_Master", "#maze",
                              f"{user.nick} | {health_print(user.player.health)}")

















