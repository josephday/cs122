# CS122 W'16: treemaps
# Joseph Day -- 1/12/16 -- Rogers Section -- PA1

import Deposit_Tree
import Color_Key
import Chi_Canvas
import sys


MIN_RECT_SIDE=0.01
MIN_RECT_SIDE_FOR_TEXT=0.03
X_SCALE_FACTOR=12
Y_SCALE_FACTOR=10

c = Chi_Canvas.Chi_Canvas(X_SCALE_FACTOR, Y_SCALE_FACTOR)

def aggregate_values(t):
    '''Takes in a tree with only leaf values, 
    aggregates values in all nodes as sum of children's values

    Inputs: t -- a tree
    Outputs: None -- alters t in its place, changing weight of 
    each parent node from zero to the sum of its children's deposits'''
    if t.is_leaf_node() is True:
        return t._branch.deposits
    elif t.is_leaf_node() is False:
        weight = 0
        for kid in t.children:
            try:
                weight += aggregate_values(t.get_subtree([kid.label]))
            except TypeError:
                weight += t.get_subtree([kid.label]).weight            
        t.set_weight(weight)


def get_classes(t, classes=[]):
    '''Takes in an empty list and a tree, returns a set 
    containing all classes of institution present in that tree

    Inputs: t -- a tree, classes (optional) -- list of classes, starts empty
    Outputs: set version of list of classes for all branches in t'''


    if t.is_leaf_node() is True:
        classes.append(t._branch.cls)
    elif t.is_leaf_node() is False:
        for kid in t.children:
            get_classes(t.get_subtree([kid.label]), classes)     
    return set(classes)

def calc_percent(node):
    '''Takes in a node and returns dictionary where keys are child names and values 
    are child weight / parent weight

    Inputs: tree or node
    Outputs: a list, percents, where each element in the list is the ratio of the weight 
    of one of the input node's children to the weight of the input node itself'''
    percents = {}
    if node.is_leaf_node() is True:
        pass
    elif node.is_leaf_node() is False:
        denom = node.weight
        for kid in node.children:
            sub = node.get_subtree([kid.label])
            if sub.is_leaf_node() is True:
                percent = sub._branch.deposits/denom
            else:
                percent = (node.get_subtree([kid.label]).weight) / denom
            percents[kid.label] = (percent)
    return percents


def tree_map_doer(c, t, ck, x0=0, x1=0.8, y0=0, y1=1, s=0):

    '''(Appropriately) DOES most of the work for this PA, 
    determining coordinates of rectangles and drawing them.

    Inputs: c -- a canvas, t -- a tree, ck -- a color key, 
    x0,x1,y0,y1 -- coordinates of a rectangle to be drawn or split appropriately,
    s -- spin value, even or odd that determines whether a rectangle, if it
    is to be split, is split horizontally or vertically

    Outputs: c -- canvas'''
    
    if t.is_leaf_node():
        label = "${}k  {} ({}, {}, {})  {}".format(t._branch.deposits, t._branch.instname, t._branch.city, t._branch.county, t._branch.state, t._branch.branchname)
        c.draw_rectangle(x0,y0,x1,y1,fill=ck.get_color(t._branch.cls))

        if (y1-y0)<MIN_RECT_SIDE_FOR_TEXT and (x1-x0)<MIN_RECT_SIDE_FOR_TEXT:
            pass #filters out rectangles too small for text
        else:
            if (y1-y0)>(x1-x0):
                c.draw_text_vertical((x0+x1)/2,(y0+y1)/2, y1-y0, label)
            else: 
                c.draw_text((x0+x1)/2,(y0+y1)/2, x1-x0, label)  

        return 

    else:
        s+=1 #adds one to s, changing whether we split horizontal or vertical
        w = x1-x0
        h = y1-y0
        percents = calc_percent(t)

        if w<MIN_RECT_SIDE or h<MIN_RECT_SIDE: #filters out rectangles too small to be split
            c.draw_rectangle(x0,y0,x1,y1, fill=ck.get_color("Default")) 
        else:
            if s%2==1: #split left to right
                for kid in t.children:
                    subt = t.get_subtree([kid.label])
                    x1 = x0 + w*percents[kid.label]
                    tree_map_doer(c, subt, ck, x0, x1, y0, y1, s)
                    x0 = x1
            else: #split top to bottom
                for kid in t.children:
                    subt = t.get_subtree([kid.label])
                    y1 = y0 + h*percents[kid.label]
                    tree_map_doer(c, subt, ck, x0, x1, y0, y1, s)
                    y0 = y1         

    return c


def draw_tree_map(c, t):
    
    '''draws a treemap for deposit tree t in canvas c'''
    
    classes = get_classes(t)
    ck = Color_Key.Color_Key(classes)
    ck.draw_color_key(c,.8,0,1.0,.30)

    c=tree_map_doer(c,t,ck)
    #c.show()    


def test_subtree(input_filename, path, output_filename):
    ''' 
    Generate a treemap for a specific subtree of the tree
    specified in the input file.  The subtree is specified by
    a list of labels for nodes along the path.  

    If output_filename is None, the resulting treemap is displayed (shown),
    otherwise it is saved in the specified output file.
        
    sample use:
        test_subtree("CPA.csv", ['PA', 'Washington', 'Charleroi', 'SB'], None)

    generates a treemap for the savings banks example from the
    description and displays it.
    '''

    c = Chi_Canvas.Chi_Canvas(X_SCALE_FACTOR, Y_SCALE_FACTOR)
    t = Deposit_Tree.Deposit_Tree(filename=input_filename)
    if len(path) > 0:
        t = t.get_subtree(path)
        if t is None:
            print("Could not build subtree")
            return
    draw_tree_map(c, t)
    if output_filename == None:
        c.show()
    else:
        c.savefig(output_filename)


def test_savings_banks(output_filename):
    '''
    generates a treemap for the savings banks example in the description
    '''
    test_subtree("CPA.csv", ['PA', 'Washington', 'Charleroi', 'SB'],
                 output_filename)


def test_charleroi(output_filename):
    '''
    generates a treemap for all institutions in Charleroi
    (one of the examples in the description)
    '''
    test_subtree("CPA.csv", ['PA', "Washington", 'Charleroi'], output_filename)


def test_greater_charleroi(output_filename):
    '''
    generates a treemap for banks in and around Charleroi
    '''
    test_subtree("CPA.csv", [], output_filename)


def go(input_filename, output_filename):
    '''
    draw a treemap for the deposit data in the input file
    and save the result in the output file (or display it,
    if output_filename is None).
    '''
    test_subtree(input_filename, [], output_filename)


if __name__=="__main__":
    num_args = len(sys.argv)

    if num_args < 2 or num_args > 4:
        print("usage: python3 " + sys.argv[0] + " [savings-banks | charleroi | greater-charleroi | <a file name>] [output filename]")
        sys.exit(0)

    if num_args == 3:
        output_filename = sys.argv[2]
    else:
        output_filename = None

    if sys.argv[1] == "savings-banks":
        test_savings_banks(output_filename)
    elif sys.argv[1] == "charleroi":
        test_charleroi(output_filename)
    elif sys.argv[1] == "greater-charleroi":
        test_greater_charleroi(output_filename)
    else:
        go(sys.argv[1], output_filename)



            
    
    
        
