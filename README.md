# ChordReviewsVis Package

## Overview
`ChordReviewsVis` is a Python package designed to process and visualize review data by generating chord plots. These visualizations illustrate word co-occurrence patterns and sentiment analysis, providing insights into the textual data.

This package was developed by Félix José Funes as part of his master's dissertation at Universidade Nova de Lisboa, which was supervised by Prof. Nuno António, PhD.

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

Prepare your DataFrame with a text column containing review data. Then call the `ChordReviews` function:
```
# Example DataFrame
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

## Returns
- **hv.Chord**: A chord plot visualization of word co-occurrence patterns and sentiment analysis.

## Example
```
import pandas as pd
from ChordReviewsVis import ChordReviews

# Example DataFrame
df = pd.read_csv("https://github.com/felix-funes/ChordReviewsVis/raw/main/Test%20Dataset%20-%20IMDB%20Movie%20Reviews.csv")

# Generate chord plot
chord_plot = ChordReviews(df, 'review')

# Display the plot
chord_plot.show()
```

[![chord plot example](https://raw.githubusercontent.com/felix-funes/ChordReviewsVis/875cd8a879bd8935be2176978b9aace2d7680f01/Sample%20Chord%20Plot%20-%20IMDB%20Dataset.svg)]

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

## License
This project is licensed under the MIT License.

## Contact
For any issues or inquiries, please contact the package maintainer at felixfunes96 [at] gmail [dot] com.

---

By using this package, you agree to the terms outlined in the LICENSE file included in the repository.
```