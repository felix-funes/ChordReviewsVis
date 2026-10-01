import unittest

import pandas as pd

from ChordReviewsVis.ChordReviews import _scale_frequencies


class TestFrequencyScaling(unittest.TestCase):
    def test_scales_relative_to_highest_frequency(self):
        frequencies = pd.Series(
            [12, 4, 1],
            index=["hotel", "room", "breakfast"],
        )

        expected = pd.Series(
            [100, 33, 8],
            index=["hotel", "room", "breakfast"],
        )

        result = _scale_frequencies(frequencies)

        pd.testing.assert_series_equal(result, expected)

    def test_single_word_scales_to_100(self):
        frequencies = pd.Series([5], index=["hotel"])
        expected = pd.Series([100], index=["hotel"])

        result = _scale_frequencies(frequencies)

        pd.testing.assert_series_equal(result, expected)

    def test_equal_frequencies_receive_equal_values(self):
        frequencies = pd.Series(
            [4, 4, 4],
            index=["hotel", "room", "breakfast"],
        )

        expected = pd.Series(
            [100, 100, 100],
            index=["hotel", "room", "breakfast"],
        )

        result = _scale_frequencies(frequencies)

        pd.testing.assert_series_equal(result, expected)

    def test_empty_frequencies_remain_empty(self):
        frequencies = pd.Series(dtype="int64")
        expected = pd.Series(dtype="int64")

        result = _scale_frequencies(frequencies)

        pd.testing.assert_series_equal(result, expected)