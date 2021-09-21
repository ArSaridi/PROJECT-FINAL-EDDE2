import time
import requests

from bs4 import BeautifulSoup
from logger import logger
from helpers import (
    concat,
    sanitize)
from functools import reduce
from web_driver import web_driver
from csv_writer import dicts_to_csv
from profiles import (
    protothema_profile,
    efsyn_profile)

log = logger("scraper")
WEB_DRIVER = web_driver()

def get_source(url):
    """
    Send an HTTP request to the given link and returns the parsed HTML after
    scrolling.
    """

    log.debug(f"Fetching source url: {url}")

    try:
        SCROLL_PAUSE_TIME = 4
        WEB_DRIVER.get(url)

        last_height = WEB_DRIVER.execute_script("return document.body.scrollHeight")

        while (last_height < 200_000):
            WEB_DRIVER.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = WEB_DRIVER.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break

            last_height = new_height
    except:
        log.error("Failed to scroll...")

    return BeautifulSoup(WEB_DRIVER.page_source, "html.parser")


def get(url):
    log.info(f"Fetching article url: {url}")

    page = requests.get(url)

    if page.status_code != 200:
        log.info(f"Fetching failed with status code {page.status_code}")

    return BeautifulSoup(page.content, "html.parser")


def scrape_source(soup, pattern):
    "Return all article links extracted from given `soup`."
    a_tags = soup.find_all("a", href=True)
    links = list(
        map(lambda tag: tag["href"], a_tags))

    return list(
        filter(lambda link: bool(pattern.match(link)), links))


def scrape_article(soup, profile):
    "Extract all required information for the article."
    url = soup.select("link[rel='canonical']")[0]["href"]

    try:
        return {
            "url": url,
            "title": sanitize(profile["title_extractor"](soup)),
            "summary": sanitize(profile["summary_extractor"](soup)),
            "body": sanitize(profile["body_extractor"](soup)),
            "published_at": profile["published_at_extractor"](soup)
        }
    except:
        log.error(f"Could not scrape {url}")
        return {}


def scrape_profile(profile):
    "Scrape all sources for a given profile."
    source_scraper = get_source if profile["requires_scrolling"] else get

    source_pages = list(map(source_scraper, profile["sources"]))
    links_per_source = list(
        map(
            lambda source_page: scrape_source(source_page, profile["link_pattern"]),
            source_pages))
    links = set(reduce(concat, links_per_source))

    if profile["relative_urls"]:
        links = list(map(lambda link: profile["site_url"] + link, links))

    articles = list(map(get, links))
    scraped_articles = list(
        map(lambda article: scrape_article(article, profile), articles))

    return list(filter(lambda article: article != {}, scraped_articles))


def scrape_and_save(profile):
    log.info(f"Scraping profile {profile['name']}")
    scraped_articles = scrape_profile(profile)

    list(
        map(
            lambda article: log.info("Scraped: " + article["title"]),
            scraped_articles))

    log.info(f"Scraped {len(scraped_articles)} artlcles")
    log.info(f"Writing articles to file: '{profile['name']}.csv'")
    dicts_to_csv(scraped_articles, profile["name"])


def main():
    log.info("Started scraper")
    profiles = [
        # protothema_profile()
        efsyn_profile()
    ]

    list(map(scrape_and_save, profiles))
    log.info("Scraper finished")


if __name__ == "__main__":
    main()
