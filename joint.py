class JOINT:
    def __init__(self,parent,child,jointtype,axis,pos):
        self.name = f"Body{parent}_Body{child}"
        self.parent = f"Body{parent}"
        self.parentID = parent
        self.childID = child
        self.child = f"Body{child}"
        self.jointtype = jointtype
        self.axis = axis
        self.position = pos

    def __str__(self):
        return f"name={self.name}, position={self.position}"