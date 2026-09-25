# ChordReviewsVis

**A research-led data product case study: exploring customer feedback with NLP and visualization.**

ChordReviewsVis turns English-language reviews into chord diagrams that bring recurring word relationships and sentiment indicators into one view. The project explores how a reusable analysis tool can help researchers and analysts investigate customer feedback and communicate patterns to product and marketing teams.

Developed by **Félix José Funes** for a master's dissertation at **NOVA Information Management School**, supervised by **Prof. Nuno António**.

**Project at a glance:** Python package · NLP and sentiment analysis · Evaluation across tourism, retail and media · Research prototype

[Problem](#why-this-project-exists) · [My contribution](#my-contribution) · [Design decisions](#design-decisions-and-trade-offs) · [Evaluation](#evaluation-and-findings) · [Getting started](#getting-started)

![Chord diagram generated from IMDb movie reviews](https://raw.githubusercontent.com/felix-funes/ChordReviewsVis/refs/heads/docs/product-readme/Sample%20Chord%20Plot%20-%20IMDB%20Dataset%20-%20Stop%20words%20and%20larger%20size.svg)

*Example from the original project. Connections represent selected word pairs and colours indicate estimated sentiment.*

## Why this project exists

Customer feedback already informs business decisions. A 2015 study by [Torres et al.](https://stars.library.ucf.edu/ucfscholar/542/) reported that **90% of the hotel general managers surveyed read online reviews daily**. Managers used this feedback to identify recurring complaints and plan recovery strategies.

The challenge is extracting useful meaning from large volumes of unstructured text. An average rating summarises an experience without explaining it. Word clouds highlight frequent terms, while word trees show language in context; the literature review identified an opportunity to bring frequency, word relationships and sentiment together in one visualization.

The research question was how text mining and visualization could improve the discovery of insights from online reviews. ChordReviewsVis explores that question through a configurable Python package, building on prior research into chord visualizations of reviews by [António et al. (2018)](https://doi.org/10.1007/s40558-018-0107-x).

## Intended users and value

The direct users are **analysts and researchers working with review data in Python**. Product and marketing teams can use their analysis to investigate frequently discussed product attributes, customer language and potential areas for improvement.

The intended workflow is to load reviews, adapt the vocabulary and preprocessing to the domain, inspect recurring relationships, and use the original comments to investigate what those patterns mean. Understanding of this need came from the literature review and analysis of review datasets.

For example, the clothing-review analysis highlighted relationships involving **fit** and **size**. A product team could use that observation to investigate sizing guidance or examine related complaints. That is a potential application of the finding; the study did not establish that sizing guidance needed changing.

**The intended user outcome:** identify meaningful themes and relationships that help focus further investigation and communicate customer feedback. The prototype evaluation assessed progress toward this outcome through worked scenarios.

## My contribution

I took the project from research through implementation and evaluation:

- **Researched the problem and existing approaches:** reviewed online-review analysis, NLP and visualization methods to identify the opportunity for a combined view.
- **Designed and implemented the artifact:** built the preprocessing, word-pair analysis, sentiment and visualization workflow, and packaged it for reuse in Python.
- **Made the analysis configurable:** exposed vocabulary replacements, additional stop words, stemming and lemmatization so users could adapt it to different domains.
- **Evaluated and documented the results:** applied the tool across three review domains, examined its outputs and processing times, and identified limitations and directions for further research.

## Design decisions and trade-offs

The initial scope centred on a reusable, configurable exploration tool. These decisions explain how the research objective translated into the package:

| Decision | Rationale | Trade-off |
| --- | --- | --- |
| Combine NLP with chord diagrams | Bring word frequency, relationships and sentiment indicators into one view. | Dense diagrams need interpretation. |
| Package the workflow in Python | Make the method reusable across datasets and research workflows. | Direct users need Python skills and a suitable environment. |
| Use VADER, a general sentiment lexicon | Support different review domains without collecting a separate sentiment-training dataset for each one. | General lexical sentiment can miss domain meaning and context. |
| Offer custom stop words and replacements | Let users remove dominant terms and consolidate vocabulary relevant to their dataset. | Settings change which relationships become visible and require judgement. |
| Offer stemming and lemmatization | Let users choose between simpler word reduction and more linguistically readable normalisation. | Processing speed and the readability of the output need to be balanced for the task. |

The study also made a deliberate evaluation choice: **scenario-based assessment within the available time and resources**, allowing rapid iterations during early development. Evaluation with stakeholders in real settings and interactive exploration still remain as future work.

## Evaluation and findings

I developed and evaluated the prototype using **design science research**: building a tool and assessing how well it addressed its intended purpose. The evaluation used an **informed argument** approach: applying the package to concrete scenarios and assessing the outputs against functionality, completeness, consistency, accuracy, performance, reliability and usability criteria.

| Scenario | Reviews in the research dataset | What the demonstration surfaced |
| --- | ---: | --- |
| Tourism: European attractions on TripAdvisor | 92,120 | Relationships involving tours, guides, places and history. Used for development and evaluation. |
| Retail: women's clothing e-commerce reviews | 23,486 | Recurring language around fit and size. |
| Media: IMDb film reviews | 50,000 | How vocabulary replacements and exclusions change the relationships visible in the chart. |

The evaluation demonstrated applications across three domains and showed how configuration affects the output. Sentiment colours were compared with aggregate review ratings as a plausibility check. Labelled sentiment benchmarks, controlled usability studies and measured business outcomes remain outside the evidence established by this study.

## What I learned

**Useful exploration requires iteration.** In the IMDb analysis, consolidating “movie” into “film” made the dominant topic clearer. Excluding both terms then exposed other relationships, including “give–performance”, but also uninformative pairs such as “thing–time”. Producing more visible relationships did not automatically produce more useful insights.

**Configuration is part of the analytical experience.** Custom stop words and replacements helped adapt the package to different domains. The examples also showed why users need to understand how those choices shape their results.

**Early evaluation informs the next questions.** The scenarios demonstrated the approach and exposed areas for refinement. Establishing its usefulness in everyday work requires evaluation with analysts and other stakeholders in real settings.

## Where I would take it next

Based on the evaluation and a review of the current implementation, I would prioritise:

1. **Evaluate usefulness with target users.** Test whether analysts can identify and explain meaningful patterns, compare the workflow with simpler alternatives, and assess sentiment against manually labelled examples.
2. **Help users inspect the evidence.** Explore filtering, highlighting and access to source review passages, so a visible relationship can lead to closer investigation.

## Getting started

### Installation

The following instructions target the code in this GitHub repository. Use a Python environment with pip and Git available.

```bash
python -m pip install "git+https://github.com/felix-funes/ChordReviewsVis.git@main"
```

The package declares its Python dependencies, including pandas, NumPy, NLTK, Beautiful Soup, HoloViews, and Matplotlib. Python's built-in `re` module does not require a separate installation.

NLTK also needs language resources. With a current NLTK installation, download these once in the same environment:

```bash
python -m nltk.downloader punkt_tab averaged_perceptron_tagger_eng stopwords wordnet vader_lexicon
```

See the [NLTK data installation guide](https://www.nltk.org/data.html) for resource locations and troubleshooting. A tested Python and dependency compatibility matrix is not yet available for this project.

### A small example

You can use the **synthetic** reviews below to try it out. Save this code as `example.py` and run it with `python example.py`, or run it in a notebook using the same environment.

```python
import pandas as pd
import holoviews as hv
from ChordReviewsVis import ChordReviews

reviews = pd.DataFrame({
    "review": [
        "The dress has soft fabric and a comfortable fit.",
        "The shirt has soft fabric and a comfortable fit.",
        "The dress has beautiful colours and a flattering shape.",
        "The jacket has stiff fabric and an awkward fit.",
        "The shirt has poor stitching and rough fabric.",
        "The jacket has excellent quality and useful pockets.",
    ]
})

plot = ChordReviews(
    reviews.copy(),
    text_column="review",
    min_pair_frequency=1,
    stemming=False,
    lemmatization=True,
)

if plot is None:
    raise RuntimeError("No chart was created. Check the error printed above.")

hv.save(plot, "review-patterns.svg", backend="matplotlib")
```

The example requests an SVG named `review-patterns.svg` in the current working directory. In a notebook, evaluating `plot` also displays the chart. See the [HoloViews export guide](https://holoviews.org/user_guide/Exporting_and_Archiving.html) for other output formats.

`min_pair_frequency=1` allows pairs from this small dataset to appear. The default is `100`, which can exclude every pair in a small sample. Passing `reviews.copy()` protects the original DataFrame because the current function adds working columns to its input.

For your own data, use one review per row and supply the exact, case-sensitive name of the text column. Start with non-empty English strings; missing and empty inputs need stronger handling in the current implementation.

### Adapting the analysis

Use `stopwords_to_add` for frequent terms that obscure other relationships, and `words_to_replace` for text replacements relevant to your dataset. In the IMDb example, replacing "movie" with "film" consolidated the vocabulary; excluding both terms in a subsequent analysis revealed other pairs.

To use stemming, set `stemming=True` and `lemmatization=False`. Compare the readability and usefulness of the resulting terms for your task. Review the effect of each preprocessing change: removing or replacing words also changes which pairs the algorithm counts.

## Technical notes

<details>
<summary>How to read the visualization and interpret its output</summary>

| Element | Meaning |
| --- | --- |
| Labels | Terms appearing in the selected word pairs. The filter retains nouns, adjectives, and adverbs. |
| Connections | Word pairs selected by the current counting algorithm. |
| Connection weight | More occurrences produce a stronger visual connection. This is a pair-occurrence count, not a count of unique reviewers. |
| Connection colour | Red indicates negative, blue indicates neutral, and green indicates positive estimated sentiment. |
| Node shading | Intended to indicate term frequency. The current scaling has limitations; do not treat it as a calibrated frequency measure. |

The current implementation counts words **two positions apart in the filtered token sequence**, keeps pairs meeting `min_pair_frequency`, and selects up to the **50 most frequent pairs**. Preprocessing removes punctuation before sentence splitting, so these are not reliable counts of pairs occurring within original sentence boundaries.

Sentiment is calculated with VADER on a constructed phrase containing each pair, rather than on the original review passage. The resulting colours are approximate lexical signals. They do not establish how a customer felt about a specific product attribute.

</details>

<details>
<summary>Current implementation limitations</summary>

- **English-language scope:** development and evaluation used English reviews. Other languages have not been validated.
- **Context loss:** preprocessing and pair extraction can discard sentence boundaries and information needed for sentiment interpretation.
- **Visual scaling:** the current term-frequency scaling can generate values outside its intended colour range.
- **Input and error handling:** empty inputs, missing resources, or thresholds that exclude every pair can cause failures. The function currently prints an error and returns `None`.
- **Text replacement:** replacements use substring matching, so they can also affect parts of longer words.
- **Reproducibility:** compatibility testing, automated regression tests, and repeatable benchmarks are improvement priorities.

</details>

<details>
<summary>Function reference and parameters</summary>

The signature and behaviour below describe the [current implementation](https://github.com/felix-funes/ChordReviewsVis/blob/main/ChordReviewsVis/ChordReviews.py).

```python
ChordReviews(
    df,
    text_column,
    size=300,
    stopwords_to_add=[],
    stemming=False,
    lemmatization=True,
    words_to_replace={},
    label_text_font_size=12,
    min_pair_frequency=100,
)
```

| Parameter | Default | Purpose |
| --- | --- | --- |
| `df` | Required | pandas DataFrame containing the reviews. Pass a copy to protect the original. |
| `text_column` | Required | Exact name of the text column. |
| `size` | `300` | HoloViews output-size setting, passed to `hv.output(size=...)`; not a pixel width. |
| `stopwords_to_add` | `[]` | Extra terms to exclude alongside NLTK's English stop words. |
| `stemming` | `False` | Apply English Snowball stemming. Disable lemmatization when selecting this option. |
| `lemmatization` | `True` | Apply WordNet lemmatization. |
| `words_to_replace` | `{}` | Mapping of text strings to replacements, applied after lowercasing. |
| `label_text_font_size` | `12` | Font size for term labels. |
| `min_pair_frequency` | `100` | Minimum number of counted pair occurrences required for inclusion. |

**Returns:** a HoloViews `hv.Chord` object on successful construction. Rendering and export are separate steps and may reveal additional plotting issues. Processing failures print an error and return `None`.

</details>

## Feedback and licence

Questions, reproducible bug reports, and ideas for improving the analysis are welcome through [GitHub Issues](https://github.com/felix-funes/ChordReviewsVis/issues).

Created by [Félix José Funes](https://www.linkedin.com/in/felix-funes/). Released under the [MIT licence](https://github.com/felix-funes/ChordReviewsVis/blob/main/License.txt).
