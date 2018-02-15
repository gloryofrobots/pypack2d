__author__ = 'human88998999877'

from PIL import Image
class Atlas(object):
    def __init__(self):
        super(Atlas,self).__init__()
        self.width = 0
        self.height = 0
        self.dirPath = None
        self.fileName = None
        self.textureMode = None
        self.atlasType = None
        self.fillColor = None

        self.canvas = None
        self.images = []
        pass

    def initialise(self, width, height, dirPath, fileName, texMode, atlasType, fillColor):
        self.width = width
        self.height = height
        self.dirPath = dirPath
        self.fileName = fileName
        self.textureMode = texMode
        self.atlasType = atlasType
        self.fillColor = fillColor
        pass

    def addImage(self, image):
        self.images.append(image)
        return True
        pass

    def getCanvas(self):
        return self.canvas
        pass

    def save(self):
        path = self.dirPath + "\\" + self.fileName
        self.canvas.save(path, self.atlasType)
        pass

    def show(self):
        self.canvas.show()
        pass

    def pack(self):
        self.canvas = Image.new(self.textureMode, (self.width, self.height), self.fillColor)
        for img in self.images:
            img.pack(self)
            pass
        pass
    pass