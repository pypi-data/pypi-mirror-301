"""This module contains tests to test the signal processing utilities."""

import unittest
import logging
from signal_processing_utilities import process_signal

logging.basicConfig(level=logging.DEBUG)


class TestProcessSignal(unittest.TestCase):
    """This class is used to define tests to test the process signal module.

    Args:
        unittest (module): This is the module that enables unittests.
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test01_compare_for_equality(self):
        logging.info(
            "test01: This is a test to ensure that the byte strings are of "
            + "equal length. The lengths are unequal and the return value "
            + "is intended to be 'False'."
        )
        byte_string1 = b"010101010001"
        byte_string2 = b"100101011001101"
        self.assertEqual(
            process_signal.compare_for_equality(byte_string1, byte_string2), False
        )

    def test02_compare_for_equality(self):
        logging.info(
            "test02: This is a test to ensure that the byte strings are of "
            + "equal value. The values are unequal and the return value "
            + "is intended to be 'False'."
        )
        byte_string1 = b"010101010001"
        byte_string2 = b"100101011001"
        self.assertEqual(
            process_signal.compare_for_equality(byte_string1, byte_string2), False
        )

    def test03_compare_for_equality(self):
        logging.info(
            "test03: This is a test to ensure that the byte strings are of "
            + "equal type. The types are unequal and the return value "
            + "is intended to be 'False'."
        )
        byte_string1 = "010101010001"
        byte_string2 = b"100101011001"
        self.assertEqual(
            process_signal.compare_for_equality(byte_string1, byte_string2), False
        )
