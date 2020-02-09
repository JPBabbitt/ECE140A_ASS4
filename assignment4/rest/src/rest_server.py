from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.response import FileResponse
import json

USERS_FILE_PATH = "users.txt"

## File Utility methods
def read_file(path):
    with open(path) as json_file:
        data = json.load(json_file)
    return data

def write_to_file(path, data):
    with open(path, 'w') as outfile:
        json.dump(data, outfile)

# Serve Web Page
def sign_up(req):
  return FileResponse("pages/sign-up.html")

# API Implementation
def sign_up_submit(req):
  username = req.POST['username']
  password = req.POST['password']
  save_user_details(username, password)
  return Response("Success!!")

# Save data in Data Store
def save_user_details(username, password):
  users = read_file(USERS_FILE_PATH)
  newUser = {}
  newUser['username'] = username
  newUser['password'] = password
  newUser['status'] = "Pending"
  users.append(newUser)
  write_to_file(USERS_FILE_PATH, users)

def getUsers(req):
  return read_file(USERS_FILE_PATH)

def updateUserStatus(userid, status):
  users = read_file(USERS_FILE_PATH)
  users[userid] = status
  write_to_file(USERS_FILE_PATH, users)
  return True;
  
if __name__ == '__main__':
  config = Configurator()
  # Add API Route to config
  config.add_route('sign_up_submit', '/sign_up_submit')
  config.add_view(sign_up_submit, route_name='sign_up_submit', request_method="POST")

  # Add Page Route to config
  config.add_route('sign_up', '/sign_up')
  config.add_view(sign_up, route_name='sign_up')

  # Add Admin Route to config
  config.add_route('rest_route', '/users')
  config.add_view(getUsers, route_name='rest_route', renderer='json')

  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 5000, app)
  server.serve_forever()