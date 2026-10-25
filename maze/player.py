from enum import Enum

from maze.battle import Battle, Enemy
from maze.maze import Maze, Point


class State(Enum):
    BATTLING =1
    EXPLORING = 2




class Player:



    def __init__(self):
        self.maze = Maze(10, 10)
        self.maze.generate()
        self.pos = Point(0,0)

        self.counter=100
        self.state= State.EXPLORING

        # battle attributes
        # health should reset after each battle
        self.max_health = 3
        self.health = 3

        self.battle = None
        self.skills= []


    def update_cooldowns(self):
        for skill in self.skills:
            skill.update()

#
class Skill:
    def __init__(self,name,cooldown):
        self.name: str = name
        self.cooldown : int = cooldown
        self._track = 0

    def apply(self,player):
        pass

    def update(self):
        self._track = min(self._track-1,0)

    def __str__(self) -> str:
        return f"{self.name} {self._track}/{self.cooldown}"




class Heal(Skill):
    def __init__(self):
        super().__init__("heal",5)

    def apply(self,player):
        player.health = player.max_health


class Instant(Skill):
    def __init__(self):
        super().__init__("instant",10)

    def apply(self,player):
        player.battle.enemy.health = 0