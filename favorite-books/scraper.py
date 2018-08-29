from robobrowser import RoboBrowser
import re
import config


def get_favorites_kitapyurdu(br):
    # Open login page
    login = config.kitapyurdu['login']
    br.open(login['url'])
    print(login['url'] + ' page is opened.')

    # Find login form and submit with credentials
    form = br.get_form(id='login')
    form['email'] = login['email']
    form['password'] = login['password']
    br.submit_form(form)
    print('Signed in.')

    # Open favorite books section and get books
    fav_url = config.kitapyurdu['fav_url']
    br.open(fav_url)
    book_list = br.select('div[itemtype="http://schema.org/Book"]')
    print(str(len(book_list)) + ' books are found.')

    # Traverse book list and extract information
    books_info = "Favorite Books\n\n"
    num = 1
    for book in book_list:
        name = book.select_one('span[itemprop="name"]').text
        url = book.select_one('a[itemprop="url"]')['href']
        isbn = book.select_one('meta[itemprop="isbn"]')
        if isbn is None:
            isbn = 'ISBN not available!'
        else:
            isbn = '978' + isbn['content']
        books_info += f'{num}. {name}\nURL= {url}\nISBN: {isbn}\n\n'
        num += 1

    # Write the list into the txt file
    with open('favorite_books.txt', 'w') as books:
        print(books_info, file=books)

    print('Favorite books have been noted.')


def set_favorites_kidega(br):
    # Open login page
    login = config.kidega['login']
    br.open(login['url'])
    print(login['url'] + ' page is opened.')

    # Find login form and get token value
    form = br.get_form(id='loginForm')
    _token = form['_token'].value
    payload = {
        '_token': _token,
        'username': login['username'],
        'password': login['password'],
        'remember': 0
    }
    # Submit post request to login
    br.session.post(login['url'], data=payload)
    print('Signed in.')

    # Get books from the txt file
    books = open('favorite_books.txt', 'r').read()
    book_list = [m.start() for m in re.finditer('ISBN: ', books)]
    isbn_list = []
    for book in book_list:
        isbn_list.insert(0, books[book+6:book+19])
    print('ISBN numbers of favorite books have been gathered.')

    # Find all books by ISBN numbers and go its page
    search_url = config.kidega['search_url']
    book_list = []
    for isbn in isbn_list:
        br.open(search_url + isbn)
        print(br.url + ' page is opened.')

        result = br.select('#products .image a')
        if len(result) > 0:
            book_href = result[0]['href']
            book_list.insert(0, book_href)
    print('Book search by ISBN number is complete.')

    # Add book to favorites list
    for book in book_list:
        br.open(book)
        print(br.url + ' page is opened.')

        book_id = br.url.split('/')[-2].split('-')[-1]
        payload = {
            '_token': _token,
            'id': book_id,
            'module': '1'
        }
        br.session.post('https://kidega.com/favori/ekle', data=payload)
    print('All books are added to favorites list.')


def create_browser():
    br = RoboBrowser(parser='html.parser')
    return br


br = create_browser()
get_favorites_kitapyurdu(br)
set_favorites_kidega(br)
