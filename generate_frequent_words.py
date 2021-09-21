import pandas as pd
import matplotlib.pyplot as plt

from toolz import groupby

def concat_article(articles):
    return " ".join(articles)


def generate_frequency_graph(dataframe, options):
    articles = dataframe[options[1]]
    words = concat_article(articles).split(" ")
    grouped_words = groupby(lambda x: x, words)

    frequencies = list(map(lambda key: len(grouped_words[key]), grouped_words.keys()))

    word_frequencies = sorted(
        list(zip(grouped_words.keys(), frequencies)),
        key=lambda word_and_frequency: word_and_frequency[1],
        reverse=True)[0:15]

    words, frequencies = list(zip(*word_frequencies))

    figure, ax = plt.subplots(figsize=(20, 8))
    ax.bar(words, frequencies)
    title = options[0] + " Top 15 word frequencies}"
    ax.set_title(title)
    ax.set_xticklabels(words)
    plt.savefig(f"./frequencies-{options[0]}.png")


def main():
    data_paths = (
        ("./processed-tweets-final.csv", ("tweets", "body")),
        ("./protothema-final.csv", ("protothema", "title")),
        ("./efsyn-final.csv", ("efsyn", "title")))

    dataframes = list(
            map(
                lambda path_and_options: generate_frequency_graph(pd.read_csv(path_and_options[0]), path_and_options[1]),
                data_paths))


if __name__ == "__main__":
    main()
