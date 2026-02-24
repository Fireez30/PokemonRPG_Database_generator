from dataclasses import dataclass

@dataclass
class Capability:
    name: str
    value: str

@dataclass
class Skill:
    name: str
    roll: str

@dataclass
class Move:
    name: str
    level: int = -1
    type: str = None

class Pokemon:
    def __init__(self,name,hp,attack,defense,spattack,spdefense,speed,poketype,base_abilities,advanced_abilities,high_abilities,evolutions,height,weight,gender_ratio_m,gender_ratio_f,egg_group,average_hatch_rate,diet,habitat,capabilities,skills,moves,tm_moves,tutor_moves,egg_moves):
        self.name = name
        self.stat_hp = hp
        self.stat_atk = attack
        self.stat_def = defense
        self.stat_sp_atk = spattack
        self.stat_sp_def = spdefense
        self.stat_spd = speed
        self.pokemon_types = poketype
        self.base_abilities = base_abilities
        self.advanced_abilities = advanced_abilities
        self.high_abilities = high_abilities
        self.evolutions = evolutions
        self.height = height
        self.weight = weight
        self.gender_ratio_m = gender_ratio_m
        self.gender_ratio_f = gender_ratio_f
        self.egg_group = egg_group
        self.average_hatch_rate = average_hatch_rate
        self.diet= diet
        self.habitat = habitat
        self.capabilities = capabilities
        self.skills = skills
        self.moves = moves
        self.tm_moves = tm_moves
        self.tutor_moves = tutor_moves
        self.egg_moves = egg_moves