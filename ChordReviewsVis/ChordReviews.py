import pandas as pd
import numpy as np
import nltk
from bs4 import BeautifulSoup
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.probability import FreqDist
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from collections import Counter
from nltk.sentiment import SentimentIntensityAnalyzer
import holoviews as hv
from holoviews import opts, dim

def _scale_frequencies(frequencies):
    """Scale positive word counts relative to their maximum, rounding down."""
    if frequencies.empty:
        return frequencies.astype("int64")

    highest_frequency = frequencies.max()

    return (
        frequencies / highest_frequency * 100
    ).astype("int64")

def _count_word_pairs(texts, max_distance, threshold):
    """Count unordered word pairs within each filtered sentence.

    Args:
        texts: Iterable of strings, each representing one filtered sentence.
        max_distance: Maximum positional distance between paired words.
        threshold: Minimum total occurrence count required to retain a pair.

    Returns:
        List of (pair, count) tuples in descending frequency order.
        Identical-word pairs are excluded.
    """
    word_pairs_counter = Counter()

    for text in texts:
        words = text.split()

        for distance in range(1, max_distance + 1):
            for i in range(len(words) - distance):
                first_word = words[i]
                second_word = words[i + distance]

                if first_word != second_word:
                    pair = tuple(sorted((first_word, second_word)))
                    word_pairs_counter[pair] += 1

    filtered_word_pairs_counter = Counter({
        pair: count
        for pair, count in word_pairs_counter.items()
        if count >= threshold
    })

    return filtered_word_pairs_counter.most_common()

def _add_pair_sentiment(word_pairs):
    """Return word pairs with constructed-phrase sentiment and polarity."""
    result = word_pairs.copy()
    analyzer = SentimentIntensityAnalyzer()

    def score_pair(row):
        text = f"The {row['target']} is {row['source']}."
        return analyzer.polarity_scores(text)["compound"]

    result["Sentiment Strength"] = result.apply(score_pair, axis=1)

    result["Polarity"] = np.where(
        result["Sentiment Strength"] < -0.33,
        "Negative",
        np.where(
            result["Sentiment Strength"] <= 0.33,
            "Neutral",
            "Positive",
        ),
    )

    return result

def _build_chord_plot(
    word_pairs,
    frequencies,
    size,
    label_text_font_size,
):
    """Build a chord chart from scored pairs and scaled term frequencies."""
    gray_scale = {}

    for value in range(101):
        gray_value = int(((100 - value) / 100) * 255)
        gray_scale[value] = "#{:02x}{:02x}{:02x}".format(
            gray_value,
            gray_value,
            gray_value,
        )

    gray_scale["nan"] = "#000000"

    color_map = (
        frequencies["Frequency_Scaled"]
        .map(gray_scale)
        .dropna()
        .to_dict()
    )

    hv.extension("matplotlib")
    hv.output(fig="svg", size=size)

    def rotate_label(plot, element):
        for annotation in plot.handles["labels"]:
            annotation.set_size(label_text_font_size)
            angle = annotation.get_rotation()

            if 90 < angle < 270:
                annotation.set_rotation(180 + angle)
                annotation.set_horizontalalignment("right")

    return hv.Chord(word_pairs).opts(
        opts.Chord(
            edge_cmap={
                "Negative": "#fe7f81",
                "Neutral": "#93e0e6",
                "Positive": "#c2ffc1",
            },
            edge_color="Polarity",
            labels="index",
            node_cmap=color_map,
            node_color="index",
            hooks=[rotate_label],
            node_size=0,
        )
    )

def _prepare_review_data(
    df,
    text_column,
    stopwords_to_add,
    stemming,
    lemmatization,
    words_to_replace,
):
    """Prepare sentence-level text and scaled term frequencies."""
    # Text preprocessing function
    def text_preprocess(raw_text, remove_HTML=True, chars_to_remove=r'\?|\.|\!|\;|\.|\"|\,|\(|\)|\&|\:|\-|\\|\/|\[|\]|\{|\}|\=|\+|\*|\%|\$|\@|\#|\_|\`|\~|\>|\<|\^|\|', 
                        remove_numbers=True, remove_line_breaks=False, 
                        special_chars_to_remove=r'[^\x00-\xfd]', convert_to_lower=True, 
                        remove_consecutive_spaces=True, remove_urls=True, stemming=stemming):
        if type(raw_text) != str:
            raw_text = str(raw_text)
        proc_text = raw_text

        if proc_text == '':
            return proc_text
    
        # Define function to remove URLs from text    
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        if remove_urls:
            # Convert the input to string
            if not isinstance(raw_text, str):
                raw_text = str(raw_text)
            # Remove URLs from text
            proc_text = url_pattern.sub('', raw_text)

        # Remove HTML
        if remove_HTML:
            proc_text = BeautifulSoup(proc_text, 'html.parser').get_text()
    
        if stemming:
            stemmer = SnowballStemmer("english")
            proc_text = ' '.join([stemmer.stem(word) for word in word_tokenize(proc_text) if word.isalnum()])
            
        if lemmatization:
            lemmatizer = WordNetLemmatizer()
            # Tokenize the text into words, filter out non-alphanumeric words, and lemmatize each word
            proc_text = ' '.join([lemmatizer.lemmatize(word) for word in word_tokenize(proc_text) if word.isalnum()])

        # Remove punctuation and other special characters
        if len(chars_to_remove) > 0:
            proc_text = re.sub(chars_to_remove, ' ', proc_text)

        # Remove numbers
        if remove_numbers:
            proc_text = re.sub(r'\d+', ' ', proc_text)

        # Remove line breaks
        if remove_line_breaks:
            proc_text = proc_text.replace('\n', ' ').replace('\r', '')

        # Remove special characters
        if len(special_chars_to_remove) > 0:
            proc_text = re.sub(special_chars_to_remove, ' ', proc_text)

        # Normalize to lower case
        if convert_to_lower:
            proc_text = proc_text.lower()

        # Replace multiple consecutive spaces with just one space
        if remove_consecutive_spaces:
            proc_text = re.sub(' +', ' ', proc_text)

        # Replace complete words without changing parts of longer words.
        for word, replacement in words_to_replace.items():
            pattern = r"\b" + re.escape(word) + r"\b"
            proc_text = re.sub(
                pattern,
                lambda match: replacement,
                proc_text,
            )

        return proc_text

    # Tokenize words function
    def tokenize_words(words):
        if type(words) != str or word_tokenize(words) == '':
            return np.nan
        else:
            return word_tokenize(words)

    # Function to remove stop words
    def remove_stop_words(text, stop_words):
        if type(text) == list:
            return [w for w in text if w not in stop_words]
        else:
            return np.nan

    # Split reviews into sentences before cleaning removes punctuation.
    sentence_rows = []

    for review_id, review in df[text_column].items():
        for sentence in sent_tokenize(str(review)):
            sentence_rows.append({
                "RevID": review_id,
                "BaseText": text_preprocess(sentence),
            })

    sentences = pd.DataFrame(
        sentence_rows,
        columns=["RevID", "BaseText"],
    )

    # Get words
    sentences['Words'] = sentences['BaseText'].apply(tokenize_words)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    stop_words.add("n't")
    stop_words.update(stopwords_to_add)
    sentences['WordsCleaned'] = sentences['Words'].apply(remove_stop_words, stop_words=stop_words)

    # Compute term frequency distribution
    fdist = FreqDist()
    for review in sentences['WordsCleaned']:
        for term in review:
            fdist[term] += 1

    # Transform results to a sorted dataframe
    df_fdist = pd.DataFrame.from_dict(fdist, orient='index', columns=['Frequency'])
    df_fdist.index.name = 'Term'
    df_fdist = df_fdist.sort_values(by='Frequency', ascending=False)

    # Scale the frequency of each word to a 0-100 scale
    df_fdist["Frequency_Scaled"] = _scale_frequencies(
        df_fdist["Frequency"]
    )

    # Preprocess text for word co-occurrence
    sentences['ProcessedText'] = sentences['WordsCleaned'].apply(lambda words: ' '.join(words))

    # Filter words that are not nouns, adjectives, or adverbs
    def filter_grammatical_words(text):
        words = text
        pos_tags = pos_tag(words)

        filtered_words = []
        for word, tag in pos_tags:
            if tag.startswith('N') or tag.startswith('J') or tag.startswith('R'):
                filtered_words.append(word)

        return ' '.join(filtered_words)

    sentences['FilteredText'] = sentences['WordsCleaned'].apply(filter_grammatical_words)
    return sentences, df_fdist


def ChordReviews(df, text_column, size=300, stopwords_to_add=[], stemming=False, lemmatization=True, words_to_replace={}, label_text_font_size=12, min_pair_frequency=100):
    """
    Process reviews data, apply text preprocessing, and generate a chord plot visualization showing word co-occurrence patterns and sentiment analysis.

    Args:
    df (pandas.DataFrame): DataFrame containing review data.
    text_column (str): Name of the column containing the text data.
    size (int, optional): Size of the output chord plot (default is 300).
    stopwords_to_add (list, optional): Additional stopwords to be included in the stop words set (default is []).
    stemming (bool, optional): Whether to apply stemming (default is False).
        Cannot be enabled together with lemmatization.
    lemmatization (bool, optional): Whether to apply lemmatization
        (default is True). Cannot be enabled together with stemming.
    words_to_replace (dict, optional): Complete-word replacements applied after
        text normalization, in dictionary order. Keys are case-sensitive and
        should match the normalized text (default is {}).
    label_text_font_size (int, optional): Font size for the labels in the chord plot (default is 12).
    min_pair_frequency (int, optional): Minimum number of counted occurrences
        required for a word pair to appear in the chord plot. Must be a positive
        integer; booleans and floats are not accepted. Use lower thresholds for
        smaller datasets (default is 100).

    Returns:
    hv.Chord: Chord plot visualization.

    Raises:
    TypeError: If min_pair_frequency is not an integer or is a boolean.
    ValueError: If stemming and lemmatization are both enabled,
        min_pair_frequency is less than 1, text_column is missing,
        the input contains no rows, any review text is missing or blank,
        or no word pairs meet min_pair_frequency.

    Notes:
    Errors propagate to the caller instead of being printed and returning None.
    """
    if stemming and lemmatization:
        raise ValueError(
            "stemming and lemmatization cannot both be enabled. "
            "Set either stemming=False or lemmatization=False."
        )

    if isinstance(min_pair_frequency, bool) or not isinstance(
        min_pair_frequency, int
    ):
        raise TypeError(
            "min_pair_frequency must be a positive integer."
        )

    if min_pair_frequency < 1:
        raise ValueError(
            "min_pair_frequency must be a positive integer."
        )

    if text_column not in df.columns:
        raise ValueError(
            f"text_column '{text_column}' was not found in the input DataFrame. "
            "Choose a column containing review text."
        )

    if len(df.index) == 0:
        raise ValueError(
            "The input DataFrame must contain at least one review."
        )

    review_text = df[text_column]

    missing_text = review_text.isna()
    blank_text = review_text.map(
        lambda value: isinstance(value, str) and not value.strip()
    )

    invalid_text = missing_text | blank_text
    invalid_count = int(invalid_text.sum())

    if invalid_count > 0:
        raise ValueError(
            f"Column '{text_column}' contains {invalid_count} row(s) "
            "with missing or blank review text. "
            "Fill in or explicitly remove these rows before calling ChordReviews."
        )

    sentences, df_fdist = _prepare_review_data(
        df=df,
        text_column=text_column,
        stopwords_to_add=stopwords_to_add,
        stemming=stemming,
        lemmatization=lemmatization,
        words_to_replace=words_to_replace,
    )

    # Include adjacent pairs and distance-two pairs after word filtering.
    word_pairs_at_distance = _count_word_pairs(
        sentences["FilteredText"],
        max_distance=2,
        threshold=min_pair_frequency,
    )

    if not word_pairs_at_distance:
        raise ValueError(
            f"No word pairs meet min_pair_frequency={min_pair_frequency}. "
            "Try lowering min_pair_frequency or check the input reviews."
        )

    # Convert to DataFrame
    df_word_pairs = pd.DataFrame([{'source': pair[0], 'target': pair[1], 'weight': count} for pair, count in word_pairs_at_distance])

    # Add sentiment scores and select the most frequent pairs.
    df_word_pairs = _add_pair_sentiment(df_word_pairs)
    df_word_pairs = df_word_pairs.head(50)

    return _build_chord_plot(
        word_pairs=df_word_pairs,
        frequencies=df_fdist,
        size=size,
        label_text_font_size=label_text_font_size,
    )