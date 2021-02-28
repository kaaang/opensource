import datetime
import time
import serial
import requests, json
import secrets
from pyfcm import FCMNotification

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

    token = secrets.token_urlsafe(8)

    # X-M2M-Origin needs to be changed
    headers = {'Content-Type' : 'application/vnd.onem2m-res+json; ty=4',
           'X-M2M-Origin' : token,
           'X-M2M-RI' : '12345',
            'Accept' : 'application/json'}
    data = { "m2m:cin" : { "con" : list }}

    response = requests.post(URL, headers=headers, data=json.dumps(data))
    print(response.status_code)
    print(response.text)

def json_goal_get():  
    #URL = 'http://127.0.0.1:7579/Mobius/Team_4/LC_goal/la'
    URL = 'http://203.250.148.89:7579/Mobius/Team_4/Goal/la'

    # X-M2M-Origin needs to be changed
    headers = {'Content-Type' : 'application/vnd.onem2m-res+json; ty=4',
           'X-M2M-Origin' : 'SOrigin',
           'X-M2M-RI' : '12345',
            'Accept' : 'application/json'}

    response = requests.get(URL, headers=headers)
    print(response.status_code)
    print(response.text)
    print("")
    dict_str = response.text
    dict = json.loads(dict_str)

    deadline = dict['m2m:cin']['con']['deadline'] 
    goal = dict['m2m:cin']['con']['goal']
    progress = dict['m2m:cin']['con']['progress']

    deadline = datetime.datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S')
    value = [deadline, float(goal), float(progress)]
    
    return value

def json_goal_post(value):
    # value = [deadline, goal, progress]
    
    #URL = 'http://127.0.0.1:7579/Mobius/Team_4/LC_goal'
    URL = 'http://203.250.148.89:7579/Mobius/Team_4/Goal'

    list = {'deadline' : value[0], 'goal' : value[1], 'progress' : value[2]}

    token = secrets.token_urlsafe(8)
    
    # X-M2M-Origin needs to be changed
    headers = {'Content-Type' : 'application/vnd.onem2m-res+json; ty=4',
           'X-M2M-Origin' : token,
           'X-M2M-RI' : '12345',
            'Accept' : 'application/json'}
    data = { "m2m:cin" : { "con" : list }}

    response = requests.post(URL, headers=headers, data=json.dumps(data))
    print(response.status_code)
    print(response.text)
    print("")

def set_goal():
    day = int(input("Day:"))
    goal = float(input("Goal:"))
    
    nowtime = datetime.datetime.now()
    deadline = nowtime + datetime.timedelta(days=day)
    deadline = deadline.strftime('%Y-%m-%d %H:%M:%S')

    value=[deadline, goal, 0]
    json_goal_post(value)
    
def show_goal_progress(diff): #diff[time, diffrence]
    value = []
    current = json_goal_get() #list[deadline, goal, progress]

    current[2] = current[2] * current[1] / 100 + diff[1] #percent -> ml
    
    nowtime = diff[0]
    percent = current[2] / current[1] * 100 #ml -> percet
    percent = round(percent, 2) 
    if (current[0] - diff[0]).days < 0: #over the deadline
        print("Deadline is over.")
        set_goal()
        return
    elif current[1] <= current[2]: #goal<=progress
        print("Achieve goal")
        set_goal()
        return
    else:
        print("Achievement rate:%.2f%%" % percent)

    current[2] = percent
    current[0] = current[0].strftime('%Y-%m-%d %H:%M:%S')
    json_goal_post(current) #updated progress -> current[2] + diff[1]

def str_to_change(time_str):
    
    dateFormatter = '%Y-%m-%d %H:%M:%S'
    return datetime.datetime.strptime(time_str, dateFormatter)

def detect_change(last, new) :

    diff = last[1] - new[1]
    mode = 1 #mode 0 = supple, mode 1 = consume
    
    if diff < 0 :
        diff *= -1
        mode = 0

    if diff >= 20 : # diffrence > 20g
        last = new
        lasttime = last[0].strftime('%Y-%m-%d %H:%M:%S')
        json_post(lasttime, last[1])

        if mode == 0 : #supple
            print("")
            print("water was replenished")

        else : #consume
            print("")
            print("water was exhausted")
            data = [last[0], diff]
            show_goal_progress(data)
        
    print("renewal")
    return last

def alertphone():
    push_service = FCMNotification(api_key="AAAANwyTgsY:APA91bFTQwDKyQcozCiu9DJkmk8bZ2dZgQ9dZqxAyk5vTvYiFHjBR0AVkHGsAuCsUHNG8eCL1dqPwcRVgQv1NwtAVFn_Sku4TVTkcHA9leq0fMEbGHeFxEopSpbJKlIUEWAi25NH4nt0")
    registration_id = "fDYSqFYPSwuk8-I0LdfnbA:APA91bHSZI2_9z0_QwMWdt5K3dcIwPDyNdkKVoX_DYWF7Mxw9ex0NpbFLGyftXUzgIup7GcgNxZUG7V_oLUzDIp3u8bdvAP_EE35tyPy7Mte0xlElztSwl1S8BI4PImm24ZcecDLAO4u"

    message_title = "[Hydration Alert]"
    message_body = "It's been two hours since you drank water."
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

    print(result)
    
def timecheck(t) :
    nowtime = datetime.datetime.now()
    timeinterval = nowtime - t
    
    #if timeinterval > datetime.timedelta(hours=2) : # time > 2 hours
    if timeinterval > datetime.timedelta(minutes=1):
        print("sent notification")
        alertphone()
        return 1

    else :
        print("timediffrence", end=' ')
        print(timeinterval)
        return 0   

def Decode(A) :
    A = A[:-2].decode()
    return A

def Ardread() : # get value

    if ARD.readable():

        LINE = ARD.readline()

        code=Decode(LINE)
        code = float(code)
        if (code < 0) :
            code = 0
        
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
    
#### MAIN START
print('serial ' + serial.__version__)

# Set a PORT Number & baud rate

PORT = 'COM3'
BaudRate = 9600

ARD= serial.Serial(PORT,BaudRate)

checksetup()

nowtime = datetime.datetime.now()
lastlist = [nowtime, -12345]
set_goal()
time.sleep(2.0)

print("==========================")
print("start")
print("==========================")

while True:
    
    new_v = Ardread() #new value
    
    now = datetime.datetime.now()

    newlist = [now, new_v]
    
    if (lastlist[1] < -1000): # if last value == initial value
        lastlist = newlist
        lasttime = lastlist[0].strftime('%Y-%m-%d %H:%M:%S')
        json_post(lasttime, lastlist[1])
        
    else :
        lastlist = detect_change(lastlist, newlist)
        print("\ndetect...ok")
        timecheck(lastlist[0])
        print("\ntimecheck...ok")

    print("============")
    time.sleep(10.0)

