import unittest
import numpy as np

from esn import EchoStateNetwork

class TestEchoStateNetwork(unittest.TestCase):

    esn = EchoStateNetwork()

    def test_rms_error(self):
        y = np.array([1, 1.5, 0]).reshape(-1, 1)
        y_target = np.array([-1, -0.5, 0.5]).reshape(-1, 1)
        by_class = self.esn._rms_error(y, y_target)
        by_hand = 1.6583124
        self.assertAlmostEqual(by_class, by_hand)

    def test_x_tilde(self):
        W_in = np.array([[1,2,3],[4,5,6]])
        u = np.array([2, 2.5]).reshape(-1, 1)
        W = np.array([[1,1],[1,1]])
        x = np.array([-0.5, 0]).reshape(-1, 1)
        by_class = self.esn._x_tilde(W_in, u, W, x)
        by_hand = np.tanh(np.array([12.0, 28.5]).reshape(-1, 1))
        self.assertTrue(np.allclose(by_class, by_hand))

    def test_x_next(self):
        alpha = 0.5
        x = np.array([1,2]).reshape(-1, 1)
        x_tilde = np.array([-7,2]).reshape(-1, 1)
        by_class = self.esn._x_next(alpha, x, x_tilde)
        by_hand = np.array([-3.0, 2]).reshape(-1, 1)
        self.assertTrue(np.allclose(by_class, by_hand))

    def test_y_scalar(self):
        W_out = np.ones((1, 4))
        z = np.array([1,0.5,-1,3]).reshape(-1, 1)
        by_class = self.esn._y_scalar(W_out, z)
        by_hand = 3.5
        self.assertEqual(by_class, by_hand)

    def test_training_iteration(self):
        W_in = np.random.rand(4, 3)
        u = np.random.rand(2, 1)
        W = np.random.rand(4, 4)
        x = np.random.rand(4, 1)
        alpha = 0.5
        x_next, z = self.esn._training_iteration(W_in, u, W, x, alpha)
        self.assertEqual(x_next.shape[0], 4)
        self.assertEqual(x_next.shape[1], 1)
        self.assertEqual(z.shape[0], 7)
        self.assertEqual(z.shape[1], 1)

if __name__ == '__main__':
    unittest.main()
