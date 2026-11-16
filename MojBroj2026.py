"""
 Постaвка:
 n, n, n, n, nn, nnn == nnn
 o(+, -, *, /)

 Број комбинација са свим елементима: 6! * 4^5

 ~~ 1mil

"""

from typing import ClassVar
import random

# Идеја 1

OPERATIONS = ("+", "-", "*", "/")
OPERATIONS_SINGLE = ("+", "*")
EQUATION_MAX_LENGTH = 11


def reconstruct_solution(equation: str, numbers: list[int], goal: int) -> str:
    """Decode postfix notation, with a, b, c, ... indexing numbers in order."""
    variables = {chr(ord("a") + i): str(number) for i, number in enumerate(numbers)}
    stack = []

    for symbol in equation:
        if symbol in OPERATIONS:
            if len(stack) < 2:
                raise ValueError("Invalid equation: operator needs two operands")
            right = stack.pop()
            left = stack.pop()
            stack.append(f"({left} {symbol} {right})")
        elif symbol in variables:
            stack.append(variables[symbol])
        else:
            raise ValueError(f"Unknown equation symbol: {symbol}")

    if len(stack) != 1:
        raise ValueError("Invalid equation: expected one complete expression")

    expression = stack[0]
    if len(equation) > 1:
        expression = expression[1:-1]
    return f"{expression} = {goal}"


class Node:
    number_of_nodes = 0
    created_nodes: ClassVar[list[str]] = []
    equation_max_length = EQUATION_MAX_LENGTH
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
        """Preserve operand order and grouping by encoding the tree in postfix."""
        if operation not in OPERATIONS:
            raise ValueError(f"Invalid operator: {operation}")
        un = (set(eq1) & set(eq2)) - set(OPERATIONS)
        if len(un) > 0:
            raise ValueError("Cannot repeat variable twice") 
        return eq1 + eq2 + operation

    def set_max_length_eq(cls, length):
        cls.equation_max_length = length

    def is_max_length(self) -> bool:
        return len(self.equation) >= self.equation_max_length
        


class Solver:

    def __init__(self, numbers, goal):
        self.numbers = numbers
        self.goal = goal 
        self.unchecked_nodes = []
        self.checked_nodes = []
        self.all_nodes = []
        self.nodes_to_check = []
        
        self.init_starter_nodes(numbers)

    def init_starter_nodes(self, numbers):
        var_name = 'a'

        for i in range(len(numbers)):
            node = Node(numbers[i], var_name)
            self.unchecked_nodes.append(node)
            var_name = chr(ord(var_name) + 1) # Advance to the next variable name

    def check_node(self, node: Node):
        return node.value == self.goal

    def _merge_nodes(self, node1: Node, node2: Node, operation, save):
        try:
            node = Node(node1, node2, operation)
            if save:
                self.nodes_to_check.append(node)
        except ValueError:
            # Skip
            return
        except KeyError:
            # Skip
            return
        except ZeroDivisionError:
            # Skip
            return

    def merge_nodes(self, node1: Node, node2: Node):
        for operation in OPERATIONS:
            self._merge_nodes(node1, node2, operation, True)
            self._merge_nodes(node1, node2, operation, operation in OPERATIONS_SINGLE)
            

    def run(self) -> Node | None:
        iters = 0
        while len(self.unchecked_nodes) > 0:
            print(f"Iter start: {iters}")
            print(f"Unchecked Nodes: {len(self.unchecked_nodes)}")
            print(f"Checked Nodes: {len(self.checked_nodes)}")
            for node in self.unchecked_nodes:
                # Check the node:
                if self.check_node(node):
                    return node
                
            # Make next checks 
            self.nodes_to_check = []
            i = 0
            n = len(self.unchecked_nodes)           
            for i in range(n):
                node = self.unchecked_nodes[i]
                if node.is_max_length():
                    continue
                # Merge Node with the unchecked nodes:
                for cnode in self.checked_nodes:
                    self.merge_nodes(node, cnode)
                for unode in self.unchecked_nodes:
                    self.merge_nodes(node, unode)

            self.checked_nodes.extend(self.unchecked_nodes)
            self.unchecked_nodes = self.nodes_to_check 
            iters += 1
        return None



def build_nums() -> list[int]:
    """Draw four small numbers, one medium number, and one large number."""
    nums = [random.randint(1, 9) for _ in range(4)]
    nums.append(random.choice((10, 15, 20)))
    nums.append(random.choice((25, 50, 75, 100)))
    return nums


def build_goal() -> int:
    """Draw a target from 1 to 999, inclusive."""
    return random.randint(1, 999)


if __name__ == "__main__":

    nums = build_nums()
    goal = build_goal()
    print(f"Numbers: {nums}")
    print(f"Goal: {goal}")

    solver = Solver(nums, goal)

    result = solver.run()

    if result:
        print(reconstruct_solution(result.equation, nums, goal))


