from enum import Enum


class HerdUnit(str, Enum):
    HEAD = 'head'  # bovinos, ovinos, caprinos, suínos
    HIVE = 'hive'  # abelhas
    TANK = 'tank'  # peixes — por tanque/açude
    FLOCK = 'flock'  # aves
    COLONY = 'colony'  # outros insetos, microrganismos


class HerdStatus(str, Enum):
    ACTIVE = 'active'
    SOLD = 'sold'
    DECEASED = 'deceased'
    TRANSFERRED = 'transferred'


class AnimalStatus(str, Enum):
    ACTIVE = 'active'
    SOLD = 'sold'
    DECEASED = 'deceased'
    SLAUGHTERED = 'slaughtered'
    TRANSFERRED = 'transferred'


class AnimalSex(str, Enum):
    MALE = 'male'
    FEMALE = 'female'
    CASTRATED = 'castrated'
