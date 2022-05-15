from wsgiref.simple_server import make_server

from frameworks import Application
from urls import routes, fronts

application = Application(routes, fronts)


def run_server():
    with make_server('', 8008, application) as httpd:
        print(f'Server running\n '
              f'================================\n'
              f'Available on 127.0.0.1:8008')
        httpd.serve_forever()


if __name__ == '__main__':
    run_server()
