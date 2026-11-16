"""
 Постaвка:
 n, n, n, n, nn, nnn == nnn
 o(+, -, *, /)

 Број комбинација са свим елементима: 6! * 4^5

 ~~ 1mil

"""

# Идеја 1

OPERATIONS = ("+, -, *, /")
OPERATIONS_SINGLE = ("+", "*")

class Node:
    number_of_nodes = 0
    created_nodes = []
    def __init__(self, init_n, init_symb, operation=None):
        if operation is None:
            self.value = init_n
            self.equation = init_symb
        else:
            child1 = init_n
            child2 = init_symb
            self.equation = self.build_equation(
                operation, child1.equation, child2.equation
            )
            if self.equation in self.created_nodes:
                raise KeyError
            self.created_nodes.append(self.equation)
            self.value = self.calc_operation(operation, child1.value, child2.value)
            
    @staticmethod
    def calc_operation(operation, a, b):
        if operation == "+":
            return a+b
        elif operation == "-":
            return a-b
        elif operation == "/":
            return a/b
        elif operation == "*":
            return a*b
        
        raise ValueError(f"Invalid operator: {operation}")

    @staticmethod
    def build_equation(operation: str, eq1: str, eq2: str):
        if operation not in OPERATIONS:
            raise ValueError(f"Invalid operator: {operation}")
        return eq1 + eq2 + operation


class Solver:

    def __init__(self, numbers, goal):
        self.numbers = numbers
        self.goal = goal 
        self.unchecked_nodes = []
        self.init_starter_nodes(numbers)
        self.checked_nodes = []
        self.all_nodes = []

    def init_starter_nodes(self, numbers):
        var_name = 'a'

        for i in range(len(numbers)):
            node = Node(numbers[i], var_name)
            self.unchecked_nodes.append(node)
            self.checked_nodes.append(node.equation)
            var_name = chr(ord(var_name) + 1) # Advance to the next variable name

    def check_node(self, node: Node):
        return node.value == self.goal

    def _merge_nodes(self, node1: Node, node2: Node, operation, save):
        try:
            node = Node(node1, node2, operation)
            if save:
                self.unchecked_nodes.append(node)
        except KeyError:
            # Skip
            return

    def merge_nodes(self, node1: Node, node2: Node):
        for operation in OPERATIONS:
            self._merge_nodes(node1, node2, operation, True)
            self._merge_nodes(node1, node2, operation, operation in OPERATIONS_SINGLE)
            
            


    def run(self) -> Node | None:

        while True:
            for node in self.unchecked_nodes:
                # Check the node:
                if self.check_node(node):
                    return node

            # Make next checks 
            next_unchecked_nodes = []
            i = 0
            n = len(self.unchecked_nodes)           
            for i in range(n):
                node = self.unchecked_nodes[i]
                # Merge Node with the unchecked nodes:
                for unode in self.unchecked_nodes:
                    self.merge_nodes(node, unode)
                



