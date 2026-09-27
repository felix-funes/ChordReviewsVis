import unittest

import pandas as pd

import holoviews as hv

from ChordReviewsVis import ChordReviews


class TestEmptyPairs(unittest.TestCase):
    def test_no_qualifying_pairs_raises_clear_error(self):
        reviews = pd.DataFrame({
            "review": [
                "The hotel room was clean and comfortable.",
                "The friendly staff served a delicious breakfast.",
                "The hotel location was convenient and quiet.",
            ]
        })

        with self.assertRaisesRegex(
            ValueError,
            "No word pairs.*min_pair_frequency",
        ):
            ChordReviews(
                reviews.copy(),
                text_column="review",
                min_pair_frequency=100,
            )

    def test_qualifying_pairs_produce_chart(self):
        reviews = pd.DataFrame({
            "review": [
                "The hotel room was clean and comfortable.",
                "The friendly staff served a delicious breakfast.",
                "The hotel location was convenient and quiet.",
            ]
        })

        plot = ChordReviews(
            reviews.copy(),
            text_column="review",
            min_pair_frequency=1,
        )

        self.assertIsInstance(plot, hv.Chord)
        self.assertFalse(plot.data.empty)