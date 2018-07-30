class Graph:
	def __init__(self):
		self.root = list()  # type: list

	def addNode(self, node1 : str, node2 : str, weight : str):
		self.root.append( Node( node1, node2, weight))

	def __str__(self):
		temp = []
		for n in self:
			temp.append("{} to {} weight {}".format(n.node1, n.node2, n.weight))
		return str(temp)

	def __iter__(self):
		for item in self.root:
			yield item

class Node:
	def __init__(self, node1 : str, node2 : str, weight : int):
		self.node1 = node1
		self.node2 = node2
		self.weight = weight







if __name__ == "__main__":
	Gr = Graph()
	with open("graph.txt") as f:
		for line in f:
			Gr.addNode(*line.strip().split(","))
	print(Gr)
