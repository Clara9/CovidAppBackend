# CovidTracking_Backend

## Description
This is the backend of a mobile app which updates COVID statistics based on location, and alerts user if there is an infected patiennt nearby. The alert happens while protecting user privacy.

## Technologies
- REST API
- Postman
- Pyramid framework
- AWS Kubernetes
Below are the quote for prerequisites.
```
An account on AWS, with administrative rights to create and deploy an RDS database and EKS cluster.
Details for the AWS programmatic access (AWS access Key ID, AWS Secret Access Key)
Details of your AWS S3 buckets (AWS access Key ID, AWS Secret Access Key)
Access to Pyramid’s Kubernetes Configurator tool in the online customer portal.
Optionally, it is useful to have a Pyramid license key ready. The key needs to be an “Enterprise Edition” key (trial or otherwise).
```

## Languages
Python

## Setup
- This file includings database information, REST endpoints, and Pyramid framework configuration.
- Download Postman: https://www.postman.com/downloads/

## Deploy References
- This tutorial provides a deployment process from Pyrmid to 
- This app is deployed to AWS RDS
- http://help.pyramidanalytics.com/Content/Root/Guides/installation/Kubernetes/Deploying%20Pyramid%20to%20AWS%20Kubernetes.htm


## Reproduction
- Download index.py.
  - This is the file for Pyramid setup and maiin functions.

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
```
Postman is a Chrome add-on and application which is used to fire requests to an API.

Features:

Very lightweight and fast
Requests can be organized in groups (called collections) and folders
Tests can be created with verifications for certain conditions on the response
Share workspaces or collections with other people or teams
Publish collections as API documentation
Run tests on collections (using the Collection Runner or Newman)
Monitor collections
Setup mock servers
```

## Source
https://github.com/Pylons/pyramid \\
https://github.com/alisonhall/postman-introduction/blob/master/README.md


## Contact
Feel free to contact me at zwei9@hotmail.com, for any questions or suggestiions.
