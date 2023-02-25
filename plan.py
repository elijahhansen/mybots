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

    def Make_Blueprint(self):
        self.Make_Base_Link()
        for i in range(c.numLinks):
            self.Create_Link_Joint()
        return self.links, self.joints


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
        new_box = new.Compute_Box()[1]
        bool = False
        for i in range(len(links)-1):
            link_box = links[i].Compute_Box()[1]
            if (new_box[0][0] < link_box[0][1] and new_box[0][1] > link_box[0][0] and new_box[1][0] < link_box[1][1]
                    and new_box[1][1] > link_box[1][0] and new_box[2][0] < link_box[2][1]
                    and new_box[2][1] > link_box[2][0]) or new_box[2][0] < 0:
                return True
            else:
                bool = False
        return bool

    def Make_Base_Link(self):
        pos = np.array([0,0,2])
        size = np.random.rand(3)*1.25 + 0.5
        self.links.append(LINK(linkID=self.linkID,pos=pos,absJointpos=np.array([0,0,0]),size=size,
                               colorBool=self.boolArray[self.linkID] == 1))
        self.linkID += 1

    def Create_Link(self,absJointPos,nextface):
        size = np.random.rand(3)*1.25 + 0.5
        direction = nextface
        posvector = self.Get_Vec_From_Center(direction,size)
        self.links.append(LINK(linkID=self.linkID,pos=posvector,absJointpos=absJointPos,size=size,
                               colorBool=self.boolArray[self.linkID] == 1))
        self.linkID += 1

    def Create_Link_Joint(self):
        while True:
            parentID = np.random.randint(len(self.links))
            absLinkPos = self.links[parentID].abspos
            nextface = np.random.randint(6)
            vec = self.Get_Vec_From_Center(nextface,self.links[parentID].size)
            absjointpos = np.add(absLinkPos, vec)
            reljointpos = np.subtract(absjointpos,self.links[parentID].absJointpos)
            self.joints.append(JOINT(parent=parentID,child=self.linkID,jointtype="revolute",axis='0 1 0',
                                     pos=reljointpos))
            self.Create_Link(absJointPos=absjointpos,nextface=nextface)

            if self.Find_Collisions(self.links, self.links[len(self.links)-1]):
                self.joints.pop()
                self.links.pop()
                self.linkID -= 1
            else:
                break


"""

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
        self.links.append(LINK(name="Body0", abspos=np.array([0,0,2]),relativepos=np.array([0,0,0]), size=headsize,
                                       colorName=colorName, rgba=rgba))
        count += 1
        body0face = random.choice(range(1))
        body0jointvec = self.Get_Vec_From_Center(body0face, headsize)
        self.joints.append(JOINT(parent=0, child=1,
                                          jointtype="revolute", axis='0 1 0', pos=body0jointvec + np.array([0,0,2]),
                                 prevface=body0face))
        for i in range(c.numLinks):
            nextface = random.choice(range(1))
            randomLink = random.randint(0,count-1)
            print(count-1)
            prevDirection = self.joints[randomLink].prevface
            prevSize = self.links[randomLink].size
            prevPos = self.links[randomLink].abspos
            prevJointPos = self.joints[randomLink].position
            bodySize = np.random.rand(3)*1.5 + 0.5
            vecToCenter = self.Get_Vec_From_Center(prevDirection, bodySize)
            jointToCenter = self.Get_Vec_From_Center(prevDirection, prevSize)
            print(jointToCenter)
            nextlinkVec = self.Get_Vec_From_Center(nextface,bodySize)
            centerToJoint = self.Get_Vec_From_Center(nextface,prevSize)
            abspos = prevPos+centerToJoint+nextlinkVec
            nextJointPos = jointToCenter + centerToJoint
            print(nextJointPos)
            if randomLink == 0:
                nextJointPos = np.array([0,0,2]) + centerToJoint

            if self.boolArray[i+1] == 1:
                rgba = '    <color rgba="0 1.0 0 1.0"/>'
                colorName = '<material name="Green">'
            else:
                rgba = '    <color rgba="0 0 1.0 1.0"/>'
                colorName = '<material name="Blue">'
            print(f'Body{count}')
            self.links.append(LINK(name=f"Body{count}", abspos=abspos,
                                   relativepos=nextlinkVec, size=bodySize, colorName=colorName, rgba=rgba))
            count += 1
            while True:
                if self.Find_Collisions(self.links, self.links[len(self.links)-1]):
                    self.links.pop()
                    count += -1
                    print(count)
                    randomLink = random.randint(0,count-1)
                    nextface = random.choice(range(1))
                    prevPos = self.links[randomLink].abspos
                    prevSize = self.links[randomLink].size
                    prevDirection = self.joints[randomLink].prevface
                    bodySize = np.random.rand(3) * 1.5 + 0.5
                    centerToJoint = self.Get_Vec_From_Center(nextface,prevSize)
                    jointToCenter = self.Get_Vec_From_Center(prevDirection, prevSize)
                    vecToCenter = self.Get_Vec_From_Center(prevDirection, bodySize)
                    nextlinkVec = self.Get_Vec_From_Center(nextface, bodySize)
                    abspos = prevPos + centerToJoint + nextlinkVec
                    nextJointPos = jointToCenter + centerToJoint
                    if randomLink == 0:
                        nextJointPos = np.array([0, 0, 2]) + centerToJoint

                    self.links.append(LINK(name=f"Body{count}", abspos=abspos,
                                           relativepos=nextlinkVec,size=bodySize, colorName=colorName,rgba=rgba))
                    count += 1
                else:
                    break
            if i + 1 < c.numLinks:
                self.joints.append(JOINT(parent=randomLink, child=count,
                                                  jointtype="revolute", axis='0 1 0', pos=nextJointPos,
                                         prevface=nextface))

        return self.links, self.joints

"""
