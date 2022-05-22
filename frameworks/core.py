import quopri
from .requests import GetRequest, PostRequest

class Application:

    def __init__(self, urlpatterns: dict, front_controller: list):
        self.urlpatterns = urlpatterns
        self.front_controller = front_controller

    def __call__(self, env, start_response):
        path = env['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        method = env['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequest().request_params(env)
            request['data'] = data
        if method == 'GET':
            request_params = GetRequest().get_request_params(env)
            request['request_params'] = request_params

        if path in self.urlpatterns:
            view = self.urlpatterns[path]
        else:
            view = NotFound404()

        for front in self.front_controller:
            front(request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        decoding_data = {}
        for key, value in data.items():
            value = bytes(value.replace('%', '=').replace('+', ' '), 'utf-8')
            decode_str = quopri.decodestring(value).decode('utf-8')
            decoding_data[key] = decode_str
        return decoding_data

class NotFound404:
    def __call__(self, request):
        return '404 Not Found', '404 Not Found'
