import unittest
from unittest.mock import MagicMock, patch
from cfgAnalyzer import Parity, add_parity, mul_parity, try_int, try_parity, ParityAnalyzer, run_analysis, PyCFG, CFGNode

class TestCFGAnalyzer(unittest.TestCase):
    
    def test_add_parity(self):
        # Test addition of parities
        self.assertEqual(add_parity(Parity.EVEN, Parity.EVEN), Parity.EVEN)
        self.assertEqual(add_parity(Parity.ODD, Parity.ODD), Parity.EVEN)
        self.assertEqual(add_parity(Parity.EVEN, Parity.ODD), Parity.ODD)
        self.assertEqual(add_parity(Parity.ODD, Parity.EVEN), Parity.ODD)
        self.assertEqual(add_parity(Parity.UNKNOWN, Parity.EVEN), Parity.UNKNOWN)
        self.assertEqual(add_parity(Parity.EVEN, Parity.UNKNOWN), Parity.UNKNOWN)

    def test_mul_parity(self):
        # Test multiplication of parities
        self.assertEqual(mul_parity(Parity.EVEN, Parity.EVEN), Parity.EVEN)
        self.assertEqual(mul_parity(Parity.ODD, Parity.ODD), Parity.ODD)
        self.assertEqual(mul_parity(Parity.EVEN, Parity.ODD), Parity.EVEN)
        self.assertEqual(mul_parity(Parity.ODD, Parity.EVEN), Parity.EVEN)
        self.assertEqual(mul_parity(Parity.UNKNOWN, Parity.EVEN), Parity.UNKNOWN)
        self.assertEqual(mul_parity(Parity.EVEN, Parity.UNKNOWN), Parity.UNKNOWN)

    def test_try_int(self):
        # Test try_int function for valid and invalid values
        self.assertTrue(try_int("123"))
        self.assertFalse(try_int("abc"))
        self.assertFalse(try_int("12.34"))
        self.assertTrue(try_int("-123"))

    def test_try_parity(self):
        # Test try_parity function for even, odd, and unknown values
        self.assertEqual(try_parity("4"), Parity.EVEN)
        self.assertEqual(try_parity("7"), Parity.ODD)
        self.assertEqual(try_parity("abc"), Parity.UNKNOWN)
        self.assertEqual(try_parity("-5"), Parity.ODD)

    def test_parity_analyzer_add_var(self):
        # Test adding variables to the analyzer
        analyzer = ParityAnalyzer()
        analyzer.add_var("x = 2")
        analyzer.add_var("y = 3")
        
        self.assertEqual(analyzer.dict["x"], Parity.EVEN)
        self.assertEqual(analyzer.dict["y"], Parity.ODD)

    def test_parity_analyzer_visit(self):
        # Test visiting nodes and analyzing their parity
        print("-------------------------------------------------")
        analyzer = ParityAnalyzer()
        analyzer.add_var("x = 2") # 1
        analyzer.add_var("y = 3") # 2
        
        analyzer.visit("z = x + y", 3) # 3
        
        self.assertEqual(analyzer.dict["z"], Parity.ODD)

        analyzer.visit("z = z * 2", 4) # 4
        self.assertEqual(analyzer.dict["z"], Parity.EVEN)

        analyzer.visit("z = z * 3", 5) # 5
        self.assertEqual(analyzer.dict["z"], Parity.EVEN)
        print("************************************************")

    def test_code1(self):
        # Sample code
        code = """
x = 2
y = 3
z = x + y
if z % 2 == 0:
    z = z * 2
else:
    z = z * 3
"""
        cfg = PyCFG()
        cfg.gen_cfg(code)
        g = CFGNode.to_graph() 
        g.draw('cfg.png', prog ='dot') # draw the cfg
        analyzer = ParityAnalyzer()
        
        for node in g.nodes():
            label = node.attr['label']
            label = label[3:]
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
            print(analyzer.dict["z"])

        self.assertEqual(analyzer.dict["x"], Parity.EVEN)
        self.assertEqual(analyzer.dict["y"], Parity.ODD)
        self.assertEqual(analyzer.dict["z"], Parity.BOTH)

    def test_parity_update_after_reassign(self):
        # Test code where variables are re-assigned
        analyzer = ParityAnalyzer()
        analyzer.add_var("x = 2") # 1
        analyzer.add_var("y = 3") # 2
        
        analyzer.visit("z = x + y", 3) # 3
        self.assertEqual(analyzer.dict["z"], Parity.ODD)
        
        analyzer.add_var("z = 4") # 4
        analyzer.visit("z = z * 3", 5) # 5
        self.assertEqual(analyzer.dict["z"], Parity.EVEN)


if __name__ == '__main__':
    unittest.main()
