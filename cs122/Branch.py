# CS122 W'16: Treemap assignment

class Branch:

    def  __init__(self,fields):
        '''
        construct a Branch, given list of fields from an FDIC CSV file
        '''
        # column names:
        # NAMEFULL,CNTYNAMB,STALPBR,DEPSUMBR,CITY2BR,CSANAMBR,NAMEBR,BKCLASS
        # financial institution name
        # branch details:
        #  county, state, deposits at ranch (thousands of $), city,
        #  combined statistical area (CSA), name of branch
        # class of institution (national association, savings bank, etc.)
        self._data = fields[:]


    def key(self, level):
        '''
        given level of node in Deposit_Tree,
        get the attribute of this branch that should
        label the node at this level
        '''
        if level == 0:
            return self.state
        elif level == 1:
            return self.county
        elif level == 2:
            return self.city
        elif level == 3:
            return self.cls
        elif level == 4:
            return self.branchname
        else:
            print("Levels of hierarchy for branches only go up to 4")
            sys.exit(0)


    @property
    def cls(self):
        '''
        returns the class of the financial
        institution the branch belongs to
        '''
        return self._data[7]


    @property
    def branchname(self):
        '''
        returns the branch's individual branch name
        (e.g. "Hyde Park Branch"
        '''
        return self._data[6]


    @property
    def instname(self):
        '''
        returns the name of the financial institution to which the branch
        belongs
        '''
        return self._data[0]


    @property
    def state(self):
        '''
        returns the state in which this branch is located
        '''
        return self._data[2]


    @property
    def county(self):
        '''
        returns the county in which this branch is located
        '''
        return self._data[1]


    @property
    def city(self):
        '''
        returns the city in which this branch is located
        '''
        return self._data[4]


    @property
    def deposits(self):
        '''
        get the deposits at the branch
        '''
        return float(self._data[3])


    @property
    def label(self):
        '''
        get the label for the branch
        '''
        return ("$" + str(self.deposits) + "k  " + self.instname + " (" +
                self.city + ", " + self.county + ", " + self.state + ") " +
                self.branchname)

