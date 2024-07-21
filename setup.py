from setuptools import setup, find_packages
from pathlib import Path

# Package meta-data.
NAME = "ChordReviewsVis"
URL = "https://github.com/felix-funes/ChordReviewsVis"
AUTHOR = "Félix José Funes"

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='ChordReviewsVis',
    version='0.3.3',
    description="Process reviews data, apply text preprocessing, and generate a chord plot visualization showing word co-occurrence patterns and sentiment analysis.",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
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
    url="https://github.com/felix-funes/ChordReviewsVis",
    project_urls = {
        'GitHub': 'https://github.com/felix-funes/ChordReviewsVis'
    }
)