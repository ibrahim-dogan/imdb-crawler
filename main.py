import re

import requests
from bs4 import BeautifulSoup
from requests import get

urls = []
titles = []
categories = []
descriptions = []


def load_imdb_urls():
    file1 = open('input/imdb.txt', 'r')
    global urls
    urls = [line.strip() for line in file1.readlines()]
    print(len(urls), " Link bulundu")


def create_outputs():
    with open('output/titles.txt', 'w') as filehandle:
        for title in titles:
            title = re.sub("[\(\[].*?[\)\]]", "", title.strip())
            title = title.replace(u'\xa0', ' ')
            filehandle.write('%s\n' % title)

    with open('output/categories.txt', 'w') as filehandle:
        for category in categories:
            filehandle.write('%s\n' % category)

    with open('output/descriptions.txt', 'w') as filehandle:
        for description in descriptions:
            filehandle.write('%s\n' % description)


def start_crawling():
    global titles, categories, descriptions
    index = 0
    for url in urls:
        index += 1
        response = get(url, headers={"Accept-Language": "tr-TR,tr;q=0.9"})

        html_soup = BeautifulSoup(response.text, 'html.parser')
        title = html_soup.find_all('h1')[0].text
        title_original = html_soup.find_all('div', class_='originalTitle')
        if (title_original):
            title_original = re.sub("[\(\[].*?[\)\]]", "", title_original[0].text.strip())
            title = f'{title.strip()}/ {title_original}'
        summary_text = html_soup.find('div', class_='summary_text')
        subtext = html_soup.find('div', class_='subtext')
        category = [category.text.strip() for category in subtext.find_all('a')[:-1]]
        poster_url = html_soup.find('div', class_='poster').find('img').get('src')

        print(f'{index}/{len(urls)}:\t',title)

        titles.append(title)
        descriptions.append(summary_text.text.strip())
        categories.append(", ".join(category))

        with open(f"output/images/{index}.jpg", "wb") as f:
            f.write(requests.get(poster_url).content)


if __name__ == '__main__':
    load_imdb_urls()
    start_crawling()
    create_outputs()
