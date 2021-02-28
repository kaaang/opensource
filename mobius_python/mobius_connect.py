import requests, json

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
