import mysql.connector
import simplejson as json
import datetime

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

# array of dictionaries
def converter(input):
    arr = []
    for item in input:
      tmp = json.dumps(item, default = myconverter)
      arr.append(dict(tmp))
    return arr

mydb = mysql.connector.connect(
  host="173.82.151.35",
  user="CS411",
  password="jllecwiXg1",
  port="50036",
  database = "CS411"
)

c = mydb.cursor()
s = c.execute("SELECT * FROM CS411_Point")
h = c.fetchall()
print(h)
print(converter(h))
print(type(converter(h)))
# converter(h))
# print(type(h))