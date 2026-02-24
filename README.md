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

- Parsing of abilities from doc, and including it in the pokemon sheets
- ask user for the list of 6 moves to include, and allow user to input the egg moves
