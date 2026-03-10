source my_env/bin/activate.fish
python extract_move_database.py data/Moves.html -o move.csv
python extract_abilities_database.py
python extract_pokemon_database.py
python extractRedux.py
python generate_poke_pdf.py