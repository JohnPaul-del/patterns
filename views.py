import os
from datetime import datetime

from frameworks.templates import _render


def page_not_found(request):
    return '404 Not Found', [b'404 Not Found']


def index_view(request):
    data = {
        'name': 'BlaBlaBla Inc,',
        'services': ['start', 'stop', 'continue']
    }

    return '200 OK', _render('index.html', **data)


def about_view(request):
    return '200 OK', _render('about.html')


def contact_view(request):
    if request.get('method') == 'POST':
        getting_time = str(datetime.now())
        data = request['data']
        title = data['title']
        text = data['text']
        email = data['email']

        path = os.path.dirname(os.path.abspath(__file__))
        with open(f'{path}/messages/message_{getting_time}.txt', 'w') as msg_data:
            msg_data.write(f'Email from: {email}\n'
                           f'Topic: {title}\n'
                           f'Text: {text}')
        return '200 OK', _render('contact_us.html')
    else:
        return '200 OK', _render('contact_us.html')
