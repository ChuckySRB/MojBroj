"""
 Постaвка:
 n, n, n, n, nn, nnn == nnn
 o(+, -, *, /)

 Број комбинација са свим елементима: 6! * 4^5

 ~~ 1mil

"""

# Идеја 1

class Node:
    GlobalNumber = 0
    OPERATIONS = ("+, -, *, /")
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
        if operation not in Node.OPERATIONS:
            raise ValueError(f"Invalid operator: {operation}")
        return eq1 + eq2 + operation


class Solver:

    def __init__(self, numbers, goal):
        self.numbers = numbers
        self.goal = goal 
        self.unchecked_nodes = {}
        self.init_starter_nodes(numbers)
        self.checked_nodes = {}

    def init_starter_nodes(self, numbers):
        var_name = 'a'

        for i in range(len(numbers)):
            self.unchecked_nodes[var_name] = Node(numbers[i], var_name)
            var_name = chr(ord(var_name) + 1) # Advance to the next variable name

    def run(self):
        #
        



