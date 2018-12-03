from PIL import Image, ImageDraw, ImageTk
from pandas import read_csv

class Map:
    A = 220
    RED               = (255, 000, 000, A)
    GREEN             = (000, 255, 000, A)
    TERRORIST         = (255, 150, 000, A)
    COUNTER_TERRORIST = (000, 000, 255, A)
    CIRCLE_SIZE = 2
    OFFSET = 10
    MAPS = ['de_cache', 'de_cbble', 'de_dust2', 'de_inferno', 'de_mirage', 'de_overpass', 'de_train']


    def __init__(self, mapName):
        self.name = mapName
        self.changeMap(mapName)
        self.loadMap()


    def loadMap(self):
        mapData = read_csv('map_data.csv')
        current = mapData[mapData.map == self.name]
        self.startX = current['StartX'].as_matrix()[0]
        self.startY = current['EndY'].as_matrix()[0]
        self.endX = current['EndX'].as_matrix()[0]
        self.endY = current['StartY'].as_matrix()[0]
        self.diffX = self.startX - self.endX
        self.diffY = self.startY - self.endY
        self.img = Image.open("maps/" + self.name + ".png")
        self.draw = ImageDraw.Draw(self.img)
        # mapData.close()

    def changeMap(self, mapName):
        try:
            self.img = Image.open("maps/" + mapName + ".png")
            self.name = mapName
            self.loadMap()
        except Exception as e:
            print("Map Not Found")

    def convertRealToImg(self, x, y):
        x = self.startX - x
        y = self.startY - y

        x /= self.diffX
        y /= self.diffY

        return x * 1024, y * 1024

    def convertImgToReal(self, x, y):
        x /= 1024
        y /= 1024

        x *= self.diffX
        y *= self.diffY

        return self.startX - x, self.startY - y

    def convertBox(self, box):
        # (x1, y1, x2, y2)
        newBox = self.convertImgToReal(box[0], box[1]) + \
                 self.convertImgToReal(box[2], box[3])

        return newBox


    def drawPoint(self, xy, color):
        xL = xy[0] - Map.CIRCLE_SIZE
        yT = xy[1] - Map.CIRCLE_SIZE
        xR = xy[0] + Map.CIRCLE_SIZE
        yB = xy[1] + Map.CIRCLE_SIZE
        self.draw.ellipse((xL, yT, xR, yB), fill=color)


    def drawShot(self, apx, apy, vpx, vpy, team):
        n_ap = self.convertRealToImg(apx, apy)
        n_vp = self.convertRealToImg(vpx, vpy)
        if team == 'CounterTerrorist':
            color = Map.COUNTER_TERRORIST
        else:
            color = Map.TERRORIST

        self.draw.line(n_ap + n_vp, color, width=2)  # Gray Line Between
        self.drawPoint(n_ap, Map.GREEN)
        self.drawPoint(n_vp, Map.RED)

    def addData(self, data):
        filtered = data.filter(items=["att_pos_x", "att_pos_y", "vic_pos_x", "vic_pos_y", 'att_side'])
        for line in filtered.as_matrix():
            self.drawShot(line[0], line[1], line[2], line[3], line[4])

    def getImageTk(self):
        return ImageTk.PhotoImage(self.img)

    def clear(self):
        self.img = Image.open("maps/" + self.name + ".png")
        self.draw = ImageDraw.Draw(self.img)

    def show(self):
        self.img.show()
        self.img.save("de_dust2_withdata.bmp")

    def save(self, filename):
        if filename.split('.')[1].lower() == 'jpg':
            self.img.save(filename)
            return 1
        return 0