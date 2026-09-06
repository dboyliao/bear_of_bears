from dataclasses import dataclass
from enum import IntEnum


class Slot(IntEnum):
    HEAD = 0
    BODY = 1
    HAND = 2
    SHOES = 3
    WEAPON = 4
    ACCESSORY = 5


@dataclass
class Equipment:
    name: str
    slot: Slot
    attack: int = 0
    defense: int = 0
    intelligence: int = 0
    agility: int = 0

    def json(self) -> dict:
        return {
            "name": self.name,
            "slot": self.slot,
            "attack": self.attack,
            "defense": self.defense,
            "intelligence": self.intelligence,
            "agility": self.agility,
        }

    def __str__(self) -> str:
        return f"{self.name} ({self.slot.name}) ATK: {self.attack}, DEF: {self.defense}, INT: {self.intelligence}, AGI: {self.agility}"
