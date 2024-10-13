import math
import unittest

from medver_pytest import pth

from tools import loader

loader.loader_init()

# ruff: noqa: E402
from on_the_fly_stats import OTFStats  # pylint: disable=wrong-import-position


# -------------------
class TestTp002(unittest.TestCase):

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
    def test_tp_002_average(self):
        pth.proto.protocol('tp-002', 'tests based on Average')

        pth.proto.step('verify initial values')
        otfs = OTFStats()
        otfs.create_average('avg1')

        pth.proto.step('verify initial values are set correctly')
        pth.ver.verify_equal(0, otfs.average['avg1'].num_elements, reqids=['SRS-020'])
        pth.ver.verify_true(math.isnan(otfs.average['avg1'].average), reqids=['SRS-020'])

        pth.proto.step('verify a single value is reported correctly')
        otfs.update_average('avg1', 10)
        pth.ver.verify_equal(1, otfs.average['avg1'].num_elements, reqids=['SRS-021'])
        pth.ver.verify_equal(10.0, otfs.average['avg1'].average, reqids=['SRS-022'])

        pth.proto.step('verify a multiple values are reported correctly')
        otfs.update_average('avg1', 20)
        pth.ver.verify_equal(2, otfs.average['avg1'].num_elements, reqids=['SRS-021'])
        pth.ver.verify_equal(15.0, otfs.average['avg1'].average, reqids=['SRS-022'])

        pth.proto.step('verify after init(), initial values are reported correctly')
        otfs.average['avg1'].init()
        pth.ver.verify_equal(0, otfs.average['avg1'].num_elements, reqids=['SRS-023', 'SRS-020'])
        pth.ver.verify_true(math.isnan(otfs.average['avg1'].average), reqids=['SRS-023', 'SRS-020'])
