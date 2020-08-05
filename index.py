from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import mysql.connector
import datetime
from datetime import date
import random
from math import radians, cos, sin, asin, sqrt

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
        # a_point_insert = "Insert Into CS411_Affected_Client_Point(Point_id, Client_id) " + "Values (" + str(pid) + ", " + str(body['Client_id']) + ")"
        # print(a_point_insert)

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
            ac_insert = 'Insert Into CS411_Affected_Client(Client_id) VALUES (' + str(cid) + ') '
            cursor.execute(ac_insert)
            mydb.commit()
            body = request.json_body
            pids = body['pids']
            temp= "Start Transaction; "
            for pid in pids:
                ap_insert = 'Insert Into CS411_Affected_Client_Point(Client_id, Point_id) VALUES (' + str(cid) + ',' + str(pid) + '); '
                temp = temp + ap_insert
                print(temp)
            temp = temp + " Commit;"
            print(temp)
            cursor.execute(temp,multi=True)
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
    'where cac.Create_time_1 BETWEEN "' + str(date.today()) + '"-INTERVAL 7 day and "' +  str(date.today()) + '" and cu.state_id = "' + state + '" ' +\
    'group by cac.Create_time_1 ' +\
    'order by cac.Create_time_1'
    # print(complex_state)
    cursor.execute(complex_state)
    states = []
    count_state = cursor.fetchall()
    for item in count_state:
        states.append(item[1])
    return states
    
def client_state(request):
    # curr_op = request.matchdict['name']
    state = request.matchdict['state']

    if request.method == 'GET':
        return input_state(state)

def input_zip(zip):
    complex_zip = 'select cp.Create_time, count(cp.Point_id )' +\
    'from (select date(Create_time) as Create_time, Point_id , Postcode from CS411_Point) as cp ' +\
    'natural join CS411_Affected_Client_Point cacp join CS411_uszips cu on (cp.Postcode = cu.zip) ' +\
    'where cp.Create_time BETWEEN "' + str(date.today()) + '"-INTERVAL 7 day and "' +  str(date.today()) + '"and cp.Postcode = "' + zip + '" ' +\
    'group by cp.Create_time ' +\
    'order by cp.Create_time '
    print(complex_zip)
    cursor.execute(complex_zip)
    count_zip = cursor.fetchall()
    zips = []
    for item in count_zip:
        zips.append(item[1])
    return zips

def client_zip(request):
    zipc = request.matchdict['zip']

    if request.method == 'GET':
        return input_zip(zipc)

# this function is used to calculate the distance between two points based on the latitude and longtitude, true if distance is less than 50 meters
# learn this function mainly from the internet
def geodistance(lon1,lat1,lon2,lat2):
    lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)]) # transfer latitude and longtitude to the radians
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a=sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    distance = 2 * asin(sqrt(a)) * 6371 * 1000 # radians of the earth is 6371km
    distance = round(distance,3)
    return distance <= 50 #return distance in meters

# measure the time difference, true if difference is less than 20 minute, which is 1200 seconds
def timedifference(datetime1, datetime2):
    diff = abs(datetime1 - datetime2)
    return (diff.days == 0) and (diff.seconds < 1200)

#this function is used to check if any clients are too closed to the affected_client
#@return: return a list of tuple, tuple is (pid, count)
#pid refers to the points that might be in risk of being affected, count is the number of point that is in danger distance with the point.
def advanced(request):
    cid = request.matchdict['id']
    if request.method == 'GET':
        print('start my advanced function')
        findallaffected = 'Select p.Latitude lat, p.Longitude lon, p.Create_time time From CS411_Affected_Client_Point acp join CS411_Point p on acp.Point_id = p.Point_id'
        cursor.execute(findallaffected) #cursor execute the sql query
        affectedlist = [] #list of affected client, each element here is a tuple like (double, double, datetime)
        for lat, lon, time in cursor:
            affectedlist.append((float(lon),float(lat),time))
        mydb.commit()
        #print(affectedlist)
        getunaffected = "Select Point_id, Latitude, Longitude, Create_time From CS411_Point where Point_id = " + str(cid)
        cursor.execute(getunaffected)

        indangerdict = {} #list of point that has risk of being affected, each element here is a tuple like (string(point_id), int(number of closed affected points))
        for Point_id, Latitude, Longitude, Create_time in cursor:
            #print(pid2)
            latitude2 = float(Latitude)
            longtitude2 = float(Longitude)
            datetime2 = Create_time
            count = 0
            c = 0
            for ele in affectedlist:
                c += 1
                if c % 10 == 0:
                    print('ten completed')
                if geodistance(ele[0], ele[1], longtitude2, latitude2) and timedifference(ele[2], datetime2):
                    count += 1
            if count > 0:
                print('one danger')
            indangerdict[Point_id] = str(count)
        mydb.commit()
        #print('search resut is'+ str(c))
        return indangerdict
#new added for advanced

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

        #new added for advanced
        config.add_route('advanced', '/advanced/{id}')  #/advanced means what should I write in the request
        config.add_view(advanced, route_name='advanced', renderer='json') # advanced here should be the function to call
        app = config.make_wsgi_app()

        # config.add_route('client_state', '/state/{state}')
        # config.add_view(client_state, route_name='client_state', renderer='json')

        # config.add_route('client_zip', '/zip/{zip}')
        # config.add_view(client_zip, route_name='client_zip}', renderer='json')

    server = make_server('0.0.0.0', 9000, app)
    server.serve_forever()
