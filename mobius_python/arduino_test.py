import datetime
import time
import serial
import requests, json
from ast import literal_eval

def json_get():
    #URL = 'http://127.0.0.1:7579/Mobius/Team_4/LC/la'
    URL = 'http://203.250.148.89:7579/Mobius/Team_4/LC/la'


    # X-M2M-Origin needs to be changed
    headers = {'Content-Type' : 'application/vnd.onem2m-res+json; ty=4',
           'X-M2M-Origin' : 'SOrigin',
           'X-M2M-RI' : '12345',
            'Accept' : 'application/json'}

    response = requests.get(URL, headers=headers)
    print(response.status_code)
    print(response.text)
    dict_str = response.text
    dict = json.loads(dict_str)
    
    time = dict['m2m:cin']['con']['time'] 
    weight = dict['m2m:cin']['con']['weight']
    
    return (time, weight)

def json_post(time, weight):
    #URL = 'http://127.0.0.1:7579/Mobius/Team_4/LC'

    URL = 'http://203.250.148.89:7579/Mobius/Team_4/LC'

    list = {'time' : time, 'weight' : float(weight)}

    # X-M2M-Origin needs to be changed
    headers = {'Content-Type' : 'application/vnd.onem2m-res+json; ty=4',
           'X-M2M-Origin' : 'SSJ7GWwpoKD',
           'X-M2M-RI' : '12345',
            'Accept' : 'application/json'}
    data = { "m2m:cin" : { "con" : list }}

    response = requests.post(URL, headers=headers, data=json.dumps(data))
    print(response.status_code)
    print(response.text)


print('serial ' + serial.__version__)

# Set a PORT Number & baud rate

PORT = 'COM3'
BaudRate = 9600

ARD= serial.Serial(PORT,BaudRate)


def Decode(A) :
    A = A[:-2].decode()
    return A

def Ardread() : # get value

    if ARD.readable():

        LINE = ARD.readline()

        code=Decode(LINE)
        code = float(code)
        nowtime = datetime.datetime.now()
        nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')

        json_post(nowDatetime, code)
        
        print("value = %.2f g" % (code))
        
        return code
    
    else :
        print("읽기 실패 from _Ardread_")

def checksetup() :

    if ARD.readable():
        
        LINE = ARD.readline()
        code=Decode(LINE)
        
        while not code.startswith("Finish setup"):
            LINE = ARD.readline()
            code=Decode(LINE)
        
            print(code)

        return 1

#list[time, weight]
    
def detect_change(last, new) :
    
    diff = last[1] - new[1]
    mode = 1 #mode 0 = supple, mode 1 = consume
    
    if diff < 0 :
        diff *= -1
        mode = 0

    if diff >= 20 : # diffrence > 20g 
        print("diff > 20")

        if mode == 0 : #supple
            print("water was replenished")

        else : #consume
            print("water was exhausted")
        
    else :
        print("time renew")
        #time renew
        
    print("renewal")
    # mobius latest value update
    return 1

def timecheck(t) :

    nowtime = datetime.datetime.now()
    timeinterval = nowtime - t
    
    if timeinterval > datetime.timedelta(hours=2) : # time > 2 hours
        print("Drink. You haven't drank water more than 2 hours")
        return 1

    else :
        print("timediffrence", end=' ')
        print(timeinterval)
        return 0   

checksetup()

nowtime = datetime.datetime.now()
#nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')

lastlist = [nowtime, 50.0]

time.sleep(5.0)

print("==========================")
print("start")
print("==========================")

while True:
    
    new_v = Ardread() #new value
    
    #latest_v = 
    
    now = datetime.datetime.now()

    newlist = [now, new_v]
    
    detect_change(lastlist, newlist)
    print("\ndetect...ok")
    timecheck(lastlist[0])
    print("\ntimecheck...ok")

    print("============")

