import csv


def dicts_to_csv(dictionaries, name):
    if len(dictionaries) == 0:
        return

    with open(f"./{name}.csv", "w", encoding="utf-8", newline="\n") as csv_file:
        writer = csv.DictWriter(csv_file, dictionaries[0].keys())
        writer.writeheader()
        writer.writerows(dictionaries)
