from pydantic import BaseModel, Field, BeforeValidator, field_validator, model_validator,PositiveInt
from typing import Literal, Annotated, Dict
import re

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


STAT_KEYS = {"Hp", "Atk", "Def", "SpAtk", "SpDef", "Spd"}
STAT_PATTERN = re.compile(r'^[+-]\d+$')

def DAMAGE_BASE_TO_ROLL():
    return {
    1: '1d6+1',
    2: '1d6+3',
    3:  '1d6+5',
    4:  '1d8+6',
    5:  '1d8+8',
    6:  '2d6+8',
    7:  '2d6+10',
    8:  '2d8+10',
    9:  '2d10+10',
    10: '3d8+10',
    11: '3d10+10',
    12: '3d12+10',
    13: '4d10+10',
    14: '4d10+15',
    15: '4d10+20',
}

def ROLL_TO_DAMAGE_BASE():
    return {
        '1d6+1' : 1,
        '1d6+3' : 2,
        '1d6+5' : 3,
        '1d8+6': 4,
        '1d8+8': 5,
        '2d6+8': 6,
        '2d6+10': 7,
        '2d8+10': 8,
        '3d6+10': 8,
        '2d10+10': 9,
        '3d8+10': 10,
        '3d10+10': 11,
        '3d12+10': 12,
        '4d10+10': 13,
        '4d10+15': 14,
        '4d10+20': 15
}
class StatsModel(BaseModel):
    stats: Dict[str, str]

    @field_validator('stats')
    @classmethod
    def validate_stats(cls, v: Dict[str, str]) -> Dict[str, str]:
        if v.keys() != STAT_KEYS:
            missing = STAT_KEYS - v.keys()
            extra = v.keys() - STAT_KEYS
            raise ValueError(f"Invalid keys. Missing: {missing}, Extra: {extra}")
        result = {}
        for key, val in v.items():
            if not STAT_PATTERN.match(val):
                if re.match(r'^\d+$', val):
                    val = f"+{val}"
                else:
                    raise ValueError(f"'{key}' value '{val}' is not a valid integer string")
                result[key] = val
        return result

class MegaEvolution(BaseModel):
    type: list
    ability: str
    stats: StatsModel

class Ability(BaseModel):
    name:str
    effect:str
    id:int = -1

class Move(BaseModel):
    name: str
    level: int = -1
    type: str | None = None

def normalize(v:str) -> str:
    return v.capitalize()

PokemonType = Annotated[Literal["Bug","Dark","Dragon","Electric","Fairy","Fighting","Fire","Flying","Ghost","Grass","Ground","Ice","Normal","Poison","Psychic","Rock","Steel","Water","Light","Data","Sound","Crystal","None"],
    BeforeValidator(normalize)
]

max_abilities_count = 8
class Pokemon(BaseModel):
    name : str = Field(min_length=1)
    stat_hp : PositiveInt
    stat_atk : PositiveInt
    stat_def : PositiveInt
    stat_sp_atk : PositiveInt
    stat_sp_def : PositiveInt
    stat_spd : PositiveInt
    pokemon_types : list[PokemonType] = Field(min_length=1,max_length=3)
    base_abilities : list[Ability] = Field(min_length=1,max_length=max_abilities_count)
    advanced_abilities : list[Ability] = Field(min_length=1,max_length=max_abilities_count)
    high_abilities : list[Ability] = Field(min_length=1,max_length=max_abilities_count)
    custom_abilities : dict[str,Ability] = Field(default_factory=dict)
    evolutions : list[str] = Field(min_length=0)
    height : str
    weight : str
    gender_ratio_m : float
    gender_ratio_f : float
    egg_group : str
    average_hatch_rate : int
    diet : str
    habitat : str
    capabilities : list[Capability] = Field(min_length=1)
    skills : list[Skill] = Field(min_length=1)
    evo_moves : list[Move] = Field(default_factory=list)
    moves : list[Move] = Field(min_length=1)
    tm_moves : list[Move] = Field(default_factory=list)
    tutor_moves : list[Move] = Field(default_factory=list)
    egg_moves : list[Move] = Field(default_factory=list)
    mega_evolution : MegaEvolution | None = None

    @field_validator("mega_evolution", mode="before")
    @classmethod
    def fix_megaevo(cls, v) -> MegaEvolution | None:
        if v == "":
            return None
        return v

    @field_validator("tm_moves", mode="before")
    @classmethod
    def clean_tm_moves(cls, v) -> list[Move]:
        final_tmmoves = []
        for m in v:
            if m["name"].lower().strip() == "unofficial homebrew":
                continue
            else:
                m["name"] = m["name"].replace("Unofficial Homebrew","").strip()
                final_tmmoves.append(m)
        return final_tmmoves

    @field_validator("gender_ratio_m", "gender_ratio_f", mode="before")
    @classmethod
    def coerce_gender_ratio(cls, v) -> str:
        return str(v)

    @model_validator(mode='after')
    def fix_empty_evo(self) -> Pokemon:
        if len(self.evolutions) == 0:
            self.evolutions = [self.name]
        return self

    @field_validator("pokemon_types", mode="before")
    @classmethod
    def split_multiple_types(cls, v) -> list[PokemonType]:
        final_types = []
        for typen in v:
            if " " in typen.strip():
                splitted = typen.split(" ")
                for s in splitted:
                    final_types.append(s)
            else:
                final_types.append(typen)
        return final_types

    @field_validator("base_abilities", "advanced_abilities", "high_abilities", mode="before")
    @classmethod
    def coerce_ability_lists(cls, v):
        if isinstance(v, list):
            return [{"name": a, "effect": "", "id": -1} if isinstance(a, str) else a for a in v]
        return v

    @field_validator("moves", "tm_moves", "tutor_moves", "egg_moves", "evo_moves", mode="before")
    @classmethod
    def coerce_move_lists(cls, v):
        if isinstance(v, list):
            return [{"name": m, "level": -1, "type": None} if isinstance(m, str) else m for m in v]
        return v


MoveClass = Annotated[Literal["Special","Status","Physical","???","Static","Versatile","None","See Text","See effect","TBD","Use highest offense","Hits_spdef"],
    BeforeValidator(normalize)
]

MoveFrequency = Literal["Static","Daily x2","2x Daily","At-Will","EOT","Scene","Scene x2","Scene x1","Daily","Daily x1","Daily x1 Quick Action","Daily x3","Scene x3","TBD","See Text"]

class FullMove(BaseModel):
    id : int = -1
    name : str
    types: list[PokemonType] = Field(min_length=1, max_length=3)
    frequency : MoveFrequency
    AC : str
    damage_base : int | None
    roll : str | None
    m_class : MoveClass
    range : str
    effect : str
    blessing : str | None = None
    special_effect : str | None = None
    contest_types : str | None = None
    contest_effect : str | None = None
    extra_lines : list[str] | None = None

    @field_validator("m_class", mode="before")
    @classmethod
    def clean_extra_long_class(cls, v):
        if not v:
            return "TBD"
        if v.lower().startswith('tbd'):
            return "TBD"
        if v.lower().startswith("use_highest_offense"):
            return "Use Highest Offense"
        if v.startswith("Versatile "):
            return v.split(" ")[0]
        if v.lower() == 'pstatus' or v.lower().startswith('status'):
            return 'Status'
        if v.lower().startswith('special'):
            return "Special"
        if v.lower() == 'physic' or v.lower().startswith('physical') or v.lower().startswith('phsyical'):
            return 'Physical'
        return v

    @field_validator("frequency", mode="before")
    @classmethod
    def replace_grammar_errors(cls, v):
        if not v:
            return "TBD"
        v = v.replace("/em>", "")
        if 'at will' in v.lower() or v.lower() == "at-will":
            return "At-Will"
        return v.replace("Scence", "Scene")


    @field_validator("AC")
    @classmethod
    def manage_static_ac(cls,v: str) -> str:
        if v == "":
            return "None"
        return v

    @field_validator("roll")
    @classmethod
    def roll_should_not_contain_slash(cls,v: str) -> str:
        if v is None:
            return None
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
        returnstr = ""
        for otype in self.types:
            returnstr += otype + "/"
        return returnstr[:-1]
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
        final_type =self.get_type()
        csv =  self.name+","+self.get_frequency()+","+self.get_AC()+","+final_type+","+(self.roll if self.roll else "")+","+self.get_classe()+","+'"'+self.get_range()+'"'+","+'"'+self.get_effect()+'"'
        return csv