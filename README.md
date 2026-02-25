# PokemonRPG_Database_generator
This repository contains code for generation of a Json base of the pokemon extracted from our RPG documentation

## Install :

You need to install python first, and than open a command prompt (windows) or a terminal (linux) inside this folder.

The code can be installed
```
python -m venv my_env 
source my_env/bin/activate
pip install pymupdf
```

## Usage : 

As long as you have the "data" folder containing the files in the same folder than the "generate_pokemon" script, 
you don't need to provide any path to any file.

### then activate environment :
 
*For fish (linux) :* 

`source my_env/bin/activate.fish`

*for other shells :*

`source my_env/bin/activate`

than you can start the code:

`python generate_pokemon.py`


The code will ask for the following informations, in this order : 

- The name of the pokemon to generate.
- Level of the pokemon
- Rarity of the pokemon (Normal, Shiny or Platine)
- Card of the pokemon (None, Normal, Shiny or Platine)
- Choosing the Pokemon nature 
  - Either providing the nature yourself (answer 'y')
    - in this case, enter the buffed stat first (HP, ATK, DEF, SPATK , SPDEF, SPD)
    - then the lowered stat (HP, ATK, DEF, SPATK , SPDEF, SPD)
  - if not providing it (answering 'n'), 3 natures will be randomly chosen
    - You can pick one using 1 , 2 or 3
- Applying level up points to the pokemon. 
  - You will be asked how many points for each stats. You can provide point for each : 
    - HP
    - ATK
    - DEF
    - SPATK
    - SPDEF
    - SPEED
  - !!! Or, if you prefer to automatically apply balanced points from base stats, enter 'default' 
- Than you will be asked the list of moves for your pokemon, the code will list all move available for your pokemon level.
  - You can either : 
    - give moves one by one among the list
    - type 'default', and the code will give the last 6 learnt moves by the pokemon
- And finally you will be able to add up to 3 egg move. You will be provided no lists. Enter the move one by one, and if you want to stop at any time, enter 'stop'.


The sheet will be generated in the same folder, with the name like this :

"pokemon_name_timestamp.md"
