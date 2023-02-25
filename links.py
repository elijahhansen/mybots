import numpy as np
class LINK:
    def __init__(self,linkID,pos,absJointpos,size,colorBool):
        self.linkID = linkID
        self.name = f"Body{linkID}"
        self.pos = pos
        self.absJointpos = absJointpos
        self.size = size
        self.colorBool = colorBool
        self.abspos, self.box = self.Compute_Box()
        if colorBool:
            self.rgba = '    <color rgba="0 1.0 0 1.0"/>'
            self.colorName = '<material name="Green">'
        else:
            self.rgba = '    <color rgba="0 0 1.0 1.0"/>'
            self.colorName = '<material name="Blue">'

    def Compute_Box(self):
        if self.linkID == 0:
            absolutePosition = [0, 0, 2]
        else:
            posRelToJoint = np.copy(self.pos)
            for i in range(len(posRelToJoint)):
                if posRelToJoint[i] < 0:
                    posRelToJoint[i] = self.size[i] / -2
                elif posRelToJoint[i] > 0:
                    posRelToJoint[i] = self.size[i] / 2
            absolutePosition = np.add(posRelToJoint, self.absJointpos)
        minX = absolutePosition[0] - self.size[0]/2
        maxX = absolutePosition[0] + self.size[0]/2
        minY = absolutePosition[1] - self.size[1]/2
        maxY = absolutePosition[1] + self.size[1]/2
        minZ = absolutePosition[2] - self.size[2]/2
        maxZ = absolutePosition[2] + self.size[2]/2
        bounding_box = [[minX,maxX],
                        [minY,maxY],
                        [minZ,maxZ]]
        return absolutePosition, bounding_box

    def __str__(self):
        return f"LINK{self.name}, abspos={self.abspos},pos={self.pos}"


