from dataclasses import dataclass
from pydantic import BaseModel, Field, BeforeValidator, field_validator, model_validator
from typing import Literal, Annotated
import json

accepted_ACs = ["--","/","TBD"]
accepted_freqs = ["2x Daily","At-Will","EOT","Scene","Scene x2","Daily","Daily x1","Daily x1 Quick Action","Daily x3","Scene x3","TBD"]
accepted_types = ["Bug","Dark","Dragon","Electric","Fairy","Fighting","Fire","Flying","Ghost","Grass","Ground","Ice","Light","Normal","Poison","Psychic","Rock","Steel","Water"]
accepted_classes = ["Phys","Spec","STATUS","Status"]

class Capability(BaseModel):
    name: str
    value: str

class Skill(BaseModel):
    name: str
    roll: str

class MegaEvolution(BaseModel):
    type: list
    ability: str
    stats: list[str] = Field(default_factory=list,min_length=1)

class Ability(BaseModel):
    name:str
    effect:str
    id:int = -1

class Move(BaseModel):
    name: str
    level: int = -1
    type: str = None

def normalize(v:str) -> str:
    return v.capitalize()

PokemonType = Annotated[Literal["Bug","Dark","Dragon","Electric","Fairy","Fighting","Fire","Flying","Ghost","Grass","Ground","Ice","Normal","Poison","Psychic","Rock","Steel","Water","Light","Data","Sound","Crystal"],
    BeforeValidator(normalize)
]

max_abilities_count = 8
class Pokemon(BaseModel):
    name : str
    stat_hp : int
    stat_atk : int
    stat_def : int
    stat_sp_atk : int
    stat_sp_def : int
    stat_spd : int
    pokemon_types : list[PokemonType] = Field(min_length=1,max_length=3)
    base_abilities : list[Ability] = Field(min_length=1,max_length=max_abilities_count)
    advanced_abilities : list[Ability] = Field(min_length=1,max_length=max_abilities_count)
    high_abilities : list[Ability] = Field(min_length=1,max_length=max_abilities_count)
    custom_abilities : dict[str,Ability] = Field(min_length=1)
    evolutions : list[str] = Field(min_length=1)
    height : str
    weight : str
    gender_ratio_m : str
    gender_ratio_f : str
    egg_group : str
    average_hatch_rate : int
    diet : str
    habitat : str
    capabilities : list[Capability] = Field(min_length=1)
    skills : list[Skill] = Field(min_length=1)
    evo_moves : list[Move]
    moves : list[Move] = Field(min_length=1)
    tm_moves : list[Move]
    tutor_moves : list[Move]
    egg_moves : list[Move]
    mega_evolution : MegaEvolution | None = None


MoveClass = Annotated[Literal["Special","Status","Physical","???","Static"],
    BeforeValidator(normalize)
]

MoveFrequency = Literal["Static","2x Daily","At-Will","EOT","Scene","Scene x2","Daily","Daily x1","Daily x1 Quick Action","Daily x3","Scene x3","TBD"]

class FullMove(BaseModel):
    id : int = -1
    name : str
    types: list[PokemonType] = Field(min_length=1, max_length=3)
    frequency : MoveFrequency
    AC : str
    damage_base : int
    roll : str
    m_class : MoveClass
    range : str
    effect : str
    blessing : str | None = None
    special_effect : str | None = None
    contest_types : str | None = None
    contest_effect : str | None = None
    extra_lines : list[str]

    @field_validator("AC")
    @classmethod
    def manage_static_ac(cls,v: str) -> str:
        if v == "":
            return "None"
        return v

    @field_validator("roll")
    @classmethod
    def roll_should_not_contain_slash(cls,v: str) -> str:
        if "/" in v:
            return v.split("/")[0]
        return v

    @model_validator(mode='after')
    def adjust_from_ac(self) -> FullMove:
        if self.AC == "Static":
            self.frequency = "Static"
            self.AC ="None"
            self.m_class = "Static"
        return self

    def get_frequency(self):
        return self.frequency
    def get_AC(self):
        print_ac = self.AC
        if self.AC.isdigit():
            print_ac = self.AC
        elif self.AC.lower() == "none":
            print_ac = "/"
        return print_ac
    def get_type(self):
        return self.types
    def get_classe(self):
        print_classe = ""
        if self.m_class == "Special":
            print_classe = "Spec"
        elif self.m_class.lower() == "Physical":
            print_classe = "Phys"
        else: # contains case like Status, Static, and weird ones
            print_classe = self.m_class
        return print_classe
    def get_range(self):
        return self.range
    def get_effect(self):
        return self.effect
    def to_csv(self):
        # this is used to override default formating
        print(self.name)
        print(self.get_type())
        final_type = ','.join(self.get_type())
        csv =  self.name+","+self.get_frequency()+","+self.get_AC()+","+final_type+","+self.roll+","+self.get_classe()+","+'"'+self.get_range()+'"'+","+'"'+self.get_effect()+'"'
        return csv