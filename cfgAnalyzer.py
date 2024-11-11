from pycfg.pycfg import PyCFG, CFGNode
import re

# Define lattice states
class Parity:
    EVEN = "E"
    ODD = "O"
    UNKNOWN = "U"

# Define abstract operations for addition and multiplication
def add_parity(a, b):
    if a == Parity.EVEN and b == Parity.EVEN:
        return Parity.EVEN
    elif a == Parity.ODD and b == Parity.ODD:
        return Parity.EVEN
    elif a == Parity.EVEN and b == Parity.ODD:
        return Parity.ODD
    elif a == Parity.ODD and b == Parity.EVEN:
        return Parity.ODD
    else:
        return Parity.UNKNOWN

def mul_parity(a, b):
    if a == Parity.EVEN or b == Parity.EVEN:
        return Parity.EVEN
    elif a == Parity.ODD and b == Parity.ODD:
        return Parity.ODD
    elif a == Parity.EVEN and b == Parity.ODD:
        return Parity.EVEN
    elif a == Parity.ODD and b == Parity.EVEN:
        return Parity.EVEN
    else:
        return Parity.UNKNOWN
    
def try_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def try_parity(var):
    if try_int(var):
        if int(var) % 2 == 0:
            return Parity.EVEN
        else:
            return Parity.ODD
    else:
        return Parity.UNKNOWN

class ParityAnalyzer:
    def __init__(self):
        self.dict = {}

    def add_var(self, node):
        s = node.split(' = ')
        self.dict[s[0]] = try_parity(s[1])

    def visit(self, node):
        if '+' in node:
            pattern_plus = r'(\w+)\s*\+\s*(\w+)'
            match_plus = re.search(pattern_plus, node)
            left_var = match_plus.group(1)
            right_var = match_plus.group(2)
            result_state = add_parity(
                self.dict.get(left_var, try_parity(left_var)),
                self.dict.get(right_var, try_parity(right_var))
            )
            self.dict[node.split(' = ')[0]] = result_state

        elif '*' in node:
            pattern_multiply = r'(\w+)\s*\*\s*(\w+)'
            match_multiply = re.search(pattern_multiply, node)
            left_var = match_multiply.group(1)
            right_var = match_multiply.group(2)
            result_state = mul_parity(
                self.dict.get(left_var, try_parity(left_var)),
                self.dict.get(right_var, try_parity(right_var))
            )
            self.dict[node.split(' = ')[0]] = result_state

        print(f"Node: {node}")
        for var in self.dict:
            state = self.dict.get(var, Parity.UNKNOWN)
            print(f"Variable {var}: {state}")

# Sample code
source_code = """
x = 2
y = 3
z = x + y
if z % 2 == 0:
    z = z * 2
else:
    z = z * 3
"""

cfg = PyCFG()
cfg.gen_cfg(source_code)
g = CFGNode.to_graph() 
g.draw('t.png', prog ='dot')
analyzer = ParityAnalyzer()

for node in g.nodes():
    label = node.attr['label']
    label = label[3:]
    if ' = ' in label:
        analyzer.add_var(label)

for node in g.nodes():
    label = node.attr['label']
    label = label[3:]
    analyzer.visit(label)
