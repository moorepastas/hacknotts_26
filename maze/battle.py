from enum import Enum

from attr import dataclass


class Elements(Enum):
    Rock = 0
    Paper = 1
    Scissors = 2



@dataclass
class Enemy:
    health: int

    name: str



@dataclass
class Battle:
    enemy: Enemy
    difficulty: int