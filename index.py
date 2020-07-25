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
cursor = mydb.cursor()

def db_select(input):
    cuursor = mydb.cursor()
    s = cursor.execute(inpuut)
    return cursor.fetchall()

def db_fetch(input):
    cuursor = mydb.cursor()
    s = cursor.execute(inpuut)
    return cursor.fetchall()

# check if input fields is in required fields
def validator(input, required):
    keys = input.keys()
    counter_v = 0
    for field in input.keys():
        # field in required
        if field in required:
            counter_v += 1
            continue
        # one of the fields not in required
        else:
            return False
    if counter_v == len(required):
        return True
    return False

def point(request):
    if request.method == 'GET':
        p_fields = ['Latitude', 'Longitude', 'Create_time']
        if not validator(input, p_fields):
            print('Status: 404 Not Found')
            return

        point_get = 'Select * From CS411_Point Where Point_id = 1'
        cursor.execute(point_get)
        p_content = cursor.fetchall()[0]
        # initialize
        pid, lati, longi, dtime = 0, 0.0, 0.0, datetime.datetime.now()
        pid, lati, longi, dtime = p_content
        return {
            "Point_id": pid,
            "Latitude": lati,
            "Longitude": longti,
            "Create_time": dtime
        }

    elif(request.method == 'POST'):
        body  = request.json_body
        pid2 = random.randint(0, 2000)
        lati2 = body['Latitude']
        longti2 = body['Longitude']
        dtime2 = body['Create_time']
        point_post = 'Insert Into CS411_Point(Point_id, Latitude, Longitude, Create_time) VALUES (' +\
            str(pid2) + ',' + str(lati2) + ',' + str(longti2) + ',"' + str(dtime2) + '")'
        # print(point_post)
        cursor.execute(point_post)
        affected_rows = cursor.rowcount
        if affected_rows == 1:
            print("Successfully inserted")
        # "affected rows = {}".format():

        # where post_id = curr_id
        return {
            "Point_id": pid2,
            "Latitude": lati2,
            "Longitude": longti2,
            "Create_time": dtime2
        }

    elif request.method == 'DEL':
        point_del = 'Delete From CS411_Point Where Point_id = ' + str(point_last_id)
        cursor.execute(point_del)

# def point_id(request):
#     return [request.matchdict['id']]
#     if request.method == 'PUT':
#         return Response('Hello World!')
#     elif request.method == 'DELETE':
#         return Response('Hello Again')
#     return Response('Hello')

def client(request):
    # must have a row before
    client_last_id = cursor.lastrowid
    if request.method == 'GET':
        client_get = 'Select * ' + 'From CS411_Client Where Client_Id = ' + str(client_last_id)
        cursor.execute(point_get)
        c_content = cursor.fetchall()[0]
        # initialize to be not sick (flag_s = 0)
        cid, dtime, flag_s, postc = 0, datetime.datetime.now(), 0, 0
        cid, dtime, flag_s, postc = c_content
        return {
            "Client_id": cid,
            "Create_time": dtime,
            "Sick_or_not": flag_s,
            "Postcode": postc
        }

    # no need to return for updates
    elif request.method == 'PUT':
        client_put = 'Update CS411_Client set Sick_or_not=0 Where Client_id=' + str(client_last_id)
        cursor.execute(client_put)

    elif request.method == 'DEL':
        client_del = 'Delete From CS411_Client Where Client_id = ' + str(client_last_id)
        cursor.execute(client_del)

    elif request.method == 'POST':
        body = request.json_body
        cid2 = random.randint(0, 100)
        # problem : not repetitive ids
        pid3 = random.randint(0, 1000)
        dtime2 = body['Create_time']
        flag_s2 = body['Sick_or_not']
        postc2 = body['Postcode']
        client_post = 'Insert Into CS411_Client(Client_id, Create_time, Sick_or_not, Postcode) VALUES (' +\
            str(cid2) + ',"' + str(dtime2) + '",' + str(flag_s2) + ',' + str(postc2) + ')'
        ac_post = 'Insert Into CS411_Affected_Client_Point(Point, Client_id) VALUES (' +\
            str(pid3) + ',' + str(cid2) + ')'
        if affected_rows == 1:
            print("Successfully inserted")
        # cursor.execute(client_post)
        return {
            "Client_id": cid2,
            "Create_time": dtime2,
            "Sick_or_not": flag_s2,
            "Postcode": postc2
        }

def affected_client(request):
    if request.method == 'DEL':
        ac_del = 'Delete From CS411_Affected_Client_Point Where Client_id = ' + str(client_last_id)
        cursor.execute(client_del)
# def client_id(request):
#     if request.method == 'GET':
#         return Response('Hello World!')
#     elif request.method == 'DELETE':
#         return Response('Hello Again')
#     elif request.method == 'PUT':
#         return Response('Hello Third Time')
#     return Response('Hello!')

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('point', '/point')
        config.add_view(point, route_name='point', renderer='json')

        config.add_route('client', '/client')
        config.add_view(client, route_name='client', renderer='json')

        config.add_route('client_id', '/client/{id}')
        config.add_view(client_id, route_name='client_id', renderer='json')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 9000, app)
    server.serve_forever()
