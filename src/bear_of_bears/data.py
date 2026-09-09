from dataclasses import dataclass
from enum import IntEnum


class Slot(IntEnum):
    BODY = 0
    ACCESSORY = 1
    HEAD = 2
    WEAPON = 3
    HANDS = 4
    FEET = 5

    @classmethod
    def from_str(cls, slot_name: str) -> "Slot":
        return cls[slot_name.upper()]


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
