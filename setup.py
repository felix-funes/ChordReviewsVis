from setuptools import setup, find_packages

# Package meta-data.
NAME = "ChordReviewsVis"
URL = "http://github.com/feature-engine/feature_engine"
AUTHOR = "Félix José Funes"

setup(
    name='ChordReviewsVis',
    version='0.2.6',
    description="Process reviews data, apply text preprocessing, and generate a chord plot visualization showing word co-occurrence patterns and sentiment analysis.",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'nltk',
        'beautifulsoup4',
        'networkx',
        'matplotlib',
        'holoviews'
    ],
    keywords=['customer reviews', 'sentiment analysis', 'chord plot'],
)