# CovidTracking_Backend

## Description
This is the backend of a mobile app which updates COVID statistics based on location, and alerts user if there is an infected patiennt nearby. The alert happens while protecting user privacy.

## Technologies
REST API, Postman, Pyramid framework

## Languages
Python

## Setup
- This file includings database information, REST endpoints, and Pyramid framework configuration.
- Download Postman: https://www.postman.com/downloads/

## Reproduction
- Download index.py.
  - This is the file for Pyramid setup and maiin functions.
  - 
## Pyramid Introduction
```
Pyramid is a small, fast, down-to-earth, open source Python web framework. It makes real-world web application development and deployment more fun, more predictable, and more productive.

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

def hello_world(request):
    return Response('Hello World!')

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
Pyramid is a project of the Pylons Project.
```

## Postman Introduction
## Source
https://github.com/Pylons/pyramid
