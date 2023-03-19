import json
import string
import random
import requests
import webbrowser
from urllib.parse import urlparse , parse_qs


def auth(credentials):
    creds = read_creds("credentials.json")
    print()
    print(creds)
    print()
    client_id = creds["client_id"]
    client_secret = creds["client_secret"]
    redirect_uri = creds["redirect_uri"]
    api_url = "https://www.linkedin.com/oauth/v2"
    
    if 'access_token' not in creds.keys():
        args = client_id , client_secret , redirect_uri 
        auth_code = authorize(api_url,*args)
        access_token = refresh_token(auth_code,*args)
        creds.update({'access_token':access_token})
        save_token(credentials,creds) 
    else: 
        access_token = creds['access_token'] 
    return access_token 


def headers(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}' ,
        'cache-control': 'no-cache' ,
        'X-Restli-Protocol-Version': '2.0.0'
    }
    return headers 


#Reading Credentials
def read_creds(filename):
    with open(filename) as f:
        credentials = json.load(f)
    return credentials
    

creds = read_creds("credentials.json")
client_id = creds["client_id"]
client_secret = creds["client_secret"]
redirect_uri = creds["redirect_uri"]


def create_CSRF_token():
    letters = string.ascii_lowercase 
    token = ''.join(random.choice(letters) for i in range(20))
    return token


api_url = "https://www.linkedin.com/oauth/v2"


def parse_redirect_uri(redirect_response):
    url = urlparse(redirect_response)
    url = parse_qs(url.query)
    return url['code'][0]


def authorize(api_url,client_id,client_secret,redirect_uri):
    csrf_token = create_CSRF_token() 
    parameters = {
        'response_type': 'code' ,
        'client_id': client_id ,
        'redirect_uri': redirect_uri ,
        'state': csrf_token ,
        'scope': 'r_liteprofile,r_emailaddress,w_member_social'
    }

    response = requests.get(f'{api_url}/authorization',params=parameters)

    webbrowser.open(response.url)
    print(response.url)

    redirect_response = input('Paste the full redirect url here : ')
    auth_code = parse_redirect_uri(redirect_response)
    return auth_code


def save_token(filename , data):
    data = json.dumps(data , indent = 4)
    with open(filename , 'w') as f:
        f.write(data)

def refresh_token(auth_code , client_id , client_secret , redirect_uri):
    access_token_url = 'https://www.linkedin.com/oauth/v2/accessToken'      
    data = {
        'grant_type' : 'authorization_code' ,
        'code' : auth_code ,
        'redirect_uri' : redirect_uri , 
        'client_id' : client_id , 
        'client_secret' : client_secret 
    }

    response = requests.post(access_token_url , data=data , timeout=30)
    response = response.json() 
    print(response)
    access_token = response['access_token'] 
    return access_token 


if __name__ == '__main__': 
    credentials = 'credentials.json' 
    access_token = auth(credentials)
