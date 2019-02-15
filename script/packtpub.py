import re
from sys import argv
from datetime import datetime, timedelta
from httplib2 import Http
from json import dumps, loads

#
# Hangouts Chat incoming webhook quickstart
#
def main():
    if len(argv) >= 2: 
        url = argv[1] 
    else: 
        raise AttributeError('Google chat bot URL is required.')

    message_headers = { 'Content-Type': 'application/json; charset=UTF-8'}
    message_template = """"
    *-->PACKTPUB FREE BOOK<---*

    *%s*

    *Pages:* %d
    *Publication date:* %s

    *About:* 
    %s
    *Topics:* %s
    *Features:* %s
    *Category:* %s
    *Preview image:* %s
    *Link:* https://www.packtpub.com/packt/offers/free-learning
    """
    
    # Collecting book info pro Packtpub API
    book_details = get_book_info()

    # Cleaning and decorating the message params
    book_details['about'] = decorate(book_details['about'], text_decoration)
    book_details['learn'] = decorate(book_details['learn'], list_decoration)
    book_details['features'] = decorate(book_details['features'], list_decoration)
    book_details['publicationDate'] = to_simple_date(book_details['publicationDate'])
    book_details['category'] = format_category(book_details['category'])
    
    bot_message = { 
        'text' : 
        message_template % 
        (book_details['title'],
        book_details['pages'],
        book_details['publicationDate'],
        book_details['about'],
        book_details['learn'],
        book_details['features'],
        book_details['category'],
        book_details['coverImage'])
    }

    print(bot_message['text'])

    response = Http().request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )

    print(response)

def get_book_info():
    today = format_date(datetime.today())
    tomorrow = format_date(datetime.today() + timedelta(days=1))

    today_free_offer = Http().request(
            method="GET",
            uri='https://services.packtpub.com/free-learning-v1/offers?dateFrom=%s&dateTo=%s' % (today, tomorrow)
        )[1]

    product_id = loads(today_free_offer)['data'].pop()['productId']

    book_details = Http().request('https://static.packt-cdn.com/products/%s/summary' % product_id, "GET")[1]

    return loads(book_details)

def format_date(date):
    return date.strftime('%Y-%m-%dT00:00:00.000Z')

def to_simple_date(string_date):
    date_array = string_date.split('T')[0].split('-')
    return '%s/%s/%s' % (date_array[2], date_array[1], date_array[0])

def remove_html(text):
    return re.sub('<.*?/?>', '', text)

def list_decoration(text):
    return '\t-  %s' % text

def text_decoration(text):
    return '_%s_' % text

def decorate(text, format_function):
    text = remove_html(text).strip()
    lines_formated = map(format_function, text.split('\r\n'))
    return "\r\n" + "\n".join(lines_formated) + "\r\n"

def format_category(category):
    return category.replace('-', ' ').capitalize()

if __name__ == '__main__':
    main()
