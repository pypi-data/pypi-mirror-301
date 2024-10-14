import unittest

import torch

from normalkl import kl


class TestKL(unittest.TestCase):
    def setUp(self):
        self.dtype = torch.float64

    def test_kl_readme_example(self):
        dtype = self.dtype
        mean1 = torch.tensor([4.0, 5.0], dtype=dtype)
        covariance1 = torch.tensor([[1.0, 1.0], [2.0, 4.0]], dtype=dtype)
        mean2 = torch.tensor([1.0, 2.0], dtype=dtype)
        scalarvar2 = torch.tensor([3.0], dtype=dtype)

        result = kl(mean1, 'covmat', covariance1, mean2, 'scalarvar', scalarvar2)

        expected = torch.tensor([3.5853720317214703], dtype=dtype)
        self.assertTrue(torch.allclose(expected, result))


# Run the tests
if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)

