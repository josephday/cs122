# CS122 W'16: Treemap assignment

# IMPORTANT: You do not need to understand how this code works to use the
#  Deposit Tree class.

import sys
import csv
import Branch

class Deposit_Tree:

    ROOT=-1
    STATE=0
    COUNTY=1
    CITY=2
    CLASS=3
    BRANCH=4

    LOW_LEVEL=CLASS


    def __init__(self,my_name="root", my_level=-1, my_branch=None,
                 filename=None):
        '''
        construct a new deposit tree from data in file filename
        or, construct a node, filling in each of the fields as given
        (indicate which to do by either providing fields or a filename)
        '''
        self._children = {}
        self._final_children = []
        self._name = my_name
        self._level = my_level
        self._weight = 0

        if my_level != Deposit_Tree.BRANCH and my_branch != None:
            print("Cannot specify a branch for an interior node")
            sys.exit(0)
        self._branch = my_branch

        if my_level == Deposit_Tree.ROOT:
           if filename == None:
               print("Must supply a filename to construct a Deposit Tree")
               sys.exit(0)
           self.load_from_file(filename)


    def load_from_file(self,filename):
        '''
        create a new dposit tree from given file filename
        '''
        with open(filename, 'rU') as csvfile:
            reader = csv.reader(csvfile)
            for fields in reader:
                b = Branch.Branch(fields)
                self.add(b)


    def add(self, b):
        '''
        add branch b to tree
        '''
        if self._level == Deposit_Tree.LOW_LEVEL:
           dt = Deposit_Tree(my_name = b.branchname,
                             my_level = Deposit_Tree.BRANCH, my_branch=b)
           self._children[b.branchname] = dt
           return

        name = b.key(self._level+1)
        if name not in self._children:
           dt = Deposit_Tree(my_name=name, my_level=self._level+1)
           self._children[name] = dt
        dt = self._children[name]
        dt.add(b)


    def compute_children(self):
        if self._children == None:
            # leaf node
            return

        # interior node
        items = sorted(self._children.items())
        for (key, kid) in items:
            kid.compute_children()
            self._final_children.append(kid)
    

    @property
    def children(self):
        '''
        return a list with the tree's children
        '''
        kids = []
        items = sorted(self._children.items())
        for (key, kid) in items:
            kids.append(kid)
        return kids


    @property
    def label(self):
        '''
        get the label of this node
        '''
        return self._name


    @property
    def branch(self):
        '''
        get the branch associated with the tree.
        will be None unless the tree is a leaf
        '''
        return self._branch


    @property
    def weight(self):
        '''
        get the tree's weight
        '''
        return self._weight


    def set_weight(self, w):
        '''
        set the tree's weight
        '''
        self._weight = w


    def is_branch_node(self):
        '''
        return true if the tree is a leaf, and false otherwise.
        '''
        return self._branch != None


    def is_leaf_node(self):
        '''
        return true if the tree is a leaf, and false otherwise.
        '''
        return self.is_branch_node()


    def get_subtree(self, l):
        '''
        traverse the tree finding subsequent nodes with values in list l
        '''
        if l == []:
            return self
        for val in l:
            if val in self._children:
                sub = self._children[val]
                return sub.get_subtree(l[1:])
            else:
                print("could not find subtree with value: " + val)
                return None


    def print_tree(self, tabs=""):
        '''
        print the tree to screen; can specify indentation in tabs
        '''
        if self._branch != None:
            print(tabs + self._branch.label)
        else:
            print(tabs + self._name + "  " + str(self._weight))
            for k in self.children:
                k.print_tree(tabs=tabs+"  ")

        
    
