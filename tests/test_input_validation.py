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

    def test_missing_or_blank_review_text_raises_clear_error(self):
        invalid_values = [None, float("nan"), pd.NA, "", "   "]

        for invalid_text in invalid_values:
            with self.subTest(value=repr(invalid_text)):
                reviews = pd.DataFrame({
                    "review": [
                        "The hotel room was clean and comfortable.",
                        "The friendly staff served a delicious breakfast.",
                        invalid_text,
                    ]
                })

                with self.assertRaisesRegex(
                    ValueError,
                    "missing or blank",
                ):
                    ChordReviews(
                        reviews,
                        text_column="review",
                        min_pair_frequency=1,
                    )

    def test_error_reports_number_of_invalid_reviews(self):
        reviews = pd.DataFrame({
            "review": [
                "  The hotel room was comfortable.  ",
                None,
                "",
                " \t\n ",
            ]
        })

        with self.assertRaises(ValueError) as caught:
            ChordReviews(reviews, text_column="review")

        self.assertIn(
            "3 row(s) with missing or blank review text",
            str(caught.exception),
        )