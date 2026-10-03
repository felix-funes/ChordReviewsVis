import unittest
from unittest.mock import patch

import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer

from ChordReviewsVis import ChordReviews
from ChordReviewsVis.ChordReviews import (
    _add_pair_sentiment,
    _prepare_review_data,
)


class TestSentenceSentiment(unittest.TestCase):
    def test_preserves_original_sentences_before_cleaning(self):
        reviews = pd.DataFrame({
            "review": ["The room was NOT good! The bathroom was clean."]
        })
        original_reviews = reviews.copy(deep=True)

        sentences, _ = _prepare_review_data(
            df=reviews,
            text_column="review",
            stopwords_to_add=[],
            stemming=False,
            lemmatization=False,
            words_to_replace={"room": "suite"},
        )

        self.assertEqual(
            sentences["OriginalText"].tolist(),
            [
                "The room was NOT good!",
                "The bathroom was clean.",
            ],
        )
        self.assertIn("suite", sentences.iloc[0]["BaseText"])
        pd.testing.assert_frame_equal(reviews, original_reviews)

    def test_chart_uses_original_sentence_scores_including_negation(self):
        positive = "The hotel room was good."
        negative = "The hotel room was not good."

        analyzer = SentimentIntensityAnalyzer()
        positive_score = analyzer.polarity_scores(positive)["compound"]
        negative_score = analyzer.polarity_scores(negative)["compound"]

        self.assertGreater(positive_score, 0)
        self.assertLess(negative_score, 0)

        cases = [
            (positive, positive_score, 1),
            (negative, negative_score, 1),
            (
                f"{positive} {negative}",
                (positive_score + negative_score) / 2,
                2,
            ),
        ]

        for review, expected_score, expected_weight in cases:
            with self.subTest(review=review):
                plot = ChordReviews(
                    pd.DataFrame({"review": [review]}),
                    text_column="review",
                    min_pair_frequency=1,
                )

                pair = plot.data.loc[
                    (plot.data["source"] == "hotel")
                    & (plot.data["target"] == "room")
                ].iloc[0]

                self.assertAlmostEqual(
                    pair["Sentiment Strength"], expected_score
                )
                self.assertEqual(pair["weight"], expected_weight)

    def test_average_weights_occurrences_and_combines_reversed_pairs(self):
        pairs = pd.DataFrame({
            "source": ["hotel"],
            "target": ["room"],
            "weight": [4],
        })
        original_pairs = pairs.copy(deep=True)

        sentences = pd.DataFrame({
            "OriginalText": [
                "A positive sentence.",
                "A negative sentence.",
            ],
            "FilteredText": [
                "hotel room hotel room",
                "room hotel",
            ],
        })

        with patch(
            "ChordReviewsVis.ChordReviews.SentimentIntensityAnalyzer"
        ) as analyzer_class:
            analyzer = analyzer_class.return_value
            analyzer.polarity_scores.side_effect = [
                {"compound": 0.8},
                {"compound": -0.4},
            ]

            result = _add_pair_sentiment(pairs, sentences)

            self.assertEqual(
                [call.args[0] for call in analyzer.polarity_scores.call_args_list],
                sentences["OriginalText"].tolist(),
            )

        # Three occurrences at 0.8, one at -0.4:
        # (3 * 0.8 - 0.4) / 4 = 0.5
        self.assertAlmostEqual(result.iloc[0]["Sentiment Strength"], 0.5)
        self.assertEqual(result.iloc[0]["Polarity"], "Positive")
        self.assertEqual(result.iloc[0]["weight"], 4)
        pd.testing.assert_frame_equal(pairs, original_pairs)

    def test_unrelated_sentence_does_not_affect_pair_sentiment(self):
        pairs = pd.DataFrame({
            "source": ["hotel"],
            "target": ["room"],
            "weight": [1],
        })
        sentences = pd.DataFrame({
            "OriginalText": ["Positive room.", "Negative breakfast."],
            "FilteredText": ["hotel room", "breakfast staff"],
        })

        with patch(
            "ChordReviewsVis.ChordReviews.SentimentIntensityAnalyzer"
        ) as analyzer_class:
            analyzer_class.return_value.polarity_scores.side_effect = [
                {"compound": 0.8},
                {"compound": -0.9},
            ]
            result = _add_pair_sentiment(pairs, sentences)

        self.assertAlmostEqual(result.iloc[0]["Sentiment Strength"], 0.8)

    def test_polarity_thresholds_are_preserved(self):
        pairs = pd.DataFrame({
            "source": ["hotel"],
            "target": ["room"],
            "weight": [1],
        })
        sentences = pd.DataFrame({
            "OriginalText": ["A sentence."],
            "FilteredText": ["hotel room"],
        })

        cases = [
            (-0.34, "Negative"),
            (-0.33, "Neutral"),
            (0.0, "Neutral"),
            (0.33, "Neutral"),
            (0.34, "Positive"),
        ]

        for score, expected_polarity in cases:
            with self.subTest(score=score):
                with patch(
                    "ChordReviewsVis.ChordReviews.SentimentIntensityAnalyzer"
                ) as analyzer_class:
                    analyzer_class.return_value.polarity_scores.return_value = {
                        "compound": score
                    }
                    result = _add_pair_sentiment(pairs, sentences)

                self.assertEqual(
                    result.iloc[0]["Polarity"], expected_polarity
                )