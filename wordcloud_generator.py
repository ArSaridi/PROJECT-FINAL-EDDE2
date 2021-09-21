import pandas as pd
import matplotlib.pyplot as plt

from wordcloud import WordCloud


def create_figure(wordcloud):
    fig = plt.figure(
        figsize   = (40, 30),
        facecolor = 'k',
        edgecolor = 'k')

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)

    return fig

def create_wordcloud(text):
    return WordCloud(
        width            = 2000,
        height           = 1000,
        background_color = 'black',
        colormap         = "Blues"
    ).generate(text)


def concat_articles(articles):
    return " ".join(articles.tolist())


def save_wordcloud(dataframe, options):
    articles = dataframe[options[1]]
    cloud = create_wordcloud(concat_articles(articles))
    figure = create_figure(cloud)
    figure.savefig(f"./wordcloud-{options[0]}.png")

    return figure


def main():
    data_paths = (
        ("./processed-tweets-final.csv", ("tweets", "body")),
        ("./protothema-final.csv", ("protothema", "title")),
        ("./efsyn-final.csv", ("efsyn", "title")))

    dataframes = list(
            map(
                lambda path_and_options: save_wordcloud(pd.read_csv(path_and_options[0]), path_and_options[1]),
                data_paths))


if __name__ == "__main__":
    main()
