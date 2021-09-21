import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from helpers import to_date
from logger import logger

log = logger("cosine-similarity")

sentiment_data = "https://raw.githubusercontent.com/datajour-gr/Data_journalism/master/week10/NRC_GREEK_Translated_6_2020.csv"
sentiment_dataframe = pd.read_csv(sentiment_data) \
    .drop_duplicates(subset=["word"]) \
    .dropna() \
    .reset_index()

sentiments = [
    "Anger",
    "Positive",
    "Sadness",
    "Disgust",
    "Surprise",
    "Anticipation",
    "Negative",
    "Joy",
    "Trust",
    "Fear"
]

lexicon = list(
    zip(
        sentiments,
        map(
            lambda sentiment: sentiment_dataframe[sentiment_dataframe[sentiment] == 1]["word"],
            sentiments)))


def vectorize(articles):
    vectorizer = CountVectorizer(
        analyzer      = "word",
        vocabulary    = sentiment_dataframe["word"],
        token_pattern = "[Α-Ωα-ωΆ-Ώά-ώ]{2,}",
        strip_accents = "unicode",
        ngram_range   = (1, 2))

    return cosine_similarity(vectorizer.fit_transform(articles))


def analyze(dataframe, name):
    log.info(f"Analyzing {name}")

    similarity = vectorize(dataframe["body"])

    figure, ax = plt.subplots(figsize=(30, 15))
    title = name + " - Cosine Similarity Heatmap"

    plt.imshow(similarity, cmap="plasma")
    ax.set_title(title)
    cb = plt.colorbar()
    cb.set_label('Cosine Similarity')
    plt.savefig(f"./{name}-heatmap.png")


def main():
    log.info("Started cosine-similary analysis")
    data_paths = (
        ("./processed-tweets-final.csv", "tweets"),
        ("./protothema-final.csv", "protothema"),
        ("./efsyn-final.csv", "efsyn"))

    list(
        map(
            lambda path_and_name: analyze(pd.read_csv(path_and_name[0]), path_and_name[1]),
            data_paths))

    log.info("Sentiment analysis has finished")


if __name__ == "__main__":
    main()
