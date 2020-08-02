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

# check if input fields is in required fields
# def validator(input, required):
#     keys = input.keys()
#     counter_v = 0
#     for field in input.keys():
#         # field in required
#         if field in required:
#             counter_v += 1
#             continue
#         # one of the fields not in required
#         else:
#             return False
#     if counter_v == len(required):
#         return True
#     return False

def point(request):
    body = request.json_body
    if request.method == 'POST':
        # insert point
        point_insert = 'Insert Into CS411_Point(Latitude, Longitude, Postcode) VALUES ('\
         + str(body['Latitude']) + ',' + str(body['Longitude']) + ',' + str(body['Postcode']) + ')'
        # print(point_insert)
        cursor.execute(point_insert)
        mydb.commit()

        point_sick = 'Select c.Sick_or_not from CS411_Client c Where c.Client_id = ' + str(body['Client_id'])
        cursor.execute(point_sick)
        s_flag = cursor.fetchall()[0]
        mydb.commit()

        point_select = 'Select last_insert_id()'
        cursor.execute(point_select)
        pid = cursor.fetchall()[0][0]
        mydb.commit()
        if s_flag:
            a_point_insert = "Insert Into CS411_Affected_Client_Point(Point_id, Client_id) " + "Values (" + str(pid) + ", " + str(body['Client_id']) + ")"
            # print(a_point_insert)
            cursor.execute(a_point_insert)
            mydb.commit()

        # get result of last query
        point_all = 'Select * From CS411_Point Where Point_id = ' + str(pid)
        cursor.execute(point_all)
        p_content = cursor.fetchall()[0]
        mydb.commit()
        # print(p_content)
        pid, lati, longti, times, postc = [str(item) for item in p_content]
        return {
            "Point_id": pid,
            "Latitude": lati,
            "Longitude": longti,
            "Create_time": times,
            "Postcode": postc
        }

def point_id(request):
    pid = request.matchdict['id']
    if request.method == 'GET':
        point_get = 'Select * ' + 'From CS411_Point Where Point_id = ' + str(pid)
        cursor.execute(point_get)
        pi_content = cursor.fetchall()[0]
        mydb.commit()
        # initialize to be not sick (flag_s = 0)
        pid, lati, longti, times, postc = [str(item) for item in pi_content]
        return {
            "Point_id": pid,
            "Latitude": lati,
            "Longitude": longti,
            "Create_time": times,
            "Postcode": postc
        }

    if request.method == 'DELETE':
        point_del_before = 'Select * From CS411_Point Where Point_id = ' + str(pid)
        cursor.execute(point_del_before)
        cp_content = cursor.fetchall()[0]
        mydb.commit()
        point_del_after = 'Delete From CS411_Point Where Point_id = ' + str(pid)
        cursor.execute(point_del_after)
        print(point_del_after)
        mydb.commit()
        pid, lati, longti, times, postc = [str(item) for item in cp_content]
        return {
            "Point_id": pid,
            "Latitude": lati, 
            "Longitude": longti,
            "Create_time": times,
            "Postcode": postc
        }

def client(request):
    body = request.json_body
    # print(body.Latitude)
    if request.method == 'POST':
    # p_fields = ['Latitude', 'Longitude', 'Create_time']
    # if not validator(input, p_fields):
    #     print('Status: 404 Not Found')
    #     return
        client_insert = 'Insert Into CS411_Client(Postcode) VALUES (' + str(body['Postcode']) + ')'
        print(client_insert)
        cursor.execute(client_insert)

        client_select = 'Select last_insert_id()'
        cursor.execute(client_select)
        # get result of last query
        cid = cursor.fetchall()[0][0]
        # print(cid)
        client_all = 'Select * From CS411_Client Where Client_id = ' + str(cid)
        cursor.execute(client_all)
        c_content = cursor.fetchall()[0]
        mydb.commit()
        # print(c_content)
        cid, ct, s_flag, postc = [str(item) for item in c_content]
        return {
            "Client_id": cid,
            "Creat_time": ct,
            "Sick_or_not": s_flag,
            "Postcode": postc
        }

def client_id(request):
    cid = request.matchdict['id']

    if request.method == 'GET':
        client_get = 'Select * ' + 'From CS411_Client Where Client_id = ' + str(cid)
        cursor.execute(client_get)
        ci_content = cursor.fetchall()[0]
        print(ci_content)
        # initialize to be not sick (flag_s = 0)
        cid, ctime, flag_s, postc = [str(item) for item in ci_content]
        return {
            "Client_id": cid,
            "Creat_time": ctime,
            "Sick_or_not": flag_s,
            "Postcode": postc
        }

    if request.method == 'PUT':
        client_put = 'Update CS411_Client Set Sick_or_not=1 Where Client_id = ' + str(cid)
        cursor.execute(client_put)
        mydb.commit()
        client_id_all = 'Select * From CS411_Client Where Client_id = ' + str(cid)
        cursor.execute(client_id_all)

        ci_content = cursor.fetchall()[0]
        cid, ct, s_flag, postc = [str(item) for item in ci_content]
        mydb.commit()
        # If current user self-reports as infected, put him/her into affected.
        # print(s_flag)
        if s_flag:
            ac_insert = 'Insert Into CS411_Affected_Client(Client_id) VALUES (' + str(cid) + ')'
            cursor.execute(ac_insert)
            mydb.commit()
        return {
            "Client_id": cid,
            "Creat_time": ct,
            "Sick_or_not": s_flag,
            "Postcode": postc
        }

    if request.method == 'DELETE':
        client_del_before = 'Select * From CS411_Client Where Client_id = ' + str(cid)
        cursor.execute(client_del_before)
        cd_content = cursor.fetchall()[0]
        mydb.commit()
        client_del_after = 'Delete From CS411_Client Where Client_id = ' + str(cid)
        cursor.execute(client_del_after)
        mydb.commit()
        client_del_after2 = 'Delete From CS411_Affected_Client Where Client_id = ' + str(cid)
        cursor.execute(client_del_after2)
        mydb.commit()
        # print(cd_content)
        cid, ct, s_flag, postc = [str(item) for item in cd_content]
        return {
            "Client_id": cid,
            "Creat_time": ct,
            "Sick_or_not": s_flag,
            "Postcode": postc
        }

def affected_client_id(request):
    cid = request.matchdict['id']
    print(cid)
    if request.method == 'DELETE':
        ac_del_before = 'Select * From CS411_Client Where Client_id = ' + str(cid)
        cursor.execute(ac_del_before)
        ac_content = cursor.fetchall()[0]
        mydb.commit()
        ac_del_after = 'Delete From CS411_Affected_Client Where Client_id = ' + str(cid)
        cursor.execute(ac_del_after)
        mydb.commit()
        cid, ct, gender, name = [str(item) for item in ac_content]
        return {
            "Client_id": cid,
            "Create_time": ct,
            "Gender": gender,
            "Name": name
        }

def input_state(state):
    complex_state = 'select cac.Create_time_1, count(cc.Client_id )' +\
    'from (select date(Create_time_1) as Create_time_1 ,Client_id from CS411_Affected_Client) as cac ' +\
    'natural join CS411_Client cc join CS411_uszips cu on (cc.Postcode = cu.zip)' +\
    'where cac.Create_time_1 BETWEEN "2020-08-07"-INTERVAL 7 day and "2020-08-07" and cu.state_id = "' + state + '" ' +\
    'group by cac.Create_time_1 ' +\
    'order by cac.Create_time_1'
    cursor.execute(complex_state)
    # print(complex_state)
    count_state = cursor.fetchall()
    return_state = {}
    for item in count_state:
        return_state[str(item[0])] = item[1]
    return return_state
    
def client_state(request):
    # curr_op = request.matchdict['name']
    state = request.matchdict['state']

    if request.method == 'GET':
        return input_state(state)

def input_zip(zip):
    complex_zip = 'select cp.Create_time, count(cp.Point_id )' +\
    'from (select date(Create_time) as Create_time, Point_id , Postcode from CS411_Point) as cp ' +\
    'natural join CS411_Affected_Client_Point cacp join CS411_uszips cu on (cp.Postcode = cu.zip) ' +\
    'where cp.Create_time BETWEEN "2020-08-07"-INTERVAL 7 day and "2020-08-07" and cp.Postcode = "' + zip + '" ' +\
    'group by cp.Create_time ' +\
    'order by cp.Create_time '
    # print(complex_zip)
    cursor.execute(complex_zip)
    count_zip = cursor.fetchall()
    return_zip = {}
    for item in count_zip:
        return_zip[str(item[0])] = item[1]
    return return_zip

def client_zip(request):
    zipc = request.matchdict['zip']

    if request.method == 'GET':
        return input_zip(zipc)


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

        config.add_route('affected_client_id', '/affected/{id}')
        config.add_view(affected_client_id, route_name='affected_client_id', renderer='json')
        app = config.make_wsgi_app()

        config.add_route('client_state', '/state/{state}')
        config.add_view(client_state, route_name='client_state', renderer='json')
        app = config.make_wsgi_app()

        config.add_route('client_zip', '/zip/{zip}')
        config.add_view(client_zip, route_name='client_zip', renderer='json')
        app = config.make_wsgi_app()

        # config.add_route('client_state', '/state/{state}')
        # config.add_view(client_state, route_name='client_state', renderer='json')

        # config.add_route('client_zip', '/zip/{zip}')
        # config.add_view(client_zip, route_name='client_zip}', renderer='json')

    server = make_server('0.0.0.0', 9000, app)
    server.serve_forever()
