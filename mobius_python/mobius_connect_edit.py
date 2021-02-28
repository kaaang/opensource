import requests, json
import secrets

mp_url = 'http://203.250.148.89:7579/'
cb = 'Mobius/'
ae1 = 'Team_4/'
cnt1 = 'LC'

def json_post(time, weight):
    #URL = 'http://127.0.0.1:7579/Mobius/Team_4/LC'
    #URL = 'http://203.250.148.89:7579/Mobius/Team_4/LC'
    URL = mp_url + cb + ae1 + cnt1
    
    list = {'time' : time, 'weight' : float(weight)}
    token = secrets.token_urlsafe(8)

    # X-M2M-Origin needs to be changed
    headers = {
        'Accept'        : 'application/json',
        'X-M2M-RI'      : '12345',
        'X-M2M-Origin'  : token,
        'Content-Type'  : 'application/vnd.onem2m-res+json; ty=4'
        }
    data = { "m2m:cin" : { "con" : list } }

    response = requests.post(URL, headers=headers, data=json.dumps(data))
    print(response.status_code)
    print(response.text)

json_post(1,111)
