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
