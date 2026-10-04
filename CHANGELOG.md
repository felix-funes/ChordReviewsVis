# Changelog

## 0.4.0

This release refreshes the review-analysis pipeline, improves error
handling, and adds automated regression coverage.

### Analysis changes

- Count adjacent word pairs and pairs two positions apart within
  each filtered sentence.
- Preserve sentence boundaries before text cleaning.
- Calculate sentiment from original sentences and average scores
  across each word pair's occurrences.
- Scale term frequencies relative to the most frequent term.
- Use grammatical roles during lemmatization.
- Apply replacements to complete words.

### Reliability and maintenance

- Raise explanatory errors for invalid inputs and missing qualifying
  pairs instead of printing an error and returning None.
- Validate the pair-frequency threshold and reject conflicting
  stemming and lemmatization settings.
- Process reviews without adding working columns to the input DataFrame.
- Separate preprocessing, pair counting, sentiment and plotting
  into internal helpers.
- Remove tracked generated packaging files.
- Add 26 automated tests and GitHub Actions checks.

### Documentation

- Present the project as a research-led data product case study.
- Update usage instructions and explain current limitations.
- Refresh the README illustration using IMDb review data.

### Upgrade notes

- Existing charts can change because pair counting, normalization,
  scaling and sentiment calculations have changed.
- Callers should handle raised exceptions rather than checking
  whether ChordReviews returned None.
- Missing or blank reviews must be corrected or explicitly removed.
- Stemming and lemmatization cannot both be enabled.

### Known limitations

- Sentiment describes sentences containing a pair, not individual
  product attributes.
- Opposing opinions can average to a neutral-looking result.
- English-language scope and environment compatibility remain limited
  to the documented evaluation and checks.
- Dependencies are not pinned, so installing this version does not
  guarantee identical results across future dependency versions.