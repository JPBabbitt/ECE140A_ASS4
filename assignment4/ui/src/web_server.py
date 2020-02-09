from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response

import requests
import os
REST_SERVER = os.environ['REST_SERVER']

def show_login(req):
  resp = requests.get(REST_SERVER + "/sign_up")
  return render_to_response(resp, {}, request = req)

def show_users(req):
  Users = requests.get(REST_SERVER + "/users").json()
  return render_to_response('templates/show_users.html', {'users': Users}, request=req)

if __name__ == '__main__':
  config = Configurator()

  config.include('pyramid_jinja2')
  config.add_jinja2_renderer('.html')

  config.add_route('v1', '/')
  config.add_view(show_login, route_name='v1')

  config.add_route('v2', '/users')
  config.add_view(show_users, route_name='v2')

  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 5000, app)
  server.serve_forever()