import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer
from functools import reduce
from helpers import to_date
from logger import logger

log = logger("sentiment-analyzer")

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


def add_sentiment_column(dataframe, wordcount, sentiment_words):
    dataframe[sentiment_words[0]] = wordcount[sentiment_words[1]].sum(axis=1)
    return dataframe


def vectorize(articles):
    vectorizer = CountVectorizer(
        analyzer      = "word",
        vocabulary    = sentiment_dataframe["word"],
        token_pattern = "[Α-Ωα-ωΆ-Ώά-ώ]{2,}",
        strip_accents = "unicode",
        ngram_range   = (1, 2))

    matrix = vectorizer.fit_transform(articles)
    vocabulary = vectorizer.get_feature_names()

    return pd.DataFrame(
        matrix.toarray(),
        columns = vocabulary)



def analyze(dataframe, options):
    log.info(f"Analyzing {options[0]}")
    dataframe["published_at"] = dataframe["published_at"] \
        .apply(lambda timestamp: pd.to_datetime(timestamp, unit="s"))

    wordcount = vectorize(dataframe["body"])

    dataframe = reduce(
        lambda df, sentiment_words: add_sentiment_column(df, wordcount, sentiment_words),
        lexicon, dataframe)

    timeseries = dataframe \
        .drop(columns=["title", "summary", "body", "url"]) \
        .resample(options[1], on="published_at") \
        .sum()

    figure, ax = plt.subplots(figsize=(30, 15))
    index = list(timeseries.index.values)
    dates = list(map(to_date, index))
    title = options[0] + " - Sentiments"

    list(map(
        lambda sentiment: ax.plot(dates, timeseries[sentiment], label=sentiment),
        sentiments))

    ax.set_title(title)
    ax.set_xticklabels(dates)
    plt.legend()
    plt.savefig(f"./{options[0]}-sentiments.png")


def main():
    log.info("Started sentiment analysis")
    data_paths = (
        ("./processed-tweets-final.csv", ("tweets", "1d")),
        ("./protothema-final.csv", ("protothema", "1w")),
        ("./efsyn-final.csv", ("efsyn", "1w")))

    dataframes = list(
            map(
                lambda path_and_options: analyze(pd.read_csv(path_and_options[0]), path_and_options[1]),
                data_paths))

    log.info("Sentiment analysis has finished")


if __name__ == "__main__":
    main()
