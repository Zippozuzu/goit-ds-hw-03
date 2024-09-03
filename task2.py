import requests
from bs4 import BeautifulSoup
import json


url = "https://quotes.toscrape.com"

html_doc = requests.get(url).text

authors_name = []
quote_list = []
authors_list = []
n = 1

# get info for qoutes.json
while n <= 10:
    page_url = url + "/page/" + str(n)
    n = n + 1
    soup = BeautifulSoup(requests.get(page_url).text, "html.parser")

    quotes = soup.find_all("div", class_="quote")

    for q in quotes:
        # Extract quote details
        quote = {
            "tags": [tag.get_text(strip=True) for tag in q.find_all("a", class_="tag")],
            "author": q.find("small", class_="author").get_text(strip=True),
            "quote": q.find("span", class_="text").get_text(strip=True),
        }
        quote_list.append(quote)

    # Get list with all authors
    quotes = soup.find_all("small", class_="author")
    for quote in quotes:
        if quote.text not in authors_name:
            authors_name.append(
                # format author name
                quote.text.replace(" ", "-")
                .replace(".", "-")
                .replace("'", "")
                .replace("--", "-")
                .replace("é", "e")
                .strip("-")
            )
            format_author = list(dict.fromkeys(authors_name))


# get info for authors.json
for a in format_author:
    author_url = url + "/author/" + a
    soup_author = BeautifulSoup(requests.get(author_url).text, "html.parser")
    # Extract author details
    author = {
        "fullname": soup_author.select_one(
            "div.author-details h3.author-title"
        ).get_text(strip=True),
        "born_date": soup_author.select_one(
            "div.author-details .author-born-date"
        ).get_text(strip=True),
        "born_location": soup_author.select_one(
            "div.author-details .author-born-location"
        ).get_text(strip=True),
        "discription": soup_author.select_one(
            "div.author-details div.author-description"
        ).get_text(strip=True),
    }
    authors_list.append(author)

with open("authors.json", "w") as final:
    json.dump(authors_list, final, indent=4, ensure_ascii=False)

with open("qoutes.json", "w") as final:
    json.dump(quote_list, final, indent=4, ensure_ascii=False)
