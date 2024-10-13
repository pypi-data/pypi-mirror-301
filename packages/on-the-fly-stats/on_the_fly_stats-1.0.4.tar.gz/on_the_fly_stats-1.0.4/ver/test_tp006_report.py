import unittest

from medver_pytest import pth

from tools import loader

loader.loader_init()

# ruff: noqa: E402
from on_the_fly_stats import OTFStats  # pylint: disable=wrong-import-position


# -------------------
class TestTp006(unittest.TestCase):
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
    def test_tp_006_report(self):
        pth.proto.protocol('tp-006', 'do full report')

        pth.proto.step('verify initial values')

        pth.proto.step('verify empty report is generated correctly')
        otfs = OTFStats()
        self.lines = []
        otfs.set_report_writer(self._writer)
        otfs.report()
        pth.ver.verify_equal(2, len(self.lines), reqids=['SRS-010'])
        pth.ver.verify_equal('', self.lines[0], reqids=['SRS-010'])
        pth.ver.verify_equal('---- Stats:', self.lines[1], reqids=['SRS-010'])

        pth.proto.step('verify report for Average is generated correctly')
        otfs = OTFStats()
        otfs.update_average('avg0', 1)
        self._check_average(otfs)

        pth.proto.step('verify report for Counter is generated correctly')
        otfs = OTFStats()
        otfs.inc_counter('cnt0')
        otfs.dec_counter('cnt1')
        self._check_counter(otfs)

        pth.proto.step('verify report for MinMax is generated correctly')
        otfs = OTFStats()
        otfs.update_min_max('mm0', 3)
        otfs.update_min_max('mm0', 4)
        otfs.update_min_max('mm1', 5.1)
        otfs.update_min_max('mm1', 6.2)
        self._check_minmax(otfs)

        pth.proto.step('verify report for Stddev is generated correctly')
        otfs = OTFStats()
        otfs.update_stddev('sd0', 1)
        otfs.update_stddev('sd0', 2)
        self._check_stddev(otfs)

    # -------------------
    def _check_average(self, otfs):
        self.lines = []
        otfs.set_report_writer(self._writer)
        otfs.report()

        pth.ver.verify_equal(7, len(self.lines), reqids=['SRS-010'])
        pth.ver.verify_equal('', self.lines[0], reqids=['SRS-010'])
        pth.ver.verify_equal('---- Stats:', self.lines[1], reqids=['SRS-010'])
        pth.ver.verify_equal('', self.lines[2], reqids=['SRS-010'])
        pth.ver.verify_equal('             Average statistic', self.lines[3], reqids=['SRS-010'])
        pth.ver.verify_equal('     --------------- ------------------------------------------------------------------',
                             self.lines[4], reqids=['SRS-010'])
        pth.ver.verify_equal('            1.000000 avg0', self.lines[5], reqids=['SRS-010'])
        pth.ver.verify_equal('     >>> end of Averages', self.lines[6], reqids=['SRS-010'])

    # -------------------
    def _check_counter(self, otfs):
        self.lines = []
        otfs.set_report_writer(self._writer)
        otfs.report()
        pth.ver.verify_equal(8, len(self.lines), reqids=['SRS-010'])
        pth.ver.verify_equal('', self.lines[0], reqids=['SRS-010'])
        pth.ver.verify_equal('---- Stats:', self.lines[1], reqids=['SRS-010'])
        pth.ver.verify_equal('', self.lines[2], reqids=['SRS-010'])
        pth.ver.verify_equal('               Total statistic', self.lines[3], reqids=['SRS-010'])
        pth.ver.verify_equal('     --------------- ------------------------------------------------------------------',
                             self.lines[4], reqids=['SRS-010'])
        pth.ver.verify_equal('                   1 cnt0', self.lines[5], reqids=['SRS-010'])
        pth.ver.verify_equal('                  -1 cnt1', self.lines[6], reqids=['SRS-010'])
        pth.ver.verify_equal('     >>> end of counters', self.lines[7], reqids=['SRS-010'])

    # -------------------
    def _check_minmax(self, otfs):
        self.lines = []
        otfs.set_report_writer(self._writer)
        otfs.report()
        pth.ver.verify_equal(8, len(self.lines), reqids=['SRS-010'])
        pth.ver.verify_equal('', self.lines[0], reqids=['SRS-010'])
        pth.ver.verify_equal('---- Stats:', self.lines[1], reqids=['SRS-010'])
        pth.ver.verify_equal('', self.lines[2], reqids=['SRS-010'])
        pth.ver.verify_equal('                 Min             Max statistic', self.lines[3], reqids=['SRS-010'])
        pth.ver.verify_equal(
            '     --------------- --------------- ------------------------------------------------------------------',
            self.lines[4], reqids=['SRS-010'])
        pth.ver.verify_equal('                   3               4 mm0', self.lines[5], reqids=['SRS-010'])
        pth.ver.verify_equal('            5.100000        6.200000 mm1', self.lines[6], reqids=['SRS-010'])
        pth.ver.verify_equal('     >>> end of min/max', self.lines[7], reqids=['SRS-010'])

    # -------------------
    def _check_stddev(self, otfs):
        self.lines = []
        otfs.set_report_writer(self._writer)
        otfs.report()
        pth.ver.verify_equal(7, len(self.lines), reqids=['SRS-010'])
        pth.ver.verify_equal('', self.lines[0], reqids=['SRS-010'])
        pth.ver.verify_equal('---- Stats:', self.lines[1], reqids=['SRS-010'])
        pth.ver.verify_equal('', self.lines[2], reqids=['SRS-010'])
        pth.ver.verify_equal('              StdDev statistic', self.lines[3], reqids=['SRS-010'])
        pth.ver.verify_equal('     --------------- ------------------------------------------------------------------',
                             self.lines[4], reqids=['SRS-010'])
        pth.ver.verify_equal('            0.707107 sd0', self.lines[5], reqids=['SRS-010'])
        pth.ver.verify_equal('     >>> end of StdDev', self.lines[6], reqids=['SRS-010'])

    # -------------------
    def _writer(self, msg=''):
        self.lines.append(msg)
