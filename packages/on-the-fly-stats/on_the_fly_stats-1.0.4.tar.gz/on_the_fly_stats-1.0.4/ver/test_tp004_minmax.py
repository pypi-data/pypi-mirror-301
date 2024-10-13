import unittest

from medver_pytest import pth

from tools import loader

loader.loader_init()

# ruff: noqa: E402
from on_the_fly_stats import OTFStats  # pylint: disable=wrong-import-position


# -------------------
class TestTp004(unittest.TestCase):

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
    def test_tp_004_minmax(self):
        pth.proto.protocol('tp-004', 'tests based on Min/Max')

        pth.proto.step('verify initial values')
        otfs = OTFStats()
        otfs.create_min_max('mm1')

        pth.proto.step('verify initial values are set correctly')
        pth.ver.verify_is_none(otfs.min_max['mm1'].minimum, reqids=['SRS-060'])
        pth.ver.verify_is_none(otfs.min_max['mm1'].maximum, reqids=['SRS-060'])
        pth.ver.verify_equal(0, otfs.min_max['mm1'].num_elements, reqids=['SRS-060'])

        pth.proto.step('verify a minimum value is reported correctly')
        otfs.update_min_max('mm1', -1)
        pth.ver.verify_equal(-1, otfs.min_max['mm1'].minimum, reqids=['SRS-061'])
        pth.ver.verify_equal(-1, otfs.min_max['mm1'].maximum, reqids=['SRS-062'])
        otfs.update_min_max('mm1', -2)
        pth.ver.verify_equal(-2, otfs.min_max['mm1'].minimum, reqids=['SRS-061'])
        pth.ver.verify_equal(-1, otfs.min_max['mm1'].maximum, reqids=['SRS-062'])
        pth.ver.verify_equal(2, otfs.min_max['mm1'].num_elements, reqids=['SRS-060'])

        pth.proto.step('verify a maximum is reported correctly')
        otfs.update_min_max('mm1', 3)
        pth.ver.verify_equal(-2, otfs.min_max['mm1'].minimum, reqids=['SRS-061'])
        pth.ver.verify_equal(3, otfs.min_max['mm1'].maximum, reqids=['SRS-062'])
        pth.ver.verify_equal(3, otfs.min_max['mm1'].num_elements, reqids=['SRS-060'])

        pth.proto.step('verify after init(), initial values are reported correctly')
        otfs.min_max['mm1'].init()
        pth.ver.verify_is_none(otfs.min_max['mm1'].minimum, reqids=['SRS-063', 'SRS-060'])
        pth.ver.verify_is_none(otfs.min_max['mm1'].maximum, reqids=['SRS-063', 'SRS-060'])
        pth.ver.verify_equal(0, otfs.min_max['mm1'].num_elements, reqids=['SRS-063', 'SRS-060'])
