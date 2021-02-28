import serial
import time
import datetime
import requests, json
import secrets
import matplotlib.pyplot as plt

# LC_goal
def json_week_get():
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
    dict_str = response.text
    dict = json.loads(dict_str)

    day_list = dict['m2m:cin']['con']
    day_list = day_list[1, -1]
    day_weight = day_list.split(",")
                            
    return day_weight

# data = [deadline, goal, progress]
def json_week_post(value):
    #URL = 'http://127.0.0.1:7579/Mobius/Team_4/LC_goal'
    URL = 'http://203.250.148.89:7579/Mobius/Team_4/Goal'

    list = value

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


def init_today():
    init = [0 for _ in range(7)]
    json_today_post(init)

#"json_today_get()" returns list = [0,1,2,3...,7]
#use in detect_change(last, new) if diff >= 20
#consume = [time, diff]
def show_timeline(consume):

    days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']

    current = [1,2,3,4,5,6,7]
    #current = json_week_get()

    day = consume[0].weekday()
    current[day] = current[day] + consume[1] #sum of drinking at that day

    plt.plot(hours, current)
    plt.show()
    
    json_week_post(current)


    
