# CS 122 W'16: Building decision trees
#
# Joseph Day

import csv
import math
import sys
import pandas as pd

def create_values_dict(observations_subset):
    '''Given a pandas dataframe (observations_subset),
    create a dictionary called values_dict
    where keys are column names in the dataframe
    and values in dict are lists of possible values for that column name.
    '''
    values_dict = {}
    for n in range(0,len(observations_subset.columns)):
        values_dict[observations_subset.columns[n]] = list(set(observations_subset[observations_subset.columns[n]]))
        
    return values_dict


def calc_p(observations_subset, attribute, value):
    '''Given a pandas dataframe -- observations_subset,
    a column you are interested in -- attribute,
    and a possible value for that attribute -- value
    and returns the probability that an instance in the subset has
    attribute value.
    '''
    top = observations_subset[observations_subset[attribute] == value] 
    top = top.shape[0]
    bottom = observations_subset.shape[0]
    return top/bottom


def get_argmax(observations_subset, target, values_dict):
    '''
    Given a pandas dataframe -- observations_subset,
    a column you are interested in -- target,
    and the dictionary of values for that column -- values_dict
    and returns the most common value for that target attribute in the subset.
    '''
    argmax = 0
    maj_value = None
    for value in values_dict[target]:
        p = calc_p(observations_subset, target, value)
        if p > argmax:
            argmax = p
            maj_value = value
        else:
            pass
    return maj_value


def calc_gini(observations_subset, attribute, values_dict):
    '''
    Calculates the gini coefficient of an attribute
    given a pandas dataframe -- observations_subset,
    column in the dataframe -- attribute,
    and a dictionary of values -- values_dict.
    '''
    sum_term = 0
    for value in values_dict[attribute]:
        p = calc_p(observations_subset, attribute, value)
        sum_term += (p**2)
    return 1-sum_term


def calc_gain(observations_subset, split_attribute, target, values_dict):
    '''Given a pandas dataframe -- observations_subset,
    a column you are interested in -- split_attribute,
    the column you are trying to predict -- target,
    and a dictionary of values -- values_dict,
    calculates the gain of splitting on the attribute.
    '''
    first_term = calc_gini(observations_subset, target, values_dict)
    sum_term = 0
    for value in values_dict[split_attribute]:
        p = calc_p(observations_subset, split_attribute, value)
        subset = observations_subset[observations_subset[split_attribute] == value]
        if subset.shape[0] > 0:
            gini = calc_gini(subset, target, values_dict)
        else:
            gini = 0
        sum_term += p*gini
    gain = first_term - sum_term
    return gain


def calc_split_info(observations_subset, attribute, values_dict):
    '''Given a pandas dataframe -- observations_subset,
    a column you are interested in -- attribute,
    and a dictionary of possible value for that attribute -- values_dict
    and returns the split_info of splitting on that attribute.
    '''
    sum_term = 0
    for value in values_dict[attribute]:
        p = calc_p(observations_subset, attribute, value)
        if p>0:
            sum_term += (p*math.log(p))
        else:
            pass

    split_info = -1 * sum_term
    return split_info


def calc_gain_ratio(observations_subset, split_attribute, target, values_dict):
    '''Given a pandas dataframe -- observations_subset,
    a column you are interested in -- split_attribute,
    the column you are trying to predict -- target,
    and a dictionary of possible value for that attribute -- values_dict
    and returns the gain_ratio of splitting on that attribute.
    '''
    gain = calc_gain(observations_subset, split_attribute, target, values_dict)
    split_info = calc_split_info(observations_subset, split_attribute, values_dict)
    if split_info != 0:
        gain_ratio = gain/split_info
    else:
        gain_ratio = 10000000000
    return gain_ratio   


def same_condition(observations_subset, target):
    '''Given a pandas dataframe -- observations_subset,
    and the column you are trying to predict,
    returns True if all instances in observations_subset have
    the same target value, False if not.
    '''
    for index, row in observations_subset.iterrows():
        comparison = row[target]
        break

    for index, row in observations_subset.iterrows():
        if row[target] != comparison:
            return False
        else:
            pass
    return True 


def same_condition_2(observations_subset, ATTR):
    '''Given a pandas dataframe -- observations_subset,
    and a list of remaining attributes to split on -- ATTR,
    returns True if all instances in observations_subset have
    the same values for all attributes in ATTR, False if not.
    '''
    assert type(ATTR) is list

    for index,row in observations_subset.iterrows():
        comparison = row[ATTR]
        break
    for index,row in observations_subset.iterrows():
        if row[ATTR].equals(comparison):
            pass
        else:
            return False

    return True



class Node:

    def __init__(self, subset, value, final, branch = None):
        '''Initiate an instance of Node class with pandas dataframe for subset,
        value which could be split_attribute or target value, final which was used to 
        debug and tells how a node was created, and branch which tells how the node was reached. 
        '''

        self.children = []
        self.subset = subset
        self.value = value
        self.final = final
        self.branch = branch

def build_tree(observations_subset, target, ATTR, values_dict, branch = None):
    '''Hoo doogie, do we have a function here or what?
    build_tree takes in a pandas dataframe -- observations_subset,
    column you are trying to predict -- target,
    list of potential split variables -- ATTR,
    a dictionary of their possible values -- values_dict,
    and where nodes created at this recursion level came from -- branch.
    '''

    #three stopping conditions
    node = Node(observations_subset, None, None)
    if same_condition(observations_subset, target) is True:
        most = get_argmax(observations_subset, target, values_dict)
        if most == 'no':
            most = 0
        else:
            most = 1          
        node.value=most
        node.final='same_condition'
        node.branch = branch
        pass

    elif len(ATTR) == 0:
        most = get_argmax(observations_subset, target, values_dict)
        if most == 'no':
            most = 0
        else:
            most = 1
        node.value=most
        node.final='no mas attributes'
        node.branch = branch
        pass

    elif same_condition_2(observations_subset, ATTR) is True:        
        most = get_argmax(observations_subset, target, values_dict)
        if most == 'no':
            most = 0
        else:
            most = 1
        node.value=most
        node.final = 'Same 2'
        node.branch = branch
        pass
    #stopping conditions not met, time to split
    else:
        max_gain_ratio = 0        
        for attribute in ATTR:
            gain_ratio = calc_gain_ratio(observations_subset, attribute, target, values_dict)
            if gain_ratio >max_gain_ratio:
                max_gain_ratio = gain_ratio
                split_attribute = attribute            
            else:
                pass
            # if gain ratio is zero, then there is no reason to split
            if max_gain_ratio == 0:
                most = get_argmax(observations_subset, target, values_dict)
                if most == 'no':
                    most = 0
                else:
                    most = 1
                node.value=most
                node.final = 'Same 2'
                node.branch = branch
                return
            # if not, get ready to split
            else:
                node.value = split_attribute
                node.final = 'N/A'
                node.branch = branch

        for value in values_dict[split_attribute]:
            new_obs = observations_subset[observations_subset[split_attribute] == value]
            #if there are no instances in the new split, just set the
            #child's value to that argmax of parent node
            if new_obs.shape[0] == 0:
                most = get_argmax(observations_subset, target, values_dict)
                if most == 'no':
                    most = 0
                else:
                    most = 1
                child = Node(new_obs, most, 'other', value)

            else:
                new_ATTR = []
                for item in ATTR:
                    new_ATTR.append(item)
                
                if split_attribute in new_ATTR:
                    new_ATTR.remove(split_attribute)
                else:
                    pass
                
                child = build_tree(new_obs, target, new_ATTR, values_dict, value)
                #if child is None, just set the node's value to its argmax
                #these instances should really be handled by stopping condition
                #but just in case one sneaks through the cracks
                if child == None:
                    most = get_argmax(observations_subset, target, values_dict)
                    if most == 'no':
                        most = 0
                    else:
                        most = 1
                    node.value = most
                else:
                    pass
            node.children.append(child)

    return node

def traverse(instance, decision_tree):
    '''Given an instance (in our case a patient) from testing data,
    use decision_tree made previously from training data
    to predict the instance's target column value
    '''
    
    if decision_tree.value == 0 or decision_tree.value == 1:
        return decision_tree.value 
    elif len(decision_tree.children) == 0:
        return decision_tree.value
    else:
        split_attribute = decision_tree.value
        instance_value = instance[split_attribute]
        next_node = 0
        for child in decision_tree.children:
            if child is not None:
                if child.branch == instance_value:
                    next_node = child
                    break
                else:
                    pass
            else:
                pass
        if next_node == 0:
            return get_argmax
        return traverse(instance, next_node)


def go(training_filename, testing_filename):
    '''Given a training_filename and testing_filename,
    creates decision_tree using training data,
    and classifies each instance in testing data,
    returning a list of all of their predictions where
    index in this list relates to number of instance in testing.
    '''
    training = pd.read_csv(training_filename)
    training = training.dropna()
    testing = pd.read_csv(testing_filename)
    testing = testing.dropna()

    attributes = list(training.columns[:-1])
    target = training.columns[-1]
    values_dict = create_values_dict(training)

    decision_tree = build_tree(training, target, attributes, values_dict)
    test_results = []
    actual = []
    total = 0
    for n in range(0,testing.shape[0]):
        b = traverse(testing.iloc[n], decision_tree)
        test_results.append(b)
        
    return test_results

if __name__=="__main__":
    if len(sys.argv) != 3:
        print("usage: python3 {} <training filename> <testing filename>".format(sys.argv[0]))
        sys.exit(1)

    for result in go(sys.argv[1], sys.argv[2]):
        print(result)
