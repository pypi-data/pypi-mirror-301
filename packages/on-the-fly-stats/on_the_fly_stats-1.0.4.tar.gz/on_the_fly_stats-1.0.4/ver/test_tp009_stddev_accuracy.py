import math
import random
import statistics
import unittest

from medver_pytest import pth

from tools import loader

loader.loader_init()

# ruff: noqa: E402
from on_the_fly_stats import OTFStats  # pylint: disable=wrong-import-position


# -------------------
class TestTp009(unittest.TestCase):
    lines = []

    # --------------------
    @classmethod
    def setUpClass(cls):
        pth.init()

    # -------------------
    def setUp(self):
        print('')

    # -------------------
    def tearDown(self):
        pass

    # --------------------
    @classmethod
    def tearDownClass(cls):
        pth.term()

    # --------------------
    def test_tp_009_stddev_accuracy(self):
        pth.proto.protocol('tp-009', 'verify accuracy of stddev calculations')

        pth.proto.step('verify initial values')

        pth.proto.step('verify empty report is generated correctly')
        otfs = OTFStats()

        pth.proto.step('calculate the stddev 100 times and compare to python statistics module')
        values = []
        for count in range(0, 100):
            # val = random.uniform(0, 1000) # works to 2e-13
            val = random.random()
            values.append(val)
            otfs.update_stddev('sd1', val)
            if count > 2:
                diff = math.fabs(otfs.stddev['sd1'].stddev - statistics.stdev(values))
                pth.ver.verify_lt(diff, 1e-15, reqids=['SRS-084'])
                pth.ver.verify_equal(count + 1, otfs.stddev['sd1'].num_elements, reqids=['SRS-084'])
