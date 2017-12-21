import unittest
from agent.func_aprox import *
import numpy as np


class TestFuncApprox(unittest.TestCase):
    def setUp(self):
        pass

    def test_mlp(self):
        mlp = MLP('test', (9, 50, 50, 1))
        batch_x = np.array([[0.1 for _ in range(9)], [0.2 for _ in range(9)], [0.3 for _ in range(9)]])
        batch_y = np.array([[1], [2], [3]])
        mlp.train((batch_x, batch_y))
        value = mlp.eval(np.array([[0.1 for _ in range(9)]]))
        self.assertIsInstance(value[0][0], np.float32)


if __name__ == '__main__':
    unittest.main()
