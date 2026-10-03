import unittest

import pandas as pd

from ChordReviewsVis import ChordReviews
from ChordReviewsVis.ChordReviews import _prepare_review_data


class TestLemmatization(unittest.TestCase):
    def test_auxiliary_verbs_do_not_create_chart_terms(self):
        reviews = pd.DataFrame({
            "review": [
                "The hotel room was good.",
                "The hotel rooms were good.",
            ]
        })

        plot = ChordReviews(
            reviews,
            text_column="review",
            min_pair_frequency=1,
            stemming=False,
            lemmatization=True,
        )

        terms = set(plot.data["source"]) | set(plot.data["target"])

        self.assertIn("hotel", terms)
        self.assertIn("room", terms)

        for unwanted in ("wa", "was", "were", "be"):
            with self.subTest(term=unwanted):
                self.assertNotIn(unwanted, terms)

        pair = plot.data.loc[
            (plot.data["source"] == "hotel")
            & (plot.data["target"] == "room")
        ].iloc[0]

        self.assertEqual(pair["weight"], 2)

    def test_lemmatization_uses_verb_and_noun_roles(self):
        original = "The guests were enjoying the rooms."
        reviews = pd.DataFrame({"review": [original]})

        sentences, _ = _prepare_review_data(
            df=reviews,
            text_column="review",
            stopwords_to_add=[],
            stemming=False,
            lemmatization=True,
            words_to_replace={},
        )

        normalized_words = set(
            sentences.iloc[0]["BaseText"].split()
        )

        self.assertTrue(
            {"guest", "be", "enjoy", "room"}.issubset(normalized_words)
        )
        self.assertTrue(
            {"guests", "were", "enjoying", "rooms"}.isdisjoint(
                normalized_words
            )
        )

        self.assertNotIn("be", sentences.iloc[0]["WordsCleaned"])
        self.assertEqual(sentences.iloc[0]["OriginalText"], original)