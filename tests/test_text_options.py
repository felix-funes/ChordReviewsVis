import unittest

import pandas as pd

from ChordReviewsVis import ChordReviews


class TestTextOptions(unittest.TestCase):
    def test_stemming_and_lemmatization_cannot_both_be_enabled(self):
        reviews = pd.DataFrame({
            "review": ["The clean hotel room was comfortable."]
        })

        with self.assertRaisesRegex(
            ValueError,
            "stemming and lemmatization cannot both be enabled",
        ):
            ChordReviews(
                reviews,
                text_column="review",
                min_pair_frequency=1,
                stemming=True,
                lemmatization=True,
            )

    def test_supported_combinations_produce_chart(self):
        combinations = [
            (True, False),
            (False, True),
            (False, False),
        ]

        for stemming, lemmatization in combinations:
            with self.subTest(
                stemming=stemming,
                lemmatization=lemmatization,
            ):
                reviews = pd.DataFrame({
                    "review": ["The clean hotel room was comfortable."]
                })

                plot = ChordReviews(
                    reviews,
                    text_column="review",
                    min_pair_frequency=1,
                    stemming=stemming,
                    lemmatization=lemmatization,
                )

                self.assertIsNotNone(plot)
                self.assertFalse(plot.data.empty)