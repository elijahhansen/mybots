class JOINT:
    def __init__(self,name,parent,child,jointtype,axis,pos,prevface):
        self.name = name
        self.parent = parent
        self.child = child
        self.jointtype = jointtype
        self.axis = axis
        self.position = pos
        self.prevface = prevface