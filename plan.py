import numpy as np
import constants as c
from links import LINK
from joint import JOINT
import random

class PLAN:
    def __init__(self):
        self.links = []
        self.joints = []

        self.boolArray = np.random.randint(2, size=c.numLinks + 1)
        self.linkID = 0
        self.jointID = 0

    def Get_Vec_From_Center(self, face, size):
        if face == 0:
            return np.array([size[0]/-2, 0, 0])
        elif face == 1:
            return np.array([0, 0, size[2]/2])
        elif face == 2:
            return np.array([size[0]/2, 0, 0])
        elif face == 3:
            return np.array([0, 0, size[2] / -2])
        elif face == 4:
            return np.array([0, size[1]/-2, 0])
        elif face == 5:
            return np.array([0, size[1]/2, 0])
        else:
            return np.array([0,0,0])

    def Find_Collisions(self, links, new):
        new_box = new.Compute_Box()
        bool = False
        for i in range(len(links)-2):
            link_box = links[i].Compute_Box()
            if new_box[0][0] < link_box[0][1] and new_box[0][1] > link_box[0][0] and new_box[1][0] < link_box[1][1] \
                    and new_box[1][1] > link_box[1][0] and new_box[2][0] < link_box[2][1] \
                    and new_box[2][1] > link_box[2][0] and new_box[2][0] < 0:
                return True
            else:
                bool = False
        return bool

    def Get_Plan(self):
        count = 0
        headsize = np.random.rand(3)*1.5 + 0.5
        print(c.numLinks)
        if self.boolArray[0] == 1:
            rgba = '    <color rgba="0 1.0 0 1.0"/>'
            colorName = '<material name="Green">'
        else:
            rgba = '    <color rgba="0 0 1.0 1.0"/>'
            colorName = '<material name="Blue">'
        self.links.append(LINK(name="Head", abspos=np.array([0,0,1]),relativepos=np.array([0,0,0]), size=headsize,
                                       colorName=colorName, rgba=rgba))
        body0face = random.choice(range(6))
        body0jointvec = self.Get_Vec_From_Center(body0face, headsize)
        self.joints.append(JOINT(name=f"Head_Body0",parent="Head", child=f"Body0",
                                          jointtype="revolute", axis='0 1 0', pos=body0jointvec + np.array([0,0,1]),
                                 prevface=body0face))
        for i in range(c.numLinks):
            nextface = random.choice(range(6))
            randomLink = random.randint(0,count)
            prevDirection = self.joints[randomLink].prevface
            prevSize = self.links[randomLink].size
            prevPos = self.links[randomLink].abspos
            prevJointPos = self.joints[randomLink].position
            bodySize = np.random.rand(3)*1.5 + 0.5
            vecToCenter = self.Get_Vec_From_Center(prevDirection, bodySize)
            centerToJoint = self.Get_Vec_From_Center(prevDirection, prevSize)
            nextlinkVec = self.Get_Vec_From_Center(nextface,bodySize)
            abspos = prevPos+centerToJoint+vecToCenter
            if randomLink == 0:
                abspos = np.array([0,0,1]) + vecToCenter

            if self.boolArray[i+1] == 1:
                rgba = '    <color rgba="0 1.0 0 1.0"/>'
                colorName = '<material name="Green">'
            else:
                rgba = '    <color rgba="0 0 1.0 1.0"/>'
                colorName = '<material name="Blue">'
            print(f'Body{count}')
            self.links.append(LINK(name=f"Body{count}", abspos=abspos,
                                   relativepos=vecToCenter, size=bodySize, colorName=colorName, rgba=rgba))
            count += 1
            while True:
                if self.Find_Collisions(self.links, self.links[len(self.links)-1]):
                    self.links.pop()
                    count += -1
                    print(count)
                    randomLink = random.randint(0,count)
                    prevPos = self.links[randomLink].abspos
                    prevSize = self.links[randomLink].size
                    prevDirection = self.joints[randomLink].prevface
                    bodySize = np.random.rand(3) * 1.5 + 0.5
                    centerToJoint = self.Get_Vec_From_Center(prevDirection, prevSize)
                    vecToCenter = self.Get_Vec_From_Center(prevDirection, bodySize)

                    self.links.append(LINK(name=f"Body{count}", abspos=prevPos+centerToJoint+vecToCenter,
                                           relativepos=vecToCenter,size=bodySize, colorName=colorName,rgba=rgba))
                    count += 1
                else:
                    break
            if i + 1 < c.numLinks:
                print(f'Body{count}_Body{count+1}')
                self.joints.append(JOINT(name=f"Body{count-1}_Body{count}",parent=f"Body{count-1}", child=f"Body{count}",
                                                  jointtype="revolute", axis='0 1 0', pos=vecToCenter+nextlinkVec,
                                         prevface=prevDirection))

        return self.links, self.joints


