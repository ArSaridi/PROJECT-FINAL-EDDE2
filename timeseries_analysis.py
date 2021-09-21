import pandas as pd
import matplotlib.pyplot as plt

from helpers import to_date


def analyze(dataframe, options):
    dataframe["published_at"] = dataframe["published_at"] \
        .apply(lambda timestamp: pd.to_datetime(timestamp, unit="s"))

    timeseries = dataframe \
        .drop(columns=["title", "summary", "body"]) \
        .resample(options[1], on="published_at") \
        .count()

    index = list(timeseries.index.values)

    dates = list(map(to_date, index))

    figure, ax = plt.subplots(figsize=(30, 8))
    ax.bar(dates, timeseries["url"])
    title = options[0] + " - Articles in 2021 per day"
    ax.set_title(title)
    ax.set_xticklabels(dates)
    plt.savefig(f"./daily-articles-{options[0]}.png")


def main():
    data_paths = (
        ("./processed-tweets-final.csv", ("tweets", "1d")),
        ("./protothema-final.csv", ("protothema", "1w")),
        ("./efsyn-final.csv", ("efsyn", "1w")))

    dataframes = list(
            map(
                lambda path_and_options: analyze(pd.read_csv(path_and_options[0]), path_and_options[1]),
                data_paths))


if __name__ == "__main__":
    main()
