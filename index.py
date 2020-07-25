from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import mysql.connector

mydb = mysql.connector.connect(
  host="173.82.151.35",
  user="CS411",
  password="jllecwiXg1",
  port="50036",
  database = "CS411"
)

def db_execute(input):
    c = mydb.cursor()
    s = c.execute("SELECT * FROM CS411_Point")
    return c.fetchall()

def validator(input, required):
    keys = input.keys()
    for(i in required):
        if (i not in keys):
            return False
    return True    

def point(request):
    

    body  = request.json_body
    # check if in required
    if (not validator(body, ['latitude', 'longitude'])):
        return {
            "error": "missing balabalbal"
        }

    c = mydb.cursor()
    s = c.execute("SELECT * FROM CS411_Point")
    return c.fetchall()
    sql = 'SELECT * FROM POINT WHERE point_id = ' + body['point_id']

    if(request.method == 'POST'):
        point_id = random()
        create_time = datetime()
        sql = 'INSERT INTO POINT (point_id, B, C) VALUES (' + body['A'] + ')'
        # where post_id = curr_id
        return {
            "point)id": point_id,
            "latitude": body['latitude'],
            "longitutde": body['longitude'],
            "create_time": create_time
        }
    

def point_id(request):
    return [request.matchdict['id']]
    if request.method == 'PUT':
        return Response('Hello World!')
    else request.method == 'DELETE':
        return Response('Hello Again')
    return Response('Hello')

def client(request):
    if request.method == 'GET':
        return Response('Hello World!')
    else request.method == 'POST':
        return Response('Hello Again')
    return Response('Hello!')

def client_id(request):
    if request.method == 'GET':
        return Response('Hello World!')
    elif request.method == 'DELETE':
        return Response('Hello Again')
    elif request.method == 'PUT':
        return Response('Hello Third Time')
    return Response('Hello!')

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('point', '/point')
        config.add_view(point, route_name='point', renderer='json')

        config.add_route('point_id', '/point/{id}')
        config.add_view(point_id, route_name='point_id', renderer='json')

        config.add_route('client', '/client')
        config.add_view(client, route_name='client', renderer='json')

        config.add_route('client_id', '/client/{id}')
        config.add_view(client_id, route_name='client_id', renderer='json')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 9000, app)
    server.serve_forever()

