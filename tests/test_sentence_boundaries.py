import unittest

import pandas as pd

from ChordReviewsVis import ChordReviews


class TestSentenceBoundaries(unittest.TestCase):
    def test_does_not_count_pairs_across_sentences(self):
        reviews = pd.DataFrame({
            "review": ["Hotel. Room. Breakfast."]
        })

        with self.assertRaisesRegex(
            ValueError,
            "No word pairs.*min_pair_frequency",
        ):
            ChordReviews(
                reviews,
                text_column="review",
                min_pair_frequency=1,
            )
    def test_preserves_pairs_within_each_sentence(self):
        reviews = pd.DataFrame({
            "review": [
                "Clean hotel room. Friendly breakfast staff."
            ]
        })

        plot = ChordReviews(
            reviews,
            text_column="review",
            min_pair_frequency=1,
        )

        pairs = {
            tuple(sorted((source, target)))
            for source, target in zip(
                plot.data["source"],
                plot.data["target"],
            )
        }

        self.assertIn(("clean", "room"), pairs)
        self.assertIn(("friendly", "staff"), pairs)

        allowed_pairs = {
            ("clean", "hotel"),
            ("clean", "room"),
            ("hotel", "room"),
            ("breakfast", "friendly"),
            ("breakfast", "staff"),
            ("friendly", "staff"),
        }

        self.assertTrue(
            pairs.issubset(allowed_pairs),
            f"Unexpected pairs across sentence boundaries: "
            f"{pairs - allowed_pairs}",
        )