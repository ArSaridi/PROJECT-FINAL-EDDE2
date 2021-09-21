import pandas as pd


def main():
    pd.read_csv("./tweets.csv") \
        .drop(
            [
                "screen_name",
                "in_reply_to_screen_name",
                "retweeted_status_screen_name",
                "user_description",
                "source",
                "lang",
                "id"
            ],
            axis=1) \
        .assign(summary="") \
        .assign(title="") \
        .assign(url="https://twitter.com/") \
        .rename(columns={
            "text"      : "body",
            "created_at": "published_at"}) \
        .to_csv("./processed-tweets.csv", index=False)


if __name__ == "__main__":
    main()
