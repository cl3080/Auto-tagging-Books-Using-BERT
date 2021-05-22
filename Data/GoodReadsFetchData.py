from datetime import datetime
import json
import os
import re
import time

from urllib.request import urlopen
from urllib.error import HTTPError
import bs4
import pandas as pd


def get_shelves(soup):

    shelf_count_dict = {}

    if soup.find('a', text='See top shelves…'):

        # Find shelves text.
        shelves_url = soup.find('a', text='See top shelves…')['href']
        source = urlopen('https://www.goodreads.com' + shelves_url)
        soup = bs4.BeautifulSoup(source, 'lxml')
        shelves = [' '.join(node.text.strip().split()) for node in soup.find_all('div', {'class': 'shelfStat'})]

        # Format shelves text.
        shelf_count_dict = {}
        for _shelf in shelves:
            _shelf_name = _shelf.split()[:-2][0]
            _shelf_count = int(_shelf.split()[-2].replace(',', ''))
            shelf_count_dict[_shelf_name] = _shelf_count

    return shelf_count_dict


def get_genres(soup):
    genres = []
    for node in soup.find_all('div', {'class': 'left'}):
        current_genres = node.find_all('a', {'class': 'actionLinkLite bookPageGenreLink'})
        current_genre = ' > '.join([g.text for g in current_genres])
        if current_genre.strip():
            genres.append(current_genre)
    return genres


def get_series_name(soup):
    series = soup.find(id="bookSeries").find("a")
    if series:
        series_name = re.search(r'\((.*?)\)', series.text).group(1)
        return series_name
    else:
        return ""


def get_description(soup):
    description = soup.find(id="description")
    if description:
        return description.text.strip()
    else:
        return ""

def get_series_uri(soup):
    series = soup.find(id="bookSeries").find("a")
    if series:
        series_uri = series.get("href")
        return series_uri
    else:
        return ""


def get_isbn(soup):
    try:
        isbn = re.findall(r'nisbn: [0-9]{10}' , str(soup))[0].split()[1]
        return isbn
    except:
        return "isbn not found"

def get_isbn13(soup):
    try:
        isbn13 = re.findall(r'nisbn13: [0-9]{13}' , str(soup))[0].split()[1]
        return isbn13
    except:
        return "isbn13 not found"


def get_rating_distribution(soup):
    distribution = re.findall(r'renderRatingGraph\([\s]*\[[0-9,\s]+', str(soup))[0]
    distribution = ' '.join(distribution.split())
    distribution = [int(c.strip()) for c in distribution.split('[')[1].split(',')]
    distribution_dict = {'5 Stars': distribution[0],
                         '4 Stars': distribution[1],
                         '3 Stars': distribution[2],
                         '2 Stars': distribution[3],
                         '1 Star':  distribution[4]}
    return distribution_dict


def get_num_pages(soup):
    if soup.find('span', {'itemprop': 'numberOfPages'}):
        num_pages = soup.find('span', {'itemprop': 'numberOfPages'}).text.strip()
        return int(num_pages.split()[0])
    return ''


def get_year_first_published(soup):
    if soup.find('nobr', attrs={'class':'greyText'}):
        year_first_published = soup.find('nobr', attrs={'class':'greyText'}).string
        return re.search('([0-9]{3,4})', year_first_published).group(1)
    return ''

def get_id(bookid):
    pattern = re.compile("([^.-]+)")
    return pattern.search(bookid).group()

def scrape_book(book_id):
    url = 'https://www.goodreads.com/book/show/' + book_id
    source = urlopen(url)
    soup = bs4.BeautifulSoup(source, 'html.parser')

    return {'book_id_title':        book_id,
            'book_id':              get_id(book_id),
            'book_title':           ' '.join(soup.find('h1', {'id': 'bookTitle'}).text.split()),
            "book_series":          get_series_name(soup),
            "book_series_uri":      get_series_uri(soup),
            'isbn':                 get_isbn(soup),
            'isbn13':               get_isbn13(soup),
            'year_first_published': get_year_first_published(soup),
            'author':               ' '.join(soup.find('span', {'itemprop': 'name'}).text.split()),
            'num_pages':            get_num_pages(soup),
            'genres':               get_genres(soup),
            'shelves':              get_shelves(soup),
            'description':       get_description(soup),
            'num_ratings':          soup.find('meta', {'itemprop': 'ratingCount'})['content'].strip(),
            'num_reviews':          soup.find('meta', {'itemprop': 'reviewCount'})['content'].strip(),
            'average_rating':       soup.find('span', {'itemprop': 'ratingValue'}).text.strip(),
            'rating_distribution':  get_rating_distribution(soup)}

def condense_books(books_directory_path):

    books = []

    for file_name in os.listdir(books_directory_path):
        if file_name.endswith('.json') and not file_name.startswith('.') and file_name != "all_books.json":
            _book = json.load(open(books_directory_path + '/' + file_name, 'r')) #, encoding='utf-8', errors='ignore'))
            books.append(_book)

    return books

def main():

    start_time = datetime.now()

    output_directory_path = '/Users/chaoli/desktop/GoodReads/Books'
    book_ids  = [str(i) for i in range(1,10000)]
    books_already_scraped = []
   # if os.path.isfile(output_directory_path):
    books_already_scraped =  [file_name.replace('.json', '') for file_name in os.listdir(output_directory_path) if file_name.endswith('.json') and not file_name.startswith('all_books')]
    books_to_scrape       = [book_id for book_id in book_ids if book_id not in books_already_scraped]
    condensed_books_path   = output_directory_path + '/all_books'

    for i, book_id in enumerate(books_to_scrape):
        try:
            print(str(datetime.now()) + ' ' +': Scraping ' + book_id + '...')
            print(str(datetime.now()) + ' ' +': #' + str(i+1+len(books_already_scraped)) + ' out of ' + str(len(book_ids)) + ' books')

            book = scrape_book(book_id)
            json.dump(book, open(output_directory_path + '/' + book_id + '.json', 'w'))

            print('=============================')

        except HTTPError as e:
            print(e)
            exit(0)


    books = condense_books(output_directory_path)

    json.dump(books, open(f"{condensed_books_path}.json", 'w'))
    book_df = pd.read_json(f"{condensed_books_path}.json")
    book_df.to_csv(f"{condensed_books_path}.csv", index=False, encoding='utf-8')

    print(str(datetime.now()) + ' ' + f':\n\n🎉 Success! All book metadata scraped. 🎉\n\nMetadata files have been output to /{output_directory_path}\nGoodreads scraping run time = ⏰ ' + str(datetime.now() - start_time) + ' ⏰')



if __name__ == '__main__':
    main()
