class LINK:
    def __init__(self,name,abspos,relativepos,size,colorName,rgba):
        self.name = name
        self.abspos = abspos
        self.relativepos = relativepos
        self.size = size
        self.colorName = colorName
        self.rgba = rgba

    def Compute_Box(self):
        minX = self.abspos[0] - self.size[0]/2
        maxX = self.abspos[0] + self.size[0]/2
        minY = self.abspos[1] - self.size[1]/2
        maxY = self.abspos[1] + self.size[1]/2
        minZ = self.abspos[2] - self.size[2]/2
        maxZ = self.abspos[2] + self.size[2]/2
        bounding_box = [[minX,maxX],
                        [minY,maxY],
                        [minZ,maxZ]]
        return bounding_box


