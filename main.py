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



class Graph:

    def __init__(self):
        """ Default constructor that builds the Graph """
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

    def buildadj(self, dicts: defaultdict(list)):
        for k, v in dicts.items():
            if isinstance(v, dict):
                print(isinstance(v, dict))
                self.buildadj(v)
            else:
                print
                "{0} : {1}".format(k, v)

    def debug(self, key: str):
        vertexleft = self.nodeset.copy()
        while vertexleft:
            shortestpath = defaultdict(list)  # type: defaultdict(list)
            nearest = (None, math.inf)  # type: tuple
            visited = defaultdict(list)  # type: defaultdict(list)
            finding = list(vertexleft)[0]
            k,v = self.distances.items()
            print(f"{k} {v}")
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


class DijGraph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distance = {}

    def add_node(self, value):
        self.nodes.add(value)
        return self

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distance[(from_node, to_node)] = distance
        return self


def dijsktra(graph, initial):
    visited = {initial: 0}
    path = {}
    nodes = set(graph.nodes)
    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node
        if min_node is None:
            break
        nodes.remove(min_node)
        current_weight = visited[min_node]
        for edge in graph.edges[min_node]:
            try:
                weight = current_weight + graph.distance[(min_node, edge)]
            except:
                continue
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node
    return visited, path


if __name__ == "__main__":
    Gr = Graph()
    DG = DijGraph()
    with open("small.txt") as f:
        for line in f:
            DG.add_node(*line.strip().split(",")[0])
            DG.add_node(*line.strip().split(",")[1])
            DG.add_edge(*line.strip().split(","))
            Gr.addNode(*line.strip().split(","))
            # print(Gr)
    _, path = dijsktra(DG, "e")
    print(path)
    #Gr.buildadj(Gr.distances)
    # kruskal(Gr).print()
