class Application:

    def __init__(self, urlpatterns: dict, front_controller: list):
        self.urlpatterns = urlpatterns
        self.front_controller = front_controller

    def __call__(self, env, start_response):
        path = env['PATH_INFO']

        if path in self.urlpatterns:
            view = self.urlpatterns[path]
            request = {}

            for controller in self.front_controller:
                controller(request)

            code, text = view(request)

            start_response(code, [('Content-Type', 'text/html')])

            return [text.encode('utf-8')]
        else:
            start_response('404 Not Found', [('Content-Type', 'text/html')])
            return [b'Not Found']
