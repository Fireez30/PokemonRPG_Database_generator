from dataclasses import dataclass
import json
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

class FullMove:
    def __init__(self,move,type_val,frequency,ac,damage_base,roll,classe,range_val,effect,blessing,special_effect,contest_type,contest_effect,extra_lines):
        self.move = move
        self.type = type_val
        self.frequency = frequency
        self.AC = ac
        self.damage_base = damage_base
        self.roll = roll
        self.classe = classe
        self.range = range_val
        self.effect = effect
        self.blessing = blessing
        self.special_effect = special_effect
        self.contest_type = contest_type
        self.contest_effect = contest_effect
        self.extra_lines = []
        if self.AC == "":
            self.AC = "None"
        if self.AC == "Static":
            self.frequency = "Static"
            self.AC ="None"
            self.classe = "Static"
    def to_csv(self):

        # this is used to override default formating
        print_classe = ""
        if self.classe.lower() == "special":
            print_classe = "Spec"
        elif self.classe.lower() == "physical":
            print_classe = "Phys"
        else: # contains case like Status, Static, and weird ones
            print_classe = self.classe
        print_ac = self.AC
        if self.AC.isdigit():
            print_ac = self.AC
        elif self.AC.lower() == "none":
            print_ac = "/"
        csv =  self.move+","+self.frequency+","+print_ac+","+self.type+","+self.roll.split("/")[0]+","+print_classe+","+'"'+self.range+'"'+","+'"'+self.effect+'"'
        print(csv.replace(",", " | "))
        return csv