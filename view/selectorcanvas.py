
from tkinter import *
from model.map import Map


class SelectionCanvas(Canvas):

    def __init__(self, loc, **args):
        Canvas.__init__(self, loc, args)

        self.minX = None
        self.minY = None
        self.maxX = None
        self.maxY = None
        self.box = None
        self.clickNum = 0

        self.currentImage = None
        self.canvasImage = None
        self.map = Map(Map.MAPS[2])

        self.bind('<Button-1>', self.click)


    def click(self, event):
        if self.clickNum == 0:
            self.minX = event.x
            self.minY = event.y
            self.maxX = event.x
            self.maxY = event.y
            self.clickNum += 1
            print("FIrst Click")
            self.create_rectangle(self.minX, self.minY, self.minX, self.minY, fill='', outline='red', tags='Box')

        elif self.clickNum == 1:
            print("Second Click")
            self.clickNum += 1
            self.maxX = event.x
            self.maxY = event.y
            self.delete('Box')
            self.create_rectangle(self.minX, self.minY, self.maxX, self.maxY, fill='', outline='red',
                                             tags='Box', width=3)
        else:
            print("Click 3")
            self.clickNum = 0
            self.delete('Box')
            self.minX = None

    def getBox(self):
        if self.minX != None:
            return self.map.convertBox((self.minX, self.maxY, self.maxX, self.minY))
        return None

    def reloadImage(self):
        self.currentImage = self.map.getImageTk()
        if self.canvasImage == None:
            self.canvasImage = self.create_image(512, 512, image=self.currentImage)
        else:
            self.itemconfig(self.canvasImage, image=self.currentImage)

    def clearMap(self):
        self.delete('Box')
        self.minX = None
        self.map.clear()


    def addData(self, data):
        self.map.addData(data)

    def setMap(self, newMap):
        self.map = newMap