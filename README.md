# Chord Reviews

## Overview
`ChordReviewsVis` is a Python package designed to process and visualize review data by generating chord plots. These visualizations illustrate word co-occurrence patterns and sentiment analysis, providing insights into the textual data. For this, the visualization relies on the following features:
- **Labels for each node:** The top nouns and adjectives extracted from the reviews were displayed around the graphic.
- **Label bars:** Below the labels, there is a bar whose color illustrates the words' overall frequency in reviews. The darker the color, the more frequent the word.
- **Edges:** The line connecting the words that occur together.
- **Edge thickness:** This characteristic shows how often the connected words appear in the same sentence. The more often they are together, the thicker the line is.
- **Edge color:** The color shows the overall sentiment of the words that are being connected. Red was used for negative sentiments, blue for neutral ones, and green for positive sentiments.

This package was developed by Felix Jose Funes as part of his master's dissertation at NOVA Information Management School (NOVA IMS), Universidade Nova de Lisboa, Portugal, which was supervised by Prof. Nuno Antonio, PhD.

## Installation
To install `ChordReviewsVis`, use pip:
```
pip install ChordReviewsVis
```

## Usage
First, import the necessary libraries and the `ChordReviews` function:
```
import pandas as pd
from ChordReviewsVis import ChordReviews
```

Prepare the DataFrame with a text column containing review data. Then call the `ChordReviews` function:
```
# Load DataFrame
df = pd.read_csv("filepath")

# Generate chord plot
ChordReviews(df, 'review')
```

Some datasets that can be used for this purpose are:

* [IMDB Movie Reviews](https://www.kaggle.com/datasets/atulanandjha/imdb-50k-movie-reviews-test-your-bert)
* [Women's E-Commerce Clothing Reviews](https://www.kaggle.com/datasets/nicapotato/womens-ecommerce-clothing-reviews)
* [Amazon Fine Food Reviews](https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews)

## Function Parameters
- **df** (pandas.DataFrame): DataFrame containing review data.
- **text_column** (str): Name of the column containing the text data.
- **size** (int, optional): Size of the output chord plot. Default is 300.
- **stopwords_to_add** (list, optional): Additional stopwords to include in the stop words set. Default is an empty list.
- **stemming** (bool, optional): Whether to apply stemming to words. Default is False.
- **lemmatization** (bool, optional): Whether to apply lemmatization to words. Default is True.
- **words_to_replace** (dict, optional): A dictionary where keys are words to be replaced and values are the replacements. Default is an empty dictionary.
- **label_text_font_size** (int, optional): Font size for the labels in the chord plot. Default is 12.
- **min_pair_frequency** (int, optional): Minimum number of times that each pair should appear in the data to be included in the visualization. For example, `min_pair_frequency=5` will only draw edges for word‑pairs that appear together in at least five sentences. For smaller data sets, this threshold should not be very high or nothing will be displayed. For larger ones, it's better to increase it to reduce the amount of irrelevant data. Default is 100.


## Returns
- **hv.Chord**: A chord plot visualization of word co-occurrence patterns and sentiment analysis.

## Examples 
### Basic Usage
```
# Import necessary libraries
import pandas as pd
from ChordReviewsVis import ChordReviews

# Load dataset
df = pd.read_csv("https://github.com/felix-funes/ChordReviewsVis/raw/main/Test%20Dataset%20-%20IMDB%20Movie%20Reviews.csv")

# Generate chord plot
ChordReviews(df, 'review')

```

![Chord plot example](https://raw.githubusercontent.com/felix-funes/ChordReviewsVis/6984c3720d6c3b2902a6ff70374040fe4d25f97b/Sample%20Chord%20Plot%20-%20IMDB%20Dataset%20-%20Basic%20usage.svg)

### Custom Parameters

Though lemmatization is used by default, users have the possibility of using stemming.
```
# Import necessary libraries
import pandas as pd
from ChordReviewsVis import ChordReviews

# Load dataset
df = pd.read_csv("https://github.com/felix-funes/ChordReviewsVis/raw/main/Test%20Dataset%20-%20IMDB%20Movie%20Reviews.csv")

# Generate chord plot
ChordReviews(df, 'review', stemming=True, lemmatization=False)

```
![Chord plot example with stemming](https://raw.githubusercontent.com/felix-funes/ChordReviewsVis/7b50f84045ddb126ba2a6fe5d036e86b23325625/Sample%20Chord%20Plot%20-%20IMDB%20Dataset%20-%20Stemming.svg)

To refine the visualization, it is possible to use the "stopwords_to_add" parameter to remove irrelevant words and "words_to_replace" to unify terms with the same meaning.

```
# Import necessary libraries
import pandas as pd
from ChordReviewsVis import ChordReviews

# Load dataset
df = pd.read_csv("https://github.com/felix-funes/ChordReviewsVis/raw/main/Test%20Dataset%20-%20IMDB%20Movie%20Reviews.csv")

# Generate chord plot
chord_reviews(df, 'Review', stemming=False, lemmatization=True, stopwords_to_add=["wa", "ha"], words_to_replace={"movie": "film"})
```
![Chord plot using the words_to_replace parameter](https://raw.githubusercontent.com/felix-funes/ChordReviewsVis/8335a92c77d0420a9a1eee8db509eae5cdde7af3/Sample%20Chord%20Plot%20-%20IMDB%20Dataset%20-%20Replacing%20words.svg)

Because of the prevalence of the words "film" and "movie", they may be considered stop words. It is possible to remove them using the parameter "stopwords_to_add". For presentation purposes, the final plot and label text can be resized.
```
# Import necessary libraries
import pandas as pd
from ChordReviewsVis import ChordReviews

# Load dataset
df = pd.read_csv("https://github.com/felix-funes/ChordReviewsVis/raw/main/Test%20Dataset%20-%20IMDB%20Movie%20Reviews.csv")

# Generate chord plot
chord_reviews(df, 'Review', stemming=False, lemmatization=True, stopwords_to_add=["wa", "ha", "movie", "film"], label_text_font_size=13, size=400)

```
![Large chord plot with stop words](https://raw.githubusercontent.com/felix-funes/ChordReviewsVis/8335a92c77d0420a9a1eee8db509eae5cdde7af3/Sample%20Chord%20Plot%20-%20IMDB%20Dataset%20-%20Stop%20words%20and%20larger%20size.svg)

## Dependencies
Ensure you have the following libraries installed:
- pandas
- numpy
- nltk
- BeautifulSoup
- re
- holoviews

These can be installed via pip:
```
pip install pandas numpy nltk beautifulsoup4 re holoviews
```

## Contact
For any issues or inquiries, please contact the package maintainer via [LinkedIn](https://www.linkedin.com/in/felix-funes/).

## License
```
MIT License

Copyright (c) 2024 Felix Funes

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```