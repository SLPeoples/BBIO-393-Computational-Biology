"""
Write a new class that represents the nodes in a phylogentic tree. Each node should know:
Name, Children, Parents, Traits, (Should have branch length, but we will ignore for now)
"""
class TreeNode(object):
    """
    A node in a phylogenetic tree
    Each node will have a name, traits, children, and parent
    """
    def __init__(self, name, traits=None, children=None, parent=None):
        self.name = name
        self.traits = traits
        self.children = children
        self.parent = parent
    def getName(self):
        return self.name
    def setParent(self, parent = None):
        self.parent = parent
    def getParent(self):
        return self.parent.getName()

treeNode1 = TreeNode("A")
treeNode2 = TreeNode("B")
print(treeNode1.getName())
treeNode1.setParent(parent=treeNode2)
print(treeNode1.getParent())

internalNode = TreeNode("AB", children = treeNode2)

