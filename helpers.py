from datetime import datetime


def concat(list1, list2):
    return [*list1, *list2]


def sanitize(string):
    return string \
        .strip() \
        .replace("\n", "")


def to_date(time):
    date_time = datetime.fromtimestamp(time.item() / 10**9)

    return date_time \
        .isoformat() \
        .split("T")[0] \
        .split("2021-")[1]
