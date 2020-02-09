from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response

import requests
import os
REST_SERVER = os.environ['REST_SERVER']

def show_books(req):
  Books = requests.get(REST_SERVER + "/books").json()
  return render_to_response('templates/show_books.html', {'books': Books}, request=req)

if __name__ == '__main__':
  config = Configurator()

  config.include('pyramid_jinja2')
  config.add_jinja2_renderer('.html')

  config.add_route('v2', '/')
  config.add_view(show_books, route_name='v2')

  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 5000, app)
  server.serve_forever()