import re


def protothema_profile():
    return {
        "name": "protothema",
        "site_url": "https://www.protothema.gr",
        "requires_scrolling": True,
        "relative_urls": True,
        "link_pattern": re.compile(".*protothema\\.gr\\/greece\\/article\\/"),
        "sources": [
            "https://www.protothema.gr/anazitisi/?q=%23metoo"
        ],
        "title_extractor": lambda soup: soup.select("meta[property='og:title']")[0]["content"],
        "summary_extractor": lambda soup: soup.select("meta[name='description']")[0]["content"],
        "body_extractor": lambda soup: soup.select(".cntTxt")[0].text,
        "published_at_extractor": lambda soup: soup.select("meta[property='article:published_time']")[0]["content"]
    }


def efsyn_profile():
    return {
        "name": "efsyn",
        "site_url": "https://www.efsyn.gr",
        "requires_scrolling": False,
        "relative_urls": True,
        "link_pattern": re.compile(".*\\/[^\\/]+\\/[0-9]{6}_"),
        "sources": [
            "https://www.efsyn.gr/search?keywords=%23metoo&field_category=All&field_author=All&field_anonymous_author=&created%5Bmin%5D=&created%5Bmax%5D=&sort_by=created",
            "https://www.efsyn.gr/search?created%5B0%5D=&created%5B1%5D=&field_anonymous_author=&field_author=All&field_category=All&keywords=%23metoo&sort_by=created&page=1",
            "https://www.efsyn.gr/search?created%5B0%5D=&created%5B1%5D=&field_anonymous_author=&field_author=All&field_category=All&keywords=%23metoo&sort_by=created&page=2",
            "https://www.efsyn.gr/search?created%5B0%5D=&created%5B1%5D=&field_anonymous_author=&field_author=All&field_category=All&keywords=%23metoo&sort_by=created&page=3",
            "https://www.efsyn.gr/search?created%5B0%5D=&created%5B1%5D=&field_anonymous_author=&field_author=All&field_category=All&keywords=%23metoo&sort_by=created&page=4",
            "https://www.efsyn.gr/search?created%5B0%5D=&created%5B1%5D=&field_anonymous_author=&field_author=All&field_category=All&keywords=%23metoo&sort_by=created&page=5",
            "https://www.efsyn.gr/search?created%5B0%5D=&created%5B1%5D=&field_anonymous_author=&field_author=All&field_category=All&keywords=%23metoo&sort_by=created&page=6",
            "https://www.efsyn.gr/search?created%5B0%5D=&created%5B1%5D=&field_anonymous_author=&field_author=All&field_category=All&keywords=%23metoo&sort_by=created&page=7",
            "https://www.efsyn.gr/search?created%5B0%5D=&created%5B1%5D=&field_anonymous_author=&field_author=All&field_category=All&keywords=%23metoo&sort_by=created&page=8",
            "https://www.efsyn.gr/search?created%5B0%5D=&created%5B1%5D=&field_anonymous_author=&field_author=All&field_category=All&keywords=%23metoo&sort_by=created&page=9"
        ],
        "title_extractor": lambda soup: soup.select("meta[property='og:title']")[0]["content"],
        "summary_extractor": lambda soup: soup.select(".article__summary")[0].text,
        "body_extractor": lambda soup: soup.select(".article__body")[0].text,
        "published_at_extractor": lambda soup: soup.select(".article__date")[0]["datetime"]
    }
