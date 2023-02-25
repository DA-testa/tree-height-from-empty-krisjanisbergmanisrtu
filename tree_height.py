# python3

import sys
import threading
from collections import namedtuple


def find_parent(i, parents):
    # parent = Node(value=None, indx=None, level=None, parent=None, is_root=None)

    if not getattr(nodes[i], 'value'):  # parent does not exist in Nodes then we also have to find its parent
        new_parent = find_parent(parents[i], parents)
        child_level = getattr(new_parent, 'level') + 1
        child = Node(value=parents[i], indx=i, level=child_level, parent=new_parent, is_root=False)
        nodes[i] = child  # And set current node values
        return child
    else:
        new_parent = nodes[i]
        return new_parent


def compute_height(n, parents):
    tree_height = 0

    # Determine root
    root = Node(value=None, indx=None, level=None, parent=None, is_root=False)
    if n > 0 and parents:  # Check if there are any elements in array
        if -1 in parents:  # If value is -1 then
            root = root._replace(value=-1)  # save value
            root = root._replace(indx=parents.index(-1))  # and index of it
        else:  # If there was no value -1 then root is in index 0
            root = root._replace(value=parents[0])  # Save value
            root = root._replace(indx=0)

        root = root._replace(level=1,
                             is_root=True)  # Root is in level 1 and This will allow us to understand that we don't need to find parent for root
        # root.root = True
        tree_height = root.level

        nodes[root.indx] = root

    for i in range(len(parents)):  # Go through all nodes
        if not nodes[i]:  # If node is not in nodes array
            nodes[i] = Node(value=parents[i], indx=i, level=None, parent=None,
                            is_root=False)  # value, and index to find in Nodes[], we will need to find level and parent.

        if not nodes[i].is_root:  # If not root then continue find level (height)
            parent = find_parent(i, parents)
            nodes[i] = nodes[i]._replace(parent=parent)
            nodes[i] = nodes[i]._replace(level=getattr(parent, 'level') + 1)

        if tree_height < getattr(parent, 'level'):
            tree_height = getattr(parent, 'level')

    return tree_height


nodes = []  # This will store nodes that we have already handled (I don't know if I really need it yet)
# value - one of the parent values we enter
# indx - index in array of  values we entered
# level - in which level this node is located in
# parent - parent node with
# root - is this node the root of tree
Node = namedtuple('Node', ['value', 'indx', 'level', 'parent', 'is_root'])


def main():
    # implement input form keyboard and from files
    text = input()
    parents = ""
    n = ""

    if "F" in text:
        file_name = input()
        # let user input file name to use, don't allow file names with letter a
        # account for github input inprecision
        if not "a" in file_name:
            file = open("./test/" + file_name, "r")
            text = file.read()

            text = text.split('\n')
            n = text[0]
            parents = text[1].split(' ')

    elif "I" in text:
        n = input()
        parents = input()

    # Delete this block
    # file = open("./test/" + "01", "r")
    # text = file.read()
    #
    # text = text.split('\n')
    # n = text[0]
    # parents = text[1].split(' ')
    #####

    # cast to ints
    n = int(n)
    parents = [eval(i) for i in parents]

    for j in range(n):  # Make array to hold empty values for each expected node
        nodes.append(Node(value=None, indx=None, level=None, parent=None, is_root=False))

    print(compute_height(n, parents))
    print(nodes)

    # input number of elements
    # input values in one variable, separate with space, split these values in an array
    # call the function and output it's result


# In Python, the default limit on recursion depth is rather low,
# so raise it here for this problem. Note that to take advantage
# of bigger stack, we have to launch the computation in a new thread.
sys.setrecursionlimit(10 ** 7)  # max depth of recursion
threading.stack_size(2 ** 27)  # new thread will get stack of such size
threading.Thread(target=main).start()
