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
    return '200 OK', _render('contact_us.html')