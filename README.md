# ChordReviewsVis

**A research-led data product for turning large volumes of customer reviews into explorable patterns of topics, relationships, and sentiment.**

ChordReviewsVis helps analysts investigate **what customers talk about together**, rather than reducing feedback to isolated keywords or aggregate ratings.

It transforms English-language review text into chord diagrams combining:

- term frequency,
- relationships between nearby words,
- and approximate sentiment signals.

The product hypothesis was that bringing these signals into a single exploratory view could help analysts identify themes worth investigating further and communicate those patterns to product and marketing teams.

Developed by **Félix José Funes** for a master's dissertation at **NOVA Information Management School**, supervised by **Prof. Nuno António**.

| | |
| --- | --- |
| **Target user** | Analysts and researchers working with customer-review data |
| **Problem** | Large volumes of qualitative feedback are difficult to explore systematically |
| **Product hypothesis** | Combining frequency, relationships and sentiment can make recurring patterns easier to discover |
| **Solution** | Configurable Python package generating chord visualizations from review datasets |
| **Evaluation** | Applied to 165,000+ reviews across tourism, retail and media |

[Problem](#the-problem) · [My contribution](#my-contribution) · [Decisions](#product-design-decisions) · [Evaluation](#evaluation-and-findings) · [Roadmap](#where-i-would-take-it-next) · [Getting started](#getting-started)

![Chord diagram generated from IMDb movie reviews](https://raw.githubusercontent.com/felix-funes/ChordReviewsVis/refs/heads/main/Sample%20Chord%20Plot%20-%20IMDB%20Dataset%20-%20Stop%20words%20and%20larger%20size%20v2.svg)

*IMDb review example. Connections represent selected word pairs; colours summarise sentiment from the original sentences containing those pairs.*

## The problem

Customer reviews contain information that aggregate metrics cannot explain.

A rating might show that customers are dissatisfied, but not **what aspects of the experience repeatedly appear together, how customers describe them, or which themes deserve further investigation**.

Analysts can inspect reviews manually, but that becomes impractical as the volume grows.

Existing approaches also solve different parts of the problem:

- **ratings** summarise overall outcomes but provide little explanation;
- **word clouds** show frequency but not relationships between concepts;
- **word trees and contextual tools** preserve more language context but can become difficult to use across large datasets.

Previous research also suggests that review analysis already plays an important role in business decision-making. For example, a 2015 study by [Torres et al.](https://stars.library.ucf.edu/ucfscholar/542/) reported that 90% of the hotel general managers surveyed read online reviews daily and used them to identify recurring complaints and plan recovery strategies.

This created the opportunity explored by the project:

> **Could one exploratory view combine frequency, word relationships and sentiment while remaining configurable enough to work across different review domains?**

ChordReviewsVis builds on previous research into chord visualizations of online reviews by [António et al. (2018)](https://doi.org/10.1007/s40558-018-0107-x).

## Users and job to be done

The primary users are **analysts and researchers working with review data in Python**. Product and marketing teams are the downstream audience for their findings.

The intended job is allowing users to **identify meaningful patterns in large volumes of feedback and use them to focus deeper investigation.**

## Product hypothesis

The project tested the hypothesis that analysts could gain a richer exploratory view of customer feedback by combining three signals that are often examined separately:

**frequency + relationships + sentiment**

Instead of automatically classifying every review into predefined topics, the product deliberately supports **exploration**.

This was an important scope decision.

The goal was obtaining recurring relationships in how customers talk so the user knows where to investigate.

## My contribution

I took the project from problem definition through implementation and evaluation.

### Discovery and research

- Reviewed academic and practitioner approaches to online-review analysis, NLP and visualization.
- Identified limitations of frequency-only and aggregate approaches.
- Defined the research question and intended analytical workflow.

### Product and analytical design

- Designed a workflow combining term frequency, word relationships and sentiment.
- Defined configurable preprocessing options for different domains.
- Chose an exploratory rather than prescriptive product approach.
- Designed evaluation scenarios across different review categories.

### Implementation

- Built the review-processing and visualization workflow in Python.
- Packaged the method so it could be reused with different datasets.
- Added configurable stop words, vocabulary replacement, stemming, lemmatization and pair-frequency thresholds.

### Evaluation and iteration

- Evaluated the prototype using three review datasets.
- Identified analytical and usability limitations.
- Later revisited the original research prototype to improve reliability, validation, testability and maintainability.

## Product design decisions

Several important decisions were product decisions rather than purely technical choices.

| Decision | Rationale | Trade-off |
| --- | --- | --- |
| **Build an exploratory tool rather than an automated insight generator** | Analysts should inspect and interpret evidence rather than receive unsupported conclusions from the system. | Requires more user involvement and analytical judgement. |
| **Use chord diagrams rather than only frequency-based visualization** | Show which concepts occur together while also communicating frequency and sentiment. | Dense diagrams become harder to interpret as the number of relationships increases. |
| **Package the workflow in Python rather than initially build a UI** | Prioritise analytical reuse and validation of the core method before investing in an interface. | Users need Python skills and a suitable environment. |
| **Expose preprocessing configuration** | Different domains contain different vocabulary and noise, so analysts need control over how text is processed. | More configuration increases cognitive load and makes results sensitive to user choices. |
| **Limit the chart to the 50 most frequent qualifying pairs** | Keep the visualization interpretable rather than displaying every possible relationship. | Less frequent but potentially meaningful relationships may be hidden. |
| **Make thresholds configurable** | Dataset sizes differ substantially, so a fixed threshold would not work equally well everywhere. | Users need to understand how the threshold affects the output. |
| **Treat the visualization as a starting point for investigation** | Co-occurrence and lexical sentiment are signals, not proof of customer intent or business causality. | The tool cannot replace qualitative inspection of the original reviews. |

## Analytical and technical decisions

The underlying analytical behaviour also required explicit trade-offs.

| Decision | Rationale | Trade-off |
| --- | --- | --- |
| **Preserve sentence boundaries before preprocessing** | Avoid creating relationships between words that appeared in different sentences simply because punctuation was removed. | Adds preprocessing complexity. |
| **Count words within a maximum distance of two positions** | Capture relatively local relationships while allowing one intervening retained term. | Distance after filtering does not perfectly represent distance in the original sentence. |
| **Treat word pairs as unordered** | Consolidate co-occurrence.  | Directionality is lost. |
| **Filter to nouns, adjectives and adverbs** | Reduce noise and focus the visualization on more descriptive terms. | Potentially meaningful verbs and other terms may be excluded. |
| **Use VADER sentiment** | Provide a lightweight sentiment signal without requiring labelled domain-specific training data. | Lexical sentiment can miss context, negation and domain-specific meaning. |
| **Scale term frequency relative to the most frequent word** | Maintain useful visual contrast across datasets of different sizes. | Node shades cannot be compared as absolute values across datasets. |
| **Make stemming and lemmatization alternative options** | Allow users to choose between stronger reduction and more readable normalization. | Users must decide which approach is better suited to their analysis. |

## Evaluation and findings

The prototype was developed using **design science research**: creating an artifact and evaluating how well it addressed its intended purpose. The original study used an **informed argument** approach, applying the package to scenarios and assessing functionality, completeness, consistency, accuracy, performance, reliability and usability.

| Scenario | Reviews | What the demonstration surfaced |
| --- | ---: | --- |
| Tourism: European attractions on TripAdvisor | 92,120 | Relationships involving tours, guides, places and history; also used during development. |
| Retail: women's clothing e-commerce reviews | 23,486 | Recurring relationships involving fit and size. |
| Media: IMDb film reviews | 50,000 | How replacements and exclusions change the relationships visible in the chart. |

Across the three scenarios, the prototype was evaluated using **165,606 reviews**.

## What the evaluation demonstrated

The research provided evidence that:

- the same workflow could be applied across substantially different review domains;
- preprocessing configuration meaningfully changes what relationships become visible;
- the visualization can surface plausible domain-specific patterns;
- large review datasets can be reduced to a smaller set of relationships for exploratory investigation;
- frequency, relationships and approximate sentiment can be presented together in a single view.

Sentiment colours were also compared with aggregate review ratings as a plausibility check.

### What I learned

**Useful exploration requires iteration.** In the IMDb analysis, replacing “movie” with “film” consolidated the dominant topic. Excluding both terms then exposed relationships such as “give–performance”, alongside uninformative pairs such as “thing–time”. More visible relationships did not automatically mean more useful insights.

**Configuration is part of the analytical experience.** Vocabulary choices and filtering determine which patterns users see. Analysts need to inspect those effects rather than treat preprocessing as neutral.

**Reliability and usefulness require different evidence.** Regression tests help protect defined behaviours. They cannot establish whether a chart helps someone make a better analytical decision.

## Where I would take it next

I would prioritise validating user value and increasing trust before expanding the interface.

| Priority | Next step | Evidence of progress |
| --- | --- | --- |
| **1. Validate the user outcome** | Run moderated investigations with analysts; compare against frequency tables, word clouds and manual review inspection. | Task completion, time to a supported finding, interpretation accuracy and perceived usefulness. |
| **2. Add evidence inspection** | Let users select a relationship and inspect its contributing sentences and reviews. | Users can trace a pattern to supporting evidence and judge whether it holds up. |
| **3. Evaluate sentiment independently** | Build a labelled evaluation dataset for the relationships shown; compare contextual, aspect-based or LLM-assisted alternatives if needed. | Agreement with human judgements and documented failure patterns for the intended use case. |
| **4. Improve interaction** | If user research demonstrates value, add controls for thresholds, vocabulary, filtering and configuration comparison. | Users can complete investigations with less friction while interpreting the output correctly. |

These are proposed measures, not achieved results.

## Getting started

### Installation

Use a Python environment with pip and Git available:

```bash
python -m pip install "git+https://github.com/felix-funes/ChordReviewsVis.git@main"
```

The package installs its declared Python dependencies. NLTK also requires language resources; download them once in the same environment:

```bash
python -m nltk.downloader punkt_tab averaged_perceptron_tagger_eng stopwords wordnet vader_lexicon
```

See the [NLTK data installation guide](https://www.nltk.org/data.html) for resource locations and troubleshooting.

### A small example

Save the code as `example.py` and run `python example.py`, or use a notebook with the same environment.

```python
import pandas as pd
import holoviews as hv
from ChordReviewsVis import ChordReviews

reviews = pd.read_csv("https://raw.githubusercontent.com/felix-funes/ChordReviewsVis/refs/heads/main/Test%20Dataset%20-%20IMDB%20Movie%20Reviews.csv")

plot = ChordReviews(
    reviews,
    text_column="review",
    min_pair_frequency=1,
    stemming=False,
    lemmatization=True,
)

hv.save(plot, "review-patterns.svg", backend="matplotlib")
```

This saves `review-patterns.svg` in the current directory. Evaluating `plot` displays it in a notebook. See the [HoloViews export guide](https://holoviews.org/user_guide/Exporting_and_Archiving.html) for other formats.

### Preparing and adapting your data

Use one English-language review per row and provide the exact, case-sensitive text-column name. Missing, empty and whitespace-only reviews are rejected; correct or explicitly remove them before analysis. The function does not add working columns to your input DataFrame.

`min_pair_frequency=1` permits pairs from this small example. The default is `100`; choose a positive Python integer suited to your dataset and inspect the resulting relationships.

Use `stopwords_to_add=["movie", "film"]` to exclude dominant terms, or `words_to_replace={"movie": "film"}` to consolidate vocabulary. To select stemming, set `stemming=True` and `lemmatization=False`; both options cannot be enabled together.

## Technical reference

<details>
<summary><strong>Interpretation</strong></summary>

| Element | Meaning |
| --- | --- |
| Labels | Terms in the selected pairs; grammatical filtering retains nouns, adjectives and adverbs. |
| Connection weight | Counted pair occurrences, not unique reviewers. |
| Connection colour | Negative (red), neutral (blue) or positive (green) estimated sentence sentiment, averaged across pair occurrences. |
| Node shading | Term frequency relative to the most frequent term, scaled to 0–100 and rounded down. Higher values are darker. |

</details>

<details>
<summary><strong>Current limitations and verification</strong></summary>

- **English-language scope:** other languages have not been validated.
- **Interpretation:** co-occurrence does not establish meaning or causality. Source reviews require inspection.
- **Sentiment context:** every pair in a sentence receives the same sentence score, even when opinions differ by attribute. Sarcasm and domain-specific language remain difficult.
- **Configuration:** preprocessing and thresholds materially affect results. Mutable list/dictionary defaults remain a deferred maintenance improvement.
- **Verification:** 26 automated tests cover selected validation, normalization, scaling, pair-extraction and sentiment-attribution behaviours. GitHub Actions checks the installed package on Ubuntu with Python 3.14. Passing tests does not establish sentiment accuracy, usefulness to analysts or compatibility with every environment.

</details>

<details>
<summary><strong>Function reference</strong></summary>

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
| `df` | Required | pandas DataFrame containing one review per row. |
| `text_column` | Required | Exact name of the review-text column. |
| `size` | `300` | HoloViews output-size setting, not a pixel width. |
| `stopwords_to_add` | `[]` | Additional terms to exclude. |
| `stemming` | `False` | Apply English Snowball stemming; requires lemmatization to be disabled. |
| `lemmatization` | `True` | Apply WordNet lemmatization using estimated grammatical roles; requires stemming to be disabled. |
| `words_to_replace` | `{}` | Complete-word replacements after normalization, applied in dictionary order. |
| `label_text_font_size` | `12` | Font size for term labels. |
| `min_pair_frequency` | `100` | Minimum counted occurrences required for inclusion. |

**Returns:** an `hv.Chord` object. Rendering and export are separate steps.

**Errors:** invalid threshold types raise `TypeError`. Nonpositive thresholds, missing columns, empty datasets, missing or blank reviews, no qualifying pairs, and conflicting stemming/lemmatization settings raise `ValueError`. Other processing errors propagate to the caller rather than being printed and replaced with `None`.

</details>

## Feedback and licence

Questions, reproducible bug reports and ideas are welcome through [GitHub Issues](https://github.com/felix-funes/ChordReviewsVis/issues).

Created by [Félix José Funes](https://www.linkedin.com/in/felix-funes/). Released under the [MIT licence](https://github.com/felix-funes/ChordReviewsVis/blob/main/License.txt).
