import pandas as pd
from . import test as ts
from . import player as espn

# Select player and seasons
seasons = [2022, 2023]
player_csv_index = 0

# Get player information from csv file
df = pd.read_csv("players.csv")
first = df['first_name'][player_csv_index]
last = df['last_name'][player_csv_index]
id = df['espn_id'][player_csv_index]
position = df['pos'][player_csv_index]

# Create Player Object
patrick_mahomes = espn.Player(first, last, id, position)

# Add Seasons to Game Log
for season in seasons:
    patrick_mahomes.Set_Season(season)
    patrick_mahomes.Set_Game_Log()

# Get game log
game_log = patrick_mahomes.Get_Game_Log()

# Verify using general property tests
test = ts.test()
test.verify_espn_pull(game_log, first, last)

print(game_log)