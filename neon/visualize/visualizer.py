import networkx as nx
from utils.models.pnode import PNode

class Visualizer:
    def __init__(self, root: PNode) -> None:
        self.graph = nx.Graph()
        self._build_graph(root)

    def _build_graph(self, node: PNode) -> None:
        # The graph should look like a tree with root as the root
        # color the root node as red
        self.graph.add_node(node.id, label=node.token.lexeme, color='red' if node.depth == 0 else 'lightblue')
        for child in node.children:
            self.graph.add_node(child.id, label=child.token.lexeme, color='lightblue')
            self.graph.add_edge(node.id, child.id)
            self._build_graph(child)

    def draw(self):
        import matplotlib.pyplot as plt
        try:
            pos = nx.nx_agraph.graphviz_layout(self.graph, prog="dot")
        except Exception as e:
            pos = nx.spring_layout(self.graph)

        node_colors = [self.graph.nodes[node]['color'] for node in self.graph.nodes]
        nx.draw(self.graph, pos, with_labels=True, node_color=node_colors, edge_color='gray', node_size=500)
        plt.show()