import unittest

import pandas as pd

from ChordReviewsVis import ChordReviews


class TestWordReplacements(unittest.TestCase):
    def test_replaces_whole_words_without_changing_longer_words(self):
        reviews = pd.DataFrame({
            "review": ["The room and bathroom were clean."]
        })

        plot = ChordReviews(
            reviews,
            text_column="review",
            min_pair_frequency=1,
            lemmatization=False,
            words_to_replace={"room": "suite"},
        )

        terms = set(plot.data["source"]) | set(plot.data["target"])

        self.assertIn("suite", terms)
        self.assertIn("bathroom", terms)
        self.assertNotIn("room", terms)
        self.assertNotIn("bathsuite", terms)