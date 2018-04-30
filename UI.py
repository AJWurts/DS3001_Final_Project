# Written by Alexander Wurts
# Data Science 3001 Final Project

from tkinter import *
from model.map import Map
from model.datahandler import DataHandler
from view.selectorcanvas import SelectionCanvas



class GUI:

    WIDTH = 1500
    HEIGHT = 1024

    SIDES = [("Terrorist", 'Terrorist'),
             ("Counter Terrorist", "CounterTerrorist"),
             ('Both', "Both")]



    def __init__(self):
        self.root = Tk()
        self.root.geometry(str(GUI.WIDTH) + 'x' + str(GUI.HEIGHT))


        self.data = DataHandler()
        self.mainFrame = Frame(self.root)
        self.mainFrame.pack(side=LEFT, fill=BOTH, expand=True)


        self.currentFilter = DataHandler.EMPTY_FILTER

        self.mainscene()
        self.root.mainloop()


    def mainscene(self):

        def reload():
            # Box on Map Handler
            box = self.canvas.getBox()
            self.currentFilter = DataHandler.EMPTY_FILTER
            if box is not None:
                self.currentFilter['box'] = box
            else:
                self.currentFilter['box'] = None

            if boxAroundVar.get() == 'Attacker':
                self.currentFilter['box_around'] = 'Attacker'
            else:
                self.currentFilter['box_around'] = 'Victim'


            # Map Selector
            self.canvas.setMap(Map(currentMap.get()))
            self.currentFilter['map'] = "'" + currentMap.get() + "'"

            # Attack Side Selector
            if attSideVar.get() == "Both":
                self.currentFilter['att_side'] = None
            else:
                self.currentFilter['att_side'] = "'" + attSideVar.get() + "'"

            # Victim Side Selector
            if vicSideVar.get() == "Both":
                self.currentFilter['vic_side'] = None
            else:
                self.currentFilter['vic_side'] = "'" + vicSideVar.get() + "'"

            # User ID Entry
            if idEntry.get() != 'None':
                self.currentFilter['att_id'] = int(idEntry.get())
            else:
                self.currentFilter['att_id'] = None

            # Weapon Selection
            if weaponVar.get() != 'All':
                self.currentFilter['wp'] = "'" + weaponVar.get() + "'"
            else:
                self.currentFilter['wp'] = None

            for key, data in enumerate(vicAndAttRankRange):
                if data.get() != '':
                    self.currentFilter['player_rank_range'][key] = int(data.get())
                else:
                    # if key is an odd number set value to 18, else even set 0
                    self.currentFilter['player_rank_range'][key] = 18 * (key % 2)


            self.canvas.addData(self.data.applyFilter(self.currentFilter))
            self.canvas.reloadImage()


        self.topFrame = Frame(self.mainFrame)
        self.topFrame.grid(column=1, row=0)

        ## Side Bar Configuration
        Button(self.topFrame, text='Reload', command=reload).grid(column=1, row=0)


        # Map Dropdown
        currentMap = StringVar(self.topFrame)
        currentMap.set(Map.MAPS[2])
        mapSelector = OptionMenu(self.topFrame, currentMap, *Map.MAPS)
        mapSelector.grid(column=1, row=1)
        Label(self.topFrame, text="Map: ").grid(row=1, column=0)

        # Att Side
        Label(self.topFrame, text="Attacker Side: ").grid(row=2, column=0)
        attSideFrame = Frame(self.topFrame)
        attSideFrame.grid(row=2, column=1)
        attSideVar = StringVar()
        attSideVar.set("Both")
        for side in GUI.SIDES:
            b = Radiobutton(attSideFrame, text=side[0], variable=attSideVar, value=side[1])
            b.pack(anchor=W)

        # Vic Side
        Label(self.topFrame, text="Victim Side: ").grid(row=3, column=0)
        vicSideFrame = Frame(self.topFrame)
        vicSideFrame.grid(row=3, column=1)
        vicSideVar = StringVar()
        vicSideVar.set("Both")
        for side in GUI.SIDES:
            b = Radiobutton(vicSideFrame, text=side[0], variable=vicSideVar, value=side[1])
            b.pack(anchor=W)

        # Att ID
        Label(self.topFrame, text="Attacker ID (Type None for all players): ").grid(row=4, column=0)
        idEntryVar = StringVar()
        idEntryVar.set("None")
        idEntry = Entry(self.topFrame, textvariable=idEntryVar)
        idEntry.grid(row=4, column=1)

        # Victim and Attacker Rank Ranges
        labels = ['Min Attacker Rank: ', 'Max Attacker Rank: ', "Min Victim Rank: ", "Max Victim Rank"]
        vicAndAttRankRange = []
        Label(self.topFrame, text="Attacker and Victim Rank (1-18, lower is better): ").grid(row=5, columnspan=2)
        for key, label in enumerate(labels):
            Label(self.topFrame, text=label).grid(row=6 + key, column=0)
            vicAndAttRankRange.append(Entry(self.topFrame))
            vicAndAttRankRange[-1].grid(row=6 + key, column=1)


        # Weapon
        weapons = ['All', 'USP', 'Glock', 'P2000', 'HE', 'Tec9', 'Deagle', 'MP9', 'UMP',
           'Famas', 'P250', 'AK47', 'AWP', 'MP7', 'M4A1', 'FiveSeven',
           'Incendiary', 'Scout', 'Unknown', 'Knife', 'Bizon', 'Flash', 'CZ',
           'M4A4', 'Molotov', 'P90', 'AUG', 'Gallil', 'G3SG1', 'M249', 'SG556',
           'Mac10', 'XM1014', 'DualBarettas', 'Nova', 'Swag7', 'Zeus',
           'Scar20', 'SawedOff', 'Smoke', 'Negev', 'Decoy', 'Bomb']
        weaponVar = StringVar(self.topFrame)
        weaponVar.set("AK47")
        weaponSelector = OptionMenu(self.topFrame, weaponVar, *weapons)
        weaponSelector.grid(row=10, column=1)
        Label(self.topFrame, text="Weapon: ").grid(row=10, column=0)


        # Box around attacker or victim
        Label(self.topFrame, text="Box Around:  ").grid(row=11, column=0)
        boxAroundFrame = Frame(self.topFrame)
        boxAroundFrame.grid(row=11, column=1)
        boxAroundVar = StringVar()
        boxAroundVar.set("Both")
        for side in ['Victim', 'Attacker']:
            b = Radiobutton(boxAroundFrame, text=side, variable=boxAroundVar, value=side)
            b.pack(anchor=W)

        self.canvas = SelectionCanvas(self.mainFrame, width=1024, height=1024)
        self.canvas.grid(column=0, row=0, stick=W)
        self.canvas.focus_force()

        self.canvas.addData(self.data.applyFilter(DataHandler.EMPTY_FILTER))
        self.canvas.reloadImage()





GUI()
