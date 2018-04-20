from PIL import Image, ImageDraw


class Map:
    A = 220
    RED  = (255, 0, 0, A)
    GREEN = (0, 255, 0, A)
    TERRORIST = (255, 150, 0, A)
    COUNTER_TERRORIST = (0, 0, 255, A)
    CIRCLE_SIZE = 2

    def __init__(self, end_x, start_y, start_x, end_y, image_name):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.diff_x = self.start_x - end_x
        self.diff_y = self.start_y - end_y
        self.img = Image.open("de_dust2.png")
        self.draw = ImageDraw.Draw(self.img)


    def convert(self, x, y):
        x = self.start_x - x
        y = self.start_y - y

        x /= self.diff_x
        y /= self.diff_y

        return (x * 1024, y * 1024)

    def drawPoint(self, xy, color):
        xL = xy[0] - Map.CIRCLE_SIZE
        yT = xy[1] - Map.CIRCLE_SIZE
        xR = xy[0] + Map.CIRCLE_SIZE
        yB = xy[1] + Map.CIRCLE_SIZE
        self.draw.ellipse((xL, yT, xR, yB), fill=color)


    def drawShot(self, apx, apy, vpx, vpy, team):
        n_ap = self.convert(apx, apy)
        n_vp = self.convert(vpx, vpy)
        if team == 'CounterTerrorist':
            color = Map.COUNTER_TERRORIST
        else:
            color = Map.TERRORIST

        self.draw.line(n_ap + n_vp, color, width=2)  # Gray Line Between
        self.drawPoint(n_ap, Map.GREEN)
        self.drawPoint(n_vp, Map.RED)


    def show(self):
        self.img.show()
        self.img.save("de_dust2_withdata.bmp")

    def save(self, filename):
        if filename.split('.')[1].lower() == 'jpg':
            self.img.save(filename)
            return 1
        return 0