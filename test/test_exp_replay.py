import unittest
from agent.exp_replay import *


class TestExpReplay(unittest.TestCase):
    def setUp(self):
        pass

    def test_add(self):
        replay = ExpReplay(2)
        replay.add([0.1, 0.1, 0, 0, 0.1, 0.1, 0, 0, 2 / 100.0], 0.006)
        self.assertEqual(len(replay), 1)
        replay.add([0.06, 0.08, 0, 0, 0.1, 0.1, 0, 0, 4 / 100.0], 0.004)
        self.assertEqual(len(replay), 2)
        replay.add([0.07, 0.07, 0, 0, 0.1, 0.1, 0, 0, 5 / 100.0], 0.015)
        self.assertEqual(len(replay), 2)

    def test_batch(self):
        replay = ExpReplay(10)
        for i in range(10):
            replay.add([0.1, 0.1, 0, 0, 0.1, 0.1, 0, 0, 2 / 100.0], 0.006)
        batch_x, batch_y = replay.batch(2)
        self.assertEqual(batch_x.shape, (2, 9))
        self.assertIsInstance(batch_x, np.ndarray)
        self.assertIsInstance(batch_x[0], np.ndarray)
        self.assertEqual(batch_y.shape, (2,))
        self.assertIsInstance(batch_y, np.ndarray)
        self.assertIsInstance(batch_y[0], np.float)


if __name__ == '__main__':
    unittest.main()
