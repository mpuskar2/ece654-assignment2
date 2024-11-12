from pycfg.pycfg import PyCFG, CFGNode
import re

# Define lattice states
class Parity:
    BOTH = "B"
    EVEN = "E"
    ODD = "O"
    UNKNOWN = "U"

# Define abstract operations for addition and multiplication
def add_parity(a, b):
    if a == Parity.UNKNOWN or b == Parity.UNKNOWN:
        return Parity.UNKNOWN
    elif a == Parity.BOTH or b == Parity.BOTH:
        return Parity.BOTH
    elif a == Parity.EVEN and b == Parity.EVEN:
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
    if a == Parity.UNKNOWN or b == Parity.UNKNOWN:
        return Parity.UNKNOWN
    elif a == Parity.BOTH or b == Parity.BOTH:
        return Parity.BOTH
    elif a == Parity.EVEN and b == Parity.EVEN:
        return Parity.EVEN
    elif a == Parity.ODD and b == Parity.ODD:
        return Parity.ODD
    elif a == Parity.EVEN and b == Parity.ODD:
        return Parity.EVEN
    elif a == Parity.ODD and b == Parity.EVEN:
        return Parity.EVEN
    else:
        return Parity.UNKNOWN
    
def merge_parities(a, b):
    if a == Parity.EVEN and b == Parity.EVEN:
        return Parity.EVEN
    elif a == Parity.ODD and b == Parity.ODD:
        return Parity.ODD
    elif a == Parity.EVEN and b == Parity.ODD:
        return Parity.BOTH
    elif a == Parity.ODD and b == Parity.EVEN:
        return Parity.BOTH
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
        self.branches = []
        self.merge_nodes = []
        self.temp_sets = []

    def add_branch(self, nodenum):
        self.branches.append(nodenum)

    def remove_branch(self, nodenum):
        self.branches.remove(nodenum)

    def add_mnode(self, nodenum):
        self.merge_nodes.append(nodenum)

    def remove_mnode(self, nodenum):
        self.merge_nodes.remove(nodenum)

    def add_var(self, node):
        s = node.split(' = ')
        self.dict[s[0]] = Parity.UNKNOWN

    def visit(self, code, node):
        index = None
        branch  = False
        for i, nodenum in enumerate(self.branches):
            if node == nodenum:
                self.temp_sets.insert(i, self.dict.copy())
                index = i
                branch = True

        if node in self.merge_nodes:
            for key in self.dict.keys():
                merged_value = self.temp_sets[0][key]
                for temp_set in self.temp_sets[1:]:
                    merged_value = merge_parities(merged_value, temp_set[key])
                self.dict[key] = merged_value

            self.remove_mnode(node)
            self.temp_sets = []

        if '+' in code:
            pattern_plus = r'(\w+)\s*\+\s*(\w+)'
            match_plus = re.search(pattern_plus, code)
            left_var = match_plus.group(1)
            right_var = match_plus.group(2)
            if not branch:
                result_state = add_parity(
                    self.dict.get(left_var, try_parity(left_var)),
                    self.dict.get(right_var, try_parity(right_var))
                )
                self.dict[code.split(' = ')[0]] = result_state
            else:
                result_state = add_parity(
                    self.temp_sets[index].get(left_var, try_parity(left_var)),
                    self.temp_sets[index].get(right_var, try_parity(right_var))
                )
                self.temp_sets[index][code.split(' = ')[0]] = result_state

        elif '*' in code:
            pattern_multiply = r'(\w+)\s*\*\s*(\w+)'
            match_multiply = re.search(pattern_multiply, code)
            left_var = match_multiply.group(1)
            right_var = match_multiply.group(2)
            if not branch:
                result_state = mul_parity(
                    self.dict.get(left_var, try_parity(left_var)),
                    self.dict.get(right_var, try_parity(right_var))
                )
                self.dict[code.split(' = ')[0]] = result_state
            else:
                result_state = mul_parity(
                    self.temp_sets[index].get(left_var, try_parity(left_var)),
                    self.temp_sets[index].get(right_var, try_parity(right_var))
                )
                self.temp_sets[index][code.split(' = ')[0]] = result_state
        elif ' = ' in code:
            s = code.split(' = ')
            self.dict[s[0]] = try_parity(s[1])

        print(f"Node {node}: {code}")
        if not branch:
            for var in self.dict:
                state = self.dict.get(var, Parity.UNKNOWN)
                print(f"Variable {var}: {state}")
        else:
            for var in self.temp_sets[index]:
                state = self.temp_sets[index].get(var, Parity.UNKNOWN)
                print(f"Variable in branch {var}: {state}")            


def run_analysis(code, analyzer):
    cfg = PyCFG()
    cfg.gen_cfg(code)
    g = CFGNode.to_graph() 
    g.draw('cfg.png', prog ='dot') # draw the cfg
    
    for node in g.nodes():
        label = node.attr['label']
        split = label.find(': ')
        label = label[split + 2:].strip()

        if len(g.out_edges(node)) > 1:
            for target in g.successors(node):
                analyzer.add_branch(target)

        if ' = ' in label:
            analyzer.add_var(label)

    for node in g.nodes():
        label = node.attr['label']
        label = label[3:]
        if len(g.in_edges(node)) > 1:
            analyzer.add_mnode(node)
            for target in g.predecessors(node):
                analyzer.remove_branch(target)
        analyzer.visit(label, node)

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
analyzer = ParityAnalyzer()
run_analysis(source_code, analyzer)
