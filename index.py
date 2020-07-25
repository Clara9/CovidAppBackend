from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import mysql.connector
import datetime
import random

mydb = mysql.connector.connect(
  host="173.82.151.35",
  user="CS411",
  password="jllecwiXg1",
  port="50036",
  database = "CS411"
)

def db_select(input):
    cuursor = mydb.cursor()
    s = cursor.execute(inpuut)
    return cursor.fetchall()

def db_fetch(input):
    cuursor = mydb.cursor()
    s = cursor.execute(inpuut)
    return cursor.fetchall()

# def validator(input, required):
#     keys = input.keys()
#     for(i in required):
#         if (i not in keys):
#             return False
#     return True    

def point(request):
    body  = request.json_body
    # # check if in required
    # if (not validator(body, ['latitude', 'longitude'])):
    #     return {
    #         "error": "missing balabalbal"
    #     }

    cursor = mydb.cursor()
    s = cursor.execute("SELECT * FROM CS411_Point")

    # give value to attributes
    content = cursor.fetchall()[0]
    pid, latitude, longitude, create_time = 0, 0.0, 0.0, datetime.datetime.now()
    pid, latitude, longitude, create_time = content

    # sql = 'SELECT * FROM POINT WHERE point_id = ' + body['point_id']
    point_get = ""
    if request.method == 'GET':
        point_get = 'Select * From CS411_Point Where Point_id = 1'
        cursor.execute(point_get)
        tmp = c.fetchall()
    # print(tmp)

    if(request.method == 'POST'):
        pid = random.randint(0, 500)
        lati = body['Latitude']
        longti = body['Longitude']
        dtime = body['Create_time']
        point_post = 'Insert Into CS411_Point(Point_id, Latitude, Longitude, Create_time) VALUES (' +\
            str(pid) + ',' + str(lati) + ',' + str(longti) + ',"' + str(dtime) + '")'
        # print(point_post)
        cursor.execute(point_post)
        affected_rows = cursor.rowcount
        if affected_rows == 1:
            print("Successfully inserted")
        # "affected rows = {}".format():

        # where post_id = curr_id
        return {
            "Point_id": pid,
            "Latitude": lati,
            "Longitude": longti,
            "Create_time": dtime
        }

def point_id(request):
    return [request.matchdict['id']]
    if request.method == 'PUT':
        return Response('Hello World!')
    elif request.method == 'DELETE':
        return Response('Hello Again')
    return Response('Hello')

def client(request):
    if request.method == 'GET':
        return Response('Hello World!')
    elif request.method == 'POST':
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

