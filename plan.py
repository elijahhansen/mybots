import copy

import numpy as np
import constants as c
from links import LINK
from joint import JOINT
import random

class PLAN:
    def __init__(self):
        self.links = []
        self.joints = []
        self.boolArray = np.random.randint(2, size=c.numLinks + 2)
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
                    and new_box[2][1] > link_box[2][0]) or new_box[2][0] < 0 or new_box[2][1] > 4:
                return True
            else:
                bool = False
        return bool

    def Calculate_Absolute_Pos(self, links, joints):
        for i in range(len(links)):
            if i == 0:
                links[i].absJointPos = [0,0,0]
                links[i].abspos, links[i].box = links[i].Compute_Box()
            else:
                upstreamLink = links[joints[i-1].parentID]
                upstreamJointPos = upstreamLink.absJointpos
                absJointPos = np.add(upstreamJointPos, joints[i-1].position)
                links[i].absJointPos = absJointPos
                links[i].abspos, links[i].box = links[i].Compute_Box()

    def Mutate_Dimension(self,linkID,randomDim):
        linksCopy = copy.deepcopy(self.links)
        jointsCopy = copy.deepcopy(self.joints)
        for i in range(5):
            #each dimension has 33% chance of being mutated
            randomSize = np.random.random()*1.25 + 0.6
            prevSize = linksCopy[linkID].size
            linksCopy[linkID].size[randomDim] = randomSize
            vecChange = np.subtract(linksCopy[linkID].size, prevSize) * 0.5
            linksCopy[linkID].pos = np.add(linksCopy[linkID].pos, vecChange)
            for joint in jointsCopy:
                if joint.parent == linksCopy[linkID].name and joint.position[randomDim] != 0:
                    joint.position = np.add(joint.position, vecChange)

            self.Calculate_Absolute_Pos(linksCopy,jointsCopy)
            for link in linksCopy:
                if self.Find_Collisions(linksCopy, link):
                    collided = True
                else:
                    continue

            if collided == True:
                continue
            else:
                self.links = copy.deepcopy(linksCopy)
                self.joints = copy.deepcopy(jointsCopy)
                mutated = True
                break


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
