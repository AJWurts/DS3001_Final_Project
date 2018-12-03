# Written by Alexander Wurts
import pandas as pd




class DataHandler:

    EMPTY_FILTER = {'map': "'de_dust2'", 'att_side': None, 'vic_side': None,
                    'att_rank': None, 'player_rank_range': [0, 18, 0, 18], 'att_id': None, 'wp': "'AK47'",
                    'box': None, 'box_around': 'Attacker'}

    def __init__(self):
        self.data = pd.read_csv('mm_master_demos.csv')

    def getData(self):
        return self.data

    def getEmptyFilter(self):
        return DataHandler.EMPTY_FILTER

    def makeFilterString(self, filter):
        out = "att_id!=0 and wp_type!='grenade' and "
        # Converting all basic filters to pands format
        for key in filter.keys():
            if key == 'box' or key == 'player_rank_range' or key == 'box_around':
                continue
            if filter[key] != None:
                out += '(' + str(key) + "==" + str(filter[key]) + ")" + ' and '

        # For Victim and Attacker Rank Range
        data = filter['player_rank_range']
        out += '((att_rank>=%d) and (att_rank<=%d) and (vic_rank>=%d) and (vic_rank<=%d)) and ' \
                % (data[0], data[1], data[2], data[3])

        # Box Converting to Pandas Filter
        if filter['box'] != None:
            box = filter['box']
            minX = min(box[0], box[2])
            maxX = max(box[0], box[2])
            minY = min(box[1], box[3])
            maxY = max(box[1], box[3])
            if filter['box_around'] == "Attacker":
                out += "((att_pos_x>%d) and (att_pos_y>%d) and (att_pos_x<%d) and (att_pos_y<%d))" \
                       % (minX, minY, maxX, maxY)
            else:
                out += "((vic_pos_x>%d) and (vic_pos_y>%d) and (vic_pos_x<%d) and (vic_pos_y<%d))" \
                       % (minX, minY, maxX, maxY)
        else:
            if len(out) != 0:
                out = out[:-5]



        print(out)
        return out


    def applyFilter(self, dictionary):
        filterString = self.makeFilterString(dictionary)
        return self.data.query(filterString)
