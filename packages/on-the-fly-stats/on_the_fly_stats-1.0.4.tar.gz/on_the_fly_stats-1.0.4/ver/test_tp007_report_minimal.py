import unittest

from medver_pytest import pth

from tools import loader

loader.loader_init()

# ruff: noqa: E402
from on_the_fly_stats import OTFStats  # pylint: disable=wrong-import-position


# -------------------
class TestTp007(unittest.TestCase):
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
    def test_tp_007_report_minimal(self):
        pth.proto.protocol('tp-007', 'do minimal report')

        pth.proto.step('verify initial values')

        pth.proto.step('verify empty report is generated correctly')
        self._check_empty_report()

        pth.proto.step('verify report for Average is generated correctly')
        self._check_average()

        pth.proto.step('verify report for Counter is generated correctly')
        self._check_counter()

        pth.proto.step('verify report for MinMax is generated correctly')
        self._check_minmax()

        pth.proto.step('verify report for Stddev is generated correctly')
        self._check_stddev()

    # -------------------
    def _check_empty_report(self):
        otfs = OTFStats()

        self.lines = []
        otfs.set_report_writer(self._writer)
        otfs.report_minimal()
        pth.ver.verify_equal(0, len(self.lines), reqids=['SRS-011'])

    # -------------------
    def _check_average(self):
        otfs = OTFStats()

        otfs.update_average('avg0', 1)

        self.lines = []
        otfs.set_report_writer(self._writer)
        otfs.report_minimal()
        pth.ver.verify_equal('Average:', self.lines[0], reqids=['SRS-011'])
        pth.ver.verify_equal('            1.000000 avg0', self.lines[1], reqids=['SRS-011'])

    # -------------------
    def _check_counter(self):
        otfs = OTFStats()

        otfs.inc_counter('cnt0')
        otfs.dec_counter('cnt1')

        self.lines = []
        otfs.set_report_writer(self._writer)
        otfs.report_minimal()
        pth.ver.verify_equal(3, len(self.lines), reqids=['SRS-011'])
        pth.ver.verify_equal('Counters:', self.lines[0], reqids=['SRS-011'])
        pth.ver.verify_equal('              1 cnt0', self.lines[1], reqids=['SRS-011'])
        pth.ver.verify_equal('             -1 cnt1', self.lines[2], reqids=['SRS-011'])

    # -------------------
    def _check_minmax(self):
        otfs = OTFStats()

        otfs.update_min_max('mm0', 3)
        otfs.update_min_max('mm0', 4)
        otfs.update_min_max('mm1', 5.1)
        otfs.update_min_max('mm1', 6.2)

        self.lines = []
        otfs.set_report_writer(self._writer)
        otfs.report_minimal()
        pth.ver.verify_equal(3, len(self.lines), reqids=['SRS-011'])
        pth.ver.verify_equal('Min/Max:', self.lines[0], reqids=['SRS-011'])
        pth.ver.verify_equal('              3               4 mm0', self.lines[1], reqids=['SRS-011'])
        pth.ver.verify_equal('       5.100000        6.200000 mm1', self.lines[2], reqids=['SRS-011'])

    def _check_stddev(self):
        otfs = OTFStats()

        otfs.update_stddev('sd0', 1)
        otfs.update_stddev('sd0', 2)

        self.lines = []
        otfs.set_report_writer(self._writer)
        otfs.report_minimal()
        pth.ver.verify_equal(2, len(self.lines), reqids=['SRS-011'])
        pth.ver.verify_equal('Stddev', self.lines[0], reqids=['SRS-011'])
        pth.ver.verify_equal('       0.707107 sd0', self.lines[1], reqids=['SRS-011'])

    # -------------------
    def _writer(self, msg=''):
        self.lines.append(msg)
