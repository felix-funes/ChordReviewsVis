import unittest

import pandas as pd

from ChordReviewsVis import ChordReviews


class TestPairDistance(unittest.TestCase):
    def test_counts_only_pairs_within_two_positions(self):
        reviews = pd.DataFrame({
            "review": ["Clean hotel room service."]
        })

        plot = ChordReviews(
            reviews,
            text_column="review",
            min_pair_frequency=1,
        )

        actual = {
            tuple(sorted((source, target))): weight
            for source, target, weight in plot.data[
                ["source", "target", "weight"]
            ].itertuples(index=False, name=None)
        }

        expected = {
            ("clean", "hotel"): 1,
            ("hotel", "room"): 1,
            ("room", "service"): 1,
            ("clean", "room"): 1,
            ("hotel", "service"): 1,
        }

        self.assertDictEqual(actual, expected)

    def test_repeated_adjacent_pairs_meet_frequency_threshold(self):
        reviews = pd.DataFrame({
            "review": ["Hotel room. Hotel room."]
        })

        plot = ChordReviews(
            reviews,
            text_column="review",
            min_pair_frequency=2,
        )

        actual = {
            tuple(sorted((source, target))): weight
            for source, target, weight in plot.data[
                ["source", "target", "weight"]
            ].itertuples(index=False, name=None)
        }

        self.assertDictEqual(
            actual,
            {("hotel", "room"): 2},
        )