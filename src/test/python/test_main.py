import unittest
from src.main.python.main import BitcoinPuzzleSolver

class TestBitcoinPuzzleSolver(unittest.TestCase):
    def setUp(self):
        self.solver = BitcoinPuzzleSolver()

    def test_generate_private_key(self):
        private_key = self.solver.generate_private_key()
        self.assertEqual(len(private_key), 64)  # 32 bytes in hex = 64 characters

    def test_private_key_to_address(self):
        private_key = "0" * 64
        address = self.solver.private_key_to_address(private_key)
        self.assertEqual(len(address), 64)  # SHA256 hash is 32 bytes, 64 in hex

    def test_check_address(self):
        # This test assumes the address is in the target_addresses.txt file
        self.assertTrue(self.solver.check_address("1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH"))
        self.assertFalse(self.solver.check_address("1111111111111111111111111111111111"))

if __name__ == '__main__':
    unittest.main()
