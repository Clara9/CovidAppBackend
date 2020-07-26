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
        point_insert = 'Insert Into CS411_Point(Latitude, Longitude, Postcode) VALUES ('\
         + str(body['Latitude']) + ',' + str(body['Longitude']) + ',' + str(body['Postcode']) + ')'
        cursor.execute(point_insert)
        mydb.commit()
        point_select = 'Select last_insert_id()'
        cursor.execute(point_select)
        # get result of last query
        pid = cursor.fetchall()[0][0]
        # print(cid)
        point_all = 'Select * From CS411_Point Where Point_id = ' + str(pid)
        cursor.execute(point_all)
        p_content = cursor.fetchall()[0]
        print(p_content)
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
        point_del_after = 'Delete From CS411_Client Where Client_id = ' + str(cid)
        cursor.execute(point_del_after)
        # print(cp_content)
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
        # print(client_insert)
        cursor.execute(client_insert)

        client_select = 'Select last_insert_id()'
        cursor.execute(client_select)
        # get result of last query
        cid = cursor.fetchall()[0][0]
        # print(cid)
        client_all = 'Select * From CS411_Client Where Client_id = ' + str(cid)
        cursor.execute(client_all)
        c_content = cursor.fetchall()[0]
        # print(c_content)
        cid, ct, s_flag, postc = [str(item) for item in c_content]
        return {
            "Client_id": cid,
            "Creat_time": ct,
            "Sick_or_not": s_flag,
            "Post_code": postc
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
            "Post_code": postc
        }

    if request.method == 'PUT':
        client_put = 'Update CS411_Client Set Sick_or_not=1 Where Client_id = ' + str(cid)
        cursor.execute(client_put)

        client_id_all = 'Select * From CS411_Client Where Client_id = ' + str(cid)
        cursor.execute(client_id_all)

        ci_content = cursor.fetchall()[0]
        cid, ct, s_flag, postc = [str(item) for item in ci_content]
        # If current user self-reports as infected, put him/her into affected.
        if s_flag == 1:
            ac_insert = 'Insert Into CS411_Affected_Client(Client_id) VALUES (' + str(cid) + ')'
            cursor.execute(ac_insert)
        
        return {
            "Client_id": cid,
            "Creat_time": ct,
            "Sick_or_not": s_flag,
            "Post_code": postc
        }

    if request.method == 'DELETE':
        client_del_before = 'Select * From CS411_Client Where Client_id = ' + str(cid)
        cursor.execute(client_del_before)
        cd_content = cursor.fetchall()[0]
        client_del_after = 'Delete From CS411_Client Where Client_id = ' + str(cid)
        cursor.execute(client_del_after)
        a_client_del_after2 = 'Delete From CS411_Affected_Client Where Client_id = ' + str(cid)
        cursor.execute(client_del_after2)
        # print(cd_content)
        cid, ct, s_flag, postc = [str(item) for item in cd_content]
        return {
            "Client_id": cid,
            "Creat_time": ct,
            "Sick_or_not": s_flag,
            "Post_code": postc
        }

def affected_client(request):
    cid = request.matchdict['id']
    if request.method == 'DELETE':
        ac_del = 'Delete From CS411_Affected_Client_Point Where Client_id = ' + str(client_last_id)
        cursor.execute(ac_del)
        cid, ct, gender, name = [str(item) for item in cd_content]
        return {
            "Client_id": cid,
            "Create_time": ct,
            "Gender": gender,
            "Name": name
        }


def client_complex(request):
    curr_op = request.matchdict['name']
    if request.method == 'GET':
        if curr_op == 'state':
            # complex_q1 = 'Select count(ac.Client_id) ' +\
            # 'From CS411_Affected_Client ac natural join CS411_Client cc join CS411_uszips cu on cc.Postcode = cu.zip' +\
            # 'Group by cu.state_id'
            complex_q1 = 'select count(ac.Client_id) from CS411_Affected_Client ac natural join CS411_uszips cu group by cu.state_id'
            print(complex_q1)
            cursor.execute(complex_q1)
            count_state = cursor.fetchall()[0]
            print(count_state)
            return {
                "number": count_state
            }
        if curr_op == 'zipcode':
            # complex_q2 = 'Select count(cacp.Point_id) ' +\
            # 'From CS411_Affected_Client_Point cacp natural join CS411_Point cp natural join CS411_uszips cu2 ' +\
            # 'Group by cu2.zip'
            cursor.execute(complex_q2)
            count_zipcode = cursor.fetchall()
            print(count_zipcode)
            # return {
            #     "number": count_zipcode
            # }


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

        config.add_route('client_complex', '/client_complex/{name}')
        config.add_view(client_complex, route_name='client_complex', renderer='json')

    server = make_server('0.0.0.0', 9000, app)
    server.serve_forever()
