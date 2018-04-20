import numpy as np
import pandas as pd
from model import map
import matplotlib.pyplot as plt
# File Columns
# file
# map
# date
# roundtick
# seconds
# att_team
# vic_team
# att_side
# vic_side
# hp_dmg
# arm_dmg
# is_bomb_planted
# bomb_site
# hitbox
# wp
# wp_type
# award
# winner_team
# winner_side
# att_id
# att_rank
# vic_id
# vic_rank
# att_pos_x
# att_pos_y
# vic_pos_x
# vic_pos_y
# round_type
# ct_eq_val
# t_eq_val
# avg_match_rank


#2127,3455,1024,1024,-2486,-1150

de_dust2 = map.Map(2127,3455,-2486,-1150, 'de_dust2.png')

data = pd.read_csv("mm_master_demos.csv")
#

# Data Analysis then Display onto Map
# Filters data down to Headshots from AWP (A weapon in the game)
if True:
    dust_map = map.Map(2127, 3455, -2486, -1150, 'de_dust2.png')
    top_players = [76561198023317027]
    player_id = top_players[0]
    filtered_data = data[(data.map == 'de_dust2')
                         & ((data.att_id == player_id))]

    filtered = filtered_data.filter(items=["att_pos_x", "att_pos_y", "vic_pos_x", "vic_pos_y", 'att_side'])

    for line in filtered.as_matrix():
        dust_map.drawShot(line[0], line[1], line[2], line[3], line[4])
    dust_map.show()
    dust_map.save("Deagle_Dust2_Attack" + str(player_id) + "_Analysis.jpg")



# Disconnected Side Analysis
if False: # Toggle
    sides = ['CounterTerrorist', 'Terrorist']
    for side in sides:
        dust_map = map.Map(2127,3455,-2486,-1150, 'de_dust2.png')
        filtered_data = data[(data.map == 'de_dust2')
                                 & (data.att_side == side)
                                # & ((data.att_id == player_id)
                                # | (data.vic_id == player_id))]
                                # (data.file == '003201673717864202280_0171883906.dem')]
                                & (data.hp_dmg == 100)
                                # & (data.att_id == 0)]
                                & (data.wp == 'Deagle')]
        filtered = filtered_data.filter(items=["att_pos_x", "att_pos_y", "vic_pos_x", "vic_pos_y", 'att_side'])

        for line in filtered.as_matrix():
            dust_map.drawShot(line[0], line[1], line[2], line[3], line[4])
        dust_map.show()
        dust_map.save("Deagle_Dust2_" + side + "_Analysis.jpg")

# # Team Kills
# data = data[(data.map == 'de_dust2')
#             & (((data.att_side == 'Terrorist') & (data.vic_side == "Terrorist"))
#                 | ((data.att_side == 'CounterTerrorist') & (data.vic_side == 'CounterTerrorist')))]


# Plotting on Map



# Unique Player Analysis
# player_id = data.filter(items=['att_id', 'vic_id']).as_matrix()
# all_ids = []
# for line in player_id:
#     all_ids.append(line[0])
#     all_ids.append(line[1])
# unique, counts = np.unique(all_ids, return_counts=True)
# zipped = [(unique[i], counts[i]) for i in range(len(unique))]
# zipped.sort(key=lambda x: x[1] , reverse=True)
#


