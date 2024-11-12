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
        code = """
x = 2
y = 3
"""
        analyzer = ParityAnalyzer()
        run_analysis(code, analyzer)
        
        self.assertEqual(analyzer.dict["x"], Parity.EVEN)
        self.assertEqual(analyzer.dict["y"], Parity.ODD)

    def test_code1(self):
        code = """
x = 2
y = 3
z = x + y
if z % 2 == 0:
    z = z * 2
else:
    z = z * 3
"""
        analyzer = ParityAnalyzer()
        run_analysis(code, analyzer)

        self.assertEqual(analyzer.dict["x"], Parity.EVEN)
        self.assertEqual(analyzer.dict["y"], Parity.ODD)
        self.assertEqual(analyzer.dict["z"], Parity.BOTH)

    def test_code2(self):
        code = """
x = 2
y = 3
z = x + y
if z % 2 == 0:
    z = z * 2
else:
    z = z * 3
z = x * 5
"""
        analyzer = ParityAnalyzer()
        run_analysis(code, analyzer)

        self.assertEqual(analyzer.dict["x"], Parity.EVEN)
        self.assertEqual(analyzer.dict["y"], Parity.ODD)
        self.assertEqual(analyzer.dict["z"], Parity.EVEN)

    def test_code3(self):
        code = """
x = 2
y = 3
z = x + y
if z % 2 == 0:
    z = z * 2
else:
    z = z * 3
z = z + 4
"""
        analyzer = ParityAnalyzer()
        run_analysis(code, analyzer)

        self.assertEqual(analyzer.dict["x"], Parity.EVEN)
        self.assertEqual(analyzer.dict["y"], Parity.ODD)
        self.assertEqual(analyzer.dict["z"], Parity.BOTH)

    def test_code4(self):
        code = """
x = 9
y = 4
z = x * y
z = z * 2
z = 1
x = z * 2
"""
        analyzer = ParityAnalyzer()
        run_analysis(code, analyzer)

        self.assertEqual(analyzer.dict["x"], Parity.EVEN)
        self.assertEqual(analyzer.dict["z"], Parity.ODD)

    def test_code5(self):
        code = """
x = 2
b = True
if b:
    x = x * 2
else:
    x = x * 3
x = x + 4
"""
        analyzer = ParityAnalyzer()
        run_analysis(code, analyzer)

        self.assertEqual(analyzer.dict["x"], Parity.EVEN)

    def test_code6(self):
        code = """
x = 3
b = True
if b:
    x = x * 2
else:
    x = x * 3
x = x + 4
"""
        analyzer = ParityAnalyzer()
        run_analysis(code, analyzer)

        self.assertEqual(analyzer.dict["x"], Parity.BOTH)

if __name__ == '__main__':
    unittest.main()
