import unittest

import pandas as pd

from ChordReviewsVis import ChordReviews


class TestInputValidation(unittest.TestCase):
    def test_missing_text_column_raises_clear_error(self):
        reviews = pd.DataFrame({
            "comment": ["The hotel room was clean."]
        })

        with self.assertRaisesRegex(
            ValueError,
            "text_column.*review",
        ):
            ChordReviews(reviews, text_column="review")

    def test_empty_dataset_raises_clear_error(self):
        reviews = pd.DataFrame({"review": []})

        with self.assertRaisesRegex(
            ValueError,
            "at least one review",
        ):
            ChordReviews(reviews, text_column="review")