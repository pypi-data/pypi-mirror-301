import math
import statistics
import unittest

from medver_pytest import pth

from tools import loader

loader.loader_init()

# ruff: noqa: E402
from on_the_fly_stats import OTFStats  # pylint: disable=wrong-import-position


# -------------------
class TestTp005(unittest.TestCase):

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
    def test_tp_005_stddev(self):
        pth.proto.protocol('tp-005', 'tests based on Stddev')

        pth.proto.step('verify initial values')
        otfs = OTFStats()
        otfs.create_stddev('sd1')

        pth.proto.step('verify initial values are set correctly')
        pth.ver.verify_true(math.isnan(otfs.stddev['sd1'].stddev), reqids=['SRS-080'])
        pth.ver.verify_true(math.isnan(otfs.stddev['sd1'].variance), reqids=['SRS-080'])
        pth.ver.verify_true(math.isnan(otfs.stddev['sd1'].mean), reqids=['SRS-080'])
        pth.ver.verify_equal(0, otfs.stddev['sd1'].num_elements, reqids=['SRS-080'])

        values = []
        val = 1
        values.append(val)
        pth.proto.step('verify a single updated value reports correctly')
        otfs.update_stddev('sd1', val)
        pth.ver.verify_true(math.isnan(otfs.stddev['sd1'].stddev), reqids=['SRS-081'])
        pth.ver.verify_true(math.isnan(otfs.stddev['sd1'].variance), reqids=['SRS-081'])
        pth.ver.verify_equal(1, otfs.stddev['sd1'].mean, reqids=['SRS-081'])
        pth.ver.verify_equal(1, otfs.stddev['sd1'].num_elements, reqids=['SRS-081'])

        pth.proto.step('verify two or more updated values reports correctly')
        val = 2
        values.append(val)
        otfs.update_stddev('sd1', val)
        pth.ver.verify_equal(statistics.stdev(values), otfs.stddev['sd1'].stddev, reqids=['SRS-082'])
        pth.ver.verify_equal(statistics.variance(values), otfs.stddev['sd1'].variance, reqids=['SRS-082'])
        pth.ver.verify_equal(statistics.mean(values), otfs.stddev['sd1'].mean, reqids=['SRS-082'])
        pth.ver.verify_equal(2, otfs.stddev['sd1'].num_elements, reqids=['SRS-082'])

        val = 3
        values.append(val)
        otfs.update_stddev('sd1', val)
        pth.ver.verify_equal(statistics.stdev(values), otfs.stddev['sd1'].stddev, reqids=['SRS-082'])
        pth.ver.verify_equal(statistics.variance(values), otfs.stddev['sd1'].variance, reqids=['SRS-082'])
        pth.ver.verify_equal(statistics.mean(values), otfs.stddev['sd1'].mean, reqids=['SRS-082'])
        pth.ver.verify_equal(3, otfs.stddev['sd1'].num_elements, reqids=['SRS-082'])

        pth.proto.step('verify after init(), initial values are reported correctly')
        otfs.stddev['sd1'].init()
        pth.ver.verify_true(math.isnan(otfs.stddev['sd1'].stddev), reqids=['SRS-083', 'SRS-080'])
        pth.ver.verify_true(math.isnan(otfs.stddev['sd1'].variance), reqids=['SRS-083', 'SRS-080'])
        pth.ver.verify_true(math.isnan(otfs.stddev['sd1'].mean), reqids=['SRS-083', 'SRS-080'])
        pth.ver.verify_equal(0, otfs.stddev['sd1'].num_elements, reqids=['SRS-083', 'SRS-080'])
