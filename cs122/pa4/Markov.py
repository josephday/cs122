# CS122 W'16: Markov models and hash tables
# Joseph Day

import sys
import math
import Hash_Table

HASH_CELLS = 57

class Markov:

    def __init__(self,k,s):
        '''
        Construct a new k-order Markov model using the statistics of string "s"
        '''
        self.k = k
        self.alphabet = len(set(s))
        self.length = len(s)
        self.k_table = Hash_Table.Hash_Table(HASH_CELLS, None)
        self.kplus1_table = Hash_Table.Hash_Table(HASH_CELLS, None)
        
        for index in range(k+1, len(s)+k+1):
            to_hash = (s+s)[index-(k+1):index]
            
            lookup = self.k_table.lookup(to_hash[0:k])
            
            if lookup == None:
                self.k_table.update(to_hash[0:k], 1)
            else:
                self.k_table.update(to_hash[0:k],lookup + 1)   
            
            lookup2 = self.kplus1_table.lookup(to_hash)

            if lookup2 == None:
                self.kplus1_table.update(to_hash, 1)
            else:
                self.kplus1_table.update(to_hash,lookup2 + 1)


    def log_probability(self,s):
        '''
        Get the log probability of string "s", given the statistics of
        character sequences modeled by this particular Markov model
        '''        
        if len(s)-1 == self.k:
            M = self.kplus1_table.lookup(s)
            N = self.k_table.lookup(s[0:self.k])
            S = self.alphabet
            if type(M) != int:
                M = 0
            if type(N) != int:
                N = 0
            return float(math.log((M+1)/(N+S)))
        else:
            return 0


    def total_string_probability(self, new_s):
        '''
        Given a new_s, calculate total normalized log probability of 
        this string having been said by speaker of training string for this Markov
        '''
        totalprob = 0
        k = self.k
        for index in range(0, self.length+2*(k+1)):
            to_hash = (new_s + new_s[0:k+1])[index:index+k+1]
            #print(to_hash)
            totalprob += self.log_probability(to_hash)
        totalprob = totalprob / (len(new_s))
        return totalprob


def identify_speaker(speech1, speech2, speech3, order):
    '''
    Given sample text from two speakers, and text from an unidentified speaker,
    return a tuple with the normalized log probabilities of each of the speakers
    uttering that text under a "order" order character-based Markov model,
    and a conclusion of which speaker uttered the unidentified text
    based on the two probabilities.
    '''
    test1 = Markov(order, speech1)
    test2 = Markov(order, speech2)
    probability1 = test1.total_string_probability(speech3)
    probability2 = test2.total_string_probability(speech3)

    if probability1 > probability2:
        conclusion = 'A'
    else:
        conclusion = 'B'

    return (probability1, probability2, conclusion)

    
def print_results(res_tuple):
    '''
    Given a tuple from identify_speaker, print formatted results to the screen
    '''
    (likelihood1, likelihood2, conclusion) = res_tuple
    
    print("Speaker A: " + str(likelihood1))
    print("Speaker B: " + str(likelihood2))

    print("")

    print("Conclusion: Speaker " + conclusion + " is most likely")


if __name__=="__main__":
    num_args = len(sys.argv)

    if num_args != 5:
        print("usage: python3 " + sys.argv[0] + " <file name for speaker A> " +
              "<file name for speaker B>\n  <file name of text to identify> " +
              "<order>")
        sys.exit(0)
    
    with open(sys.argv[1], "rU") as file1:
        speech1 = file1.read()

    with open(sys.argv[2], "rU") as file2:
        speech2 = file2.read()

    with open(sys.argv[3], "rU") as file3:
        speech3 = file3.read()

    res_tuple = identify_speaker(speech1, speech2, speech3, int(sys.argv[4]))

    print_results(res_tuple)

