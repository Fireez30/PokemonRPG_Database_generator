source my_env/bin/activate
python extract_move_database.py data/Moves.html -o move.csv
python extractRedux_moves.py
python extract_move_ptu_csv.py