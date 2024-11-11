import unittest
from cfgAnalyzer import Parity, add_parity, mul_parity, try_int, try_parity, ParityAnalyzer

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
        analyzer = ParityAnalyzer()
        analyzer.add_var("x = 2")
        analyzer.add_var("y = 3")
        
        analyzer.visit("z = x + y")
        
        self.assertEqual(analyzer.dict["z"], Parity.ODD)

        analyzer.visit("z = z * 2")
        self.assertEqual(analyzer.dict["z"], Parity.EVEN)

        analyzer.visit("z = z * 3")
        self.assertEqual(analyzer.dict["z"], Parity.EVEN)

if __name__ == '__main__':
    unittest.main()