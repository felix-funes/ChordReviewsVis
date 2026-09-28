import unittest

import pandas as pd

from ChordReviewsVis import ChordReviews


class TestPairFrequency(unittest.TestCase):
    def setUp(self):
        self.reviews = pd.DataFrame({
            "review": [
                "The hotel room was clean and comfortable.",
                "The friendly staff served a delicious breakfast.",
            ]
        })

    def test_nonpositive_frequency_raises_value_error(self):
        for frequency in [0, -1]:
            with self.subTest(frequency=frequency):
                with self.assertRaisesRegex(
                    ValueError,
                    "min_pair_frequency.*positive integer",
                ):
                    ChordReviews(
                        self.reviews.copy(),
                        text_column="review",
                        min_pair_frequency=frequency,
                    )

    def test_wrong_frequency_type_raises_type_error(self):
        for frequency in ["2", 1.5, 2.0, None, True, False]:
            with self.subTest(frequency=frequency):
                with self.assertRaisesRegex(
                    TypeError,
                    "min_pair_frequency.*positive integer",
                ):
                    ChordReviews(
                        self.reviews.copy(),
                        text_column="review",
                        min_pair_frequency=frequency,
                    )