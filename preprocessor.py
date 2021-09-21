import re
import spacy
import pandas as pd

from datetime import (
    datetime,
    timezone)
from functools import reduce
from helpers import concat
from logger import logger

log = logger("preprocessor")
nlp = spacy.load('el_core_news_sm')
custom_stopwords = [
    "το",
    "η",
    "ο",
    "ή",
    "του",
    "της",
    "κ",
    "από",
    "μας",
    "τούτης",
    "των",
    "για",
    "τους",
    "τις",
    "σε",
    "στην",
    "στον",
    "στο",
    "τα",
    "δεν",
    # Twitter filter
    "bigbrothergr",
    "agriesmelisses",
    "greece",
    "εμβολιο",
    "lifestyle",
    "toprwino",
    "happyday",
    "megakalimera",
    "pamedanai",
    "tlive",
    "thebachelorgr",
    "topchefgr",
    "dyoxenoi",
    "salonikaplus"
]


def clean_text(text):
    return re.sub(
        r"\s+",
        " ",
        re.sub(r"[^\w\s]", "", text)) \
             .lower() \
             .strip()


def remove_stop_words(lemmas):
    stopwords = concat(nlp.Defaults.stop_words, custom_stopwords)

    return list(filter(lambda lemma: lemma not in stopwords, lemmas))


def clean_text_column(column):
    return column \
        .apply(str) \
        .apply(lambda text: text.split("Ειδήσεις σήμερα")[0]) \
        .apply(clean_text) \
        .apply(nlp) \
        .apply(lambda tokens: list(map(lambda token: token.lemma_, tokens))) \
        .apply(remove_stop_words) \
        .apply(lambda lemmas: list(
            map(
                lambda lemma: lemma if not lemma.startswith("https") else "",
                lemmas))) \
        .apply(lambda lemmas: " ".join(lemmas)) \
        .apply(lambda text: text.strip() if str(text) != "nan" else "")


def clean_date_column(date_column):
    """
    Convert all string dates to UTC timezone
    and then to timestamp.
    """
    return date_column \
        .apply(lambda date: date.replace("Z", "+00:00")) \
        .apply(lambda date: datetime.fromisoformat(date)
               .astimezone(timezone.utc)
               .timestamp()
               .real)


def clean(dataframe):
    dataframe["title"] = clean_text_column(dataframe["title"])
    dataframe["summary"] = clean_text_column(dataframe["summary"])
    dataframe["body"] = clean_text_column(dataframe["body"])
    dataframe["published_at"] = clean_date_column(dataframe["published_at"])

    return dataframe


def main():
    data_paths = [
        "./processed-tweets.csv",
        "./protothema.csv",
        "./efsyn.csv"
    ]

    log.info(f"Started preprocessing {len(data_paths)} csv files")

    dataframes = list(
        zip(
            map(
                lambda path: "-final.csv".join(path.split(".csv")),
                data_paths),
            map(
                lambda path: clean(pd.read_csv(path)),
                data_paths)))

    log.info("Writing results...")

    list(
        map(
            lambda path_and_df: path_and_df[1].to_csv(path_and_df[0], index=False),
            dataframes))

    log.info("Preprocessing has completed")


if __name__ == "__main__":
    main()
