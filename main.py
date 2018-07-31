"""
Clayton A. Turner
CS 317 Project 3
Python 3.7 but should work on any Python 3.X
Kruskal's Algoritm and Djikstras

"""

import typing
import builtins
from collections import defaultdict
import math
# both of these will say unused imports; however, they are used for accessing object types
# and for typehinting to work for development


class Graph:
    """ Default constructor that builds the Graph """

    def __init__(self):
        self.root = list()  # type: list('Node')
        self.nodeset = set()  # type: set('Node')
        self.size = len(self.nodeset)  # type: int, holds # of unique vertexes
        self.distances = defaultdict(list)  # type: defaultdict(list)

    def addNode(self, node1: str, node2: str, weight: str):
        """Add a node into the Graph, and then sort the list"""
        self.distances[node1].append([node2, weight])
        self.root.append(Node(node1, node2, weight))
        self.nodeset.add(node1)
        self.nodeset.add(node2)
        self.size = len(self.nodeset)
        self.sort()

    def debug(self, key: str):
        vertexleft = self.nodeset.copy()
        while vertexleft:
            shortestpath = defaultdict(list)  # type: defaultdict(list)
            nearest = (None, math.inf)  # type: tuple
            visited = dict()  # type: dict
            finding = list(vertexleft)[0]
            for k,v in self.distances.get(key):
                if (k == finding[0]) and (nearest[1] > v):
                    nearest = (k, v)
                vertexleft.remove(finding)

    def __str__(self):
        """Overrides the dunder str method so that I can call print(Graph) directly
        Basically it creates a list of the desired output """
        temp = list()  # type: list
        temp.append("The graph has the letters {}".format(self.nodeset))
        for n in self:
            temp.append("{} to {} weight {}".format(n.node1, n.node2, n.weight))
        return str(temp)

    def __iter__(self):
        """iterator. This lets me call for x in Graph and iterate over each of the layers"""
        for item in self.root:
            yield item

    def sort(self):
        """Sort method that calls the .sort() method to map each element by the nodes weight. Then do not reverse
        So it stays in Non Decresasing order."""
        self.root.sort(key=lambda x: x.weight, reverse=False)


class Node:
    def __init__(self, node1: str, node2: str, weight: str):
        """Constructfor for the Node Class"""
        self.node1 = node1
        self.node2 = node2
        self.weight = int(weight)

    def __lt__(self, other: 'Node'):
        """Overrides Node 1 < Node 2 by comparing the weight attribute"""
        return self.weight < other.weight

    def __le__(self, other):
        """Overrides Node1 <= Node 2 by comparing the weight attribute"""
        return self.weight <= other.weight

    def __str__(self):
        """Fancy String override to print the Node by calling print(Node)"""
        return "{} <-> {} Weight: {}".format(self.node1, self.node2, self.weight)


class MST:
    """Builds the Minimum Spanning Tree and Adjacency Matrix"""

    def __init__(self):
        self.total = 0  # type: int holds the total amount of nodes
        self.mst = list()  # type: list holds the nodes
        self.mstset = set()  # type: set holds the set of vertexes to know if this is a cycle

    def addmst(self, adjnode: Node):
        """Add a node to the Minimum Spanning Tree and the Minimum Spanning Tree Set """
        self.mst.append(adjnode)
        self.mstset.add(adjnode.node1)
        self.mstset.add(adjnode.node2)

    def is_cycle(self, newnode: Node, graph: Graph):
        """This method determines if the addition of a node will cause a cycle to form in the graph"""
        tempset = self.mstset.copy()  # create a copy of our MST Set variable
        tempset.add(newnode.node1)  # add node1 and node 2 to the set
        tempset.add(newnode.node2)
        return len(tempset) == len(self.mstset)  # if the lengths are the same it will create a cycle because a set

    # is guaranteed to have all unique elements

    def is_final(self, newnode: Node, graph: Graph):
        """Will the vertex complete the graph"""
        tempset = set()  # type: set temp variable
        for node in self.mst:  # iterate over the minimum spanning tree
            # node 1 is the left, node 2 is the right
            tempset.add(node.node2)  # add each right node
        tempset.add(newnode.node2)  # add the current destination to the temporary set
        return len(tempset) == (len(graph.nodeset) - 1)

    # if the length of our temp set is == the nodeset-1 then every node except the start point is within our graph

    def print(self):
        """Prints the Minimum Spanning tree. This will become a __str__ override eventually"""
        print("MST: ")
        total = 0
        for node in self.mst:
            total += node.weight
            print("{}-{} weight {}".format(node.node1, node.node2, node.weight))
        print("Total Weight: {}".format(total))


def kruskal(krusgraph: Graph):  # method to perform Kruskal's algorithm
    adjmat = MST()  # type: MST
    for node in krusgraph:  # iterate the Graph in sorted order
        if not adjmat.is_cycle(node, krusgraph):  # if the edge won't form a cycle
            adjmat.addmst(node)  # add it to the minimum spanning tree
        elif adjmat.is_final(node, krusgraph):  # if the node will complete the mst
            adjmat.addmst(node)  # add it
            break  # and break
    return adjmat  # return the Adjacency Object containing the mst


if __name__ == "__main__":
    Gr = Graph()
    with open("small.txt") as f:
        for line in f:
            Gr.addNode(*line.strip().split(","))
            # print(Gr)
    Gr.debug("a")
    # kruskal(Gr).print()
