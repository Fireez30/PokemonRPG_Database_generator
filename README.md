# PokemonRPG_Database_generator
This repository contains code for generation of a Json base of the pokemon extracted from our RPG documentation

Install :

python -m venv my_env 
pip install pymupdf


Usage : 

Edit the code to change the path to the new pdf file to parse
Change the skip_pages_to index to avoid reading non pokedex pages
change output path

than activate environement :

For fish : 

source my_env/bin/activate.fish

for other shells :

source my_env/bin/activate

than you can start the code:

python extract_database.py


TODO : 

- Parsing of gen 9 
- for parsing gen7/8 and 9  : find all moves with "-", and replace it by "&" before parse, and replace "&"->"-" after
- for parsing gen 9 : update stats to aggregate and do post processing