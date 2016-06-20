# CS122 W'16: Markov models and hash tables
# Joseph Day 


TOO_FULL = 0.5
GROWTH_RATIO = 2

def hash_function(key, cells):
    total = 0
    assert type(key) is str
    for character in key:
        total += ord(character)
        total = total * 37
        total = total % cells
    return total


class Hash_Table(object):

    def __init__(self, cells, defval):
        '''
        Construct a new hash table with a fixed number of cells equal to the
        parameter "cells", and which yields the value defval upon a lookup to a
        key that has not previously been inserted
        '''
        self.cells = cells
        self.defval = defval
        self.table = [self.defval for x in range(self.cells)]
        self.occupied = 0
        self.growth_ratio = GROWTH_RATIO
        self.too_full = TOO_FULL

    
    @property
    def cells(self):
        return self.__cells

    @cells.setter
    def cells(self,value):
        self.__cells = value


    def lookup(self,key):
        '''
        Retrieve the value associated with the specified key in the hash table,
        or return the default value if it has not previously been inserted.
        '''
        hashed = hash_function(key, self.cells)
        n = 0
        while self.table[hashed] != self.defval and self.table[hashed][0] != key: 
            hashed = (hashed + 1) % self.cells
            n += 1
            if n == self.cells:
                return None 
        if self.table[hashed] == self.defval:
            return None        
        else:
            return self.table[hashed][1] 

    def update(self,key,value):
        '''
        Change the value associated with key "key" to value "val".
        If "key" is not currently present in the hash table,  insert it with
        value "val".
        '''
        hashed = hash_function(key, self.cells)  

        while self.table[hashed] != self.defval and self.table[hashed][0] != key:
            hashed = (hashed + 1) % self.cells
        if self.table[hashed] == self.defval:                   
            self.occupied += 1
        self.table[hashed] = (key,value)                   
            
        if self.occupied/self.cells > self.too_full:
            self.expand()
        else:
            pass 


    def expand(self):
        '''
        This function is triggered in update stage if table is too full.
        Changes size of hash table and rehashes all items previously stored.
        '''
        items_to_rehash = [pair for pair in self.table if pair != self.defval]
        self.cells = self.cells * self.growth_ratio
        self.table = [self.defval for x in range(self.cells)]
        self.occupied = 0
        for pair in items_to_rehash:
            self.update(pair[0], pair[1])



            
        
             
