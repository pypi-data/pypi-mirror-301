import unittest

from medver_pytest import pth

from tools import loader

loader.loader_init()

# ruff: noqa: E402
from on_the_fly_stats import OTFStats  # pylint: disable=wrong-import-position


# -------------------
class TestTp003(unittest.TestCase):

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
    def test_tp_003_counters(self):
        pth.proto.protocol('tp-003', 'tests based on Counters')

        pth.proto.step('verify initial values')
        otfs = OTFStats()
        otfs.create_counter('cnt1')

        pth.proto.step('verify initial values are set correctly')
        pth.ver.verify_equal(0, otfs.counters['cnt1'].count, reqids=['SRS-040'])

        pth.proto.step('verify an increment is reported correctly')
        otfs.inc_counter('cnt1')
        pth.ver.verify_equal(1, otfs.counters['cnt1'].count, reqids=['SRS-041'])

        pth.proto.step('verify an decrement is reported correctly')
        otfs.dec_counter('cnt1')
        otfs.dec_counter('cnt1')
        pth.ver.verify_equal(-1, otfs.counters['cnt1'].count, reqids=['SRS-042'])

        pth.proto.step('verify after init(), initial values are reported correctly')
        otfs.counters['cnt1'].init()
        pth.ver.verify_equal(0, otfs.counters['cnt1'].count, reqids=['SRS-043', 'SRS-040'])

        pth.proto.step('verify after clear_counter(), clears only the one counter')
        otfs.init_counter('cnt2')
        otfs.init_counter('cnt3')
        otfs.inc_counter('cnt2')
        otfs.inc_counter('cnt3')
        otfs.inc_counter('cnt2')
        otfs.init_counter('cnt3')
        pth.ver.verify_equal(2, otfs.counters['cnt2'].count, reqids=['SRS-044'])
        pth.ver.verify_equal(0, otfs.counters['cnt3'].count, reqids=['SRS-044'])
