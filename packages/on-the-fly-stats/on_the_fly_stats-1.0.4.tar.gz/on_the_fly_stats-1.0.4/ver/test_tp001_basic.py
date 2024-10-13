import math
import unittest

from medver_pytest import pth

from tools import loader

loader.loader_init()

# ruff: noqa: E402
from on_the_fly_stats import OTFStats  # pylint: disable=wrong-import-position


# -------------------
class TestTp001(unittest.TestCase):

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
    def test_tp_001_basic(self):
        pth.proto.protocol('tp-001', 'basic calls')

        pth.proto.step('verify initial values')
        otfs = OTFStats()
        otfs.update_average('avg0', 1)
        otfs.inc_counter('cnt0')
        otfs.dec_counter('cnt1')
        otfs.update_min_max('mm0', 3)
        otfs.update_min_max('mm0', 4)
        otfs.update_stddev('sd0', 1)
        otfs.update_stddev('sd0', 2)

        pth.proto.step('verify Average values are set correctly')
        self._check_average(otfs)

        pth.proto.step('verify Counter values are set correctly')
        self._check_counter(otfs)

        pth.proto.step('verify MinMax values are set correctly')
        self._check_minmax(otfs)

        pth.proto.step('verify Stddev values are set correctly')
        self._check_stddev(otfs)

        pth.proto.step('verify calling create_xx() is ignored')
        otfs.create_average('avg0')
        otfs.create_counter('cnt0')
        otfs.create_counter('cnt1')
        otfs.create_min_max('mm0')
        otfs.create_stddev('sd0')

        # these have the same values as above
        self._check_all_are_same(otfs)

        pth.proto.step('verify init() resets all values')
        self._check_init(otfs)

    # --------------------
    def _check_stddev(self, otfs):
        pth.ver.verify_equal(2, otfs.stddev['sd0'].num_elements, reqids=['SRS-001'])
        pth.ver.verify_equal(1.5, otfs.stddev['sd0'].mean, reqids=['SRS-001'])
        pth.ver.verify_equal(0.5, otfs.stddev['sd0'].variance, reqids=['SRS-001'])
        pth.ver.verify_equal(0.7071067811865476, otfs.stddev['sd0'].stddev, reqids=['SRS-001'])

    # --------------------
    def _check_minmax(self, otfs):
        pth.ver.verify_equal(2, otfs.min_max['mm0'].num_elements, reqids=['SRS-001'])
        pth.ver.verify_equal(3, otfs.min_max['mm0'].minimum, reqids=['SRS-001'])
        pth.ver.verify_equal(4, otfs.min_max['mm0'].maximum, reqids=['SRS-001'])

    # --------------------
    def _check_average(self, otfs):
        pth.ver.verify_equal(1, otfs.average['avg0'].num_elements, reqids=['SRS-001'])
        pth.ver.verify_equal(1, otfs.average['avg0'].average, reqids=['SRS-001'])

    # --------------------
    def _check_counter(self, otfs):
        pth.ver.verify_equal(1, otfs.counters['cnt0'].count, reqids=['SRS-001'])
        pth.ver.verify_equal(-1, otfs.counters['cnt1'].count, reqids=['SRS-001'])

    # --------------------
    def _check_all_are_same(self, otfs):
        pth.ver.verify_equal(1, otfs.average['avg0'].num_elements, reqids=['SRS-002'])
        pth.ver.verify_equal(1, otfs.average['avg0'].average, reqids=['SRS-002'])

        pth.ver.verify_equal(1, otfs.counters['cnt0'].count, reqids=['SRS-002'])
        pth.ver.verify_equal(-1, otfs.counters['cnt1'].count, reqids=['SRS-002'])

        pth.ver.verify_equal(2, otfs.min_max['mm0'].num_elements, reqids=['SRS-002'])
        pth.ver.verify_equal(3, otfs.min_max['mm0'].minimum, reqids=['SRS-002'])
        pth.ver.verify_equal(4, otfs.min_max['mm0'].maximum, reqids=['SRS-002'])

        pth.ver.verify_equal(2, otfs.stddev['sd0'].num_elements, reqids=['SRS-002'])
        pth.ver.verify_equal(1.5, otfs.stddev['sd0'].mean, reqids=['SRS-002'])
        pth.ver.verify_equal(0.5, otfs.stddev['sd0'].variance, reqids=['SRS-002'])
        pth.ver.verify_equal(0.7071067811865476, otfs.stddev['sd0'].stddev, reqids=['SRS-002'])

    # --------------------
    def _check_init(self, otfs):
        otfs.init()
        pth.ver.verify_equal(0, otfs.average['avg0'].num_elements, reqids=['SRS-003'])
        pth.ver.verify_true(math.isnan(otfs.average['avg0'].average), reqids=['SRS-003'])

        pth.ver.verify_equal(0, otfs.counters['cnt0'].count, reqids=['SRS-003'])
        pth.ver.verify_equal(0, otfs.counters['cnt1'].count, reqids=['SRS-003'])

        pth.ver.verify_equal(0, otfs.min_max['mm0'].num_elements, reqids=['SRS-003'])
        pth.ver.verify_none(otfs.min_max['mm0'].minimum, reqids=['SRS-003'])
        pth.ver.verify_none(otfs.min_max['mm0'].maximum, reqids=['SRS-003'])

        pth.ver.verify_equal(0, otfs.stddev['sd0'].num_elements, reqids=['SRS-003'])
        pth.ver.verify_true(math.isnan(otfs.stddev['sd0'].mean), reqids=['SRS-003'])
        pth.ver.verify_true(math.isnan(otfs.stddev['sd0'].variance), reqids=['SRS-003'])
        pth.ver.verify_true(math.isnan(otfs.stddev['sd0'].stddev), reqids=['SRS-003'])
