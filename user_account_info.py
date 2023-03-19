import requests 
from ln_auth import headers , auth 

def user_info(headers):
    response = requests.get('https://api.linkedin.com/v2/me' , headers=headers)
    user_info = response.json()
    return user_info


if __name__ == '__main__':
    credentials = 'credentials.json' 
    access_token = auth(credentials) 
    headers = headers(access_token) 
    user_info = user_info(headers)
    print(user_info)
    urn = user_info['id']