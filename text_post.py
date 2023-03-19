import requests
from GoogleNews import GoogleNews
from summary import summary_generator
from ln_auth import auth, headers
from instabot import Bot



credentials = 'credentials.json'
access_token = auth(credentials)
headers = headers(access_token)


def user_info(headers):
    response = requests.get('https://api.linkedin.com/v2/me', headers=headers)
    user_info = response.json()
    return user_info


user_info = user_info(headers)
urn = user_info['id']


api_url = 'https://api.linkedin.com/v2/ugcPosts'
author = f'urn:li:person:{urn}'


def post_on_linkedin(message , link_heading , link ):
    requests.post("https://api.linkedin.com/v2/assets?action=registerUpload")

    post_data = {
        "author": author,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": message
                },
                "shareMediaCategory": "ARTICLE",
                "media": [
                    {
                        "status": "READY",
                        "originalUrl": link,
                        "title": {
                            "text": link_heading
                        }
                    }
                ]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    if __name__ == '__main__':
        r = requests.post(api_url, headers=headers, json=post_data)
        r.json()

GNews = GoogleNews(period="10d")
search=input("\n\nSELECT THE FIELD OF THE CONTENT OF THE POST : ")
GNews.search(search)
print()
result = GNews.result()

links = GNews.get_links()

title = GNews.get_texts()
print("TOTAL ARTICLES SCRAPPED : ",end=" ")
print(len(links))
print()

for i in range(len(links)):
    print(f'|--------  ARTICLE NO. {i+1}  --------|')
    link_heading = title[i]
    print("TITLE  :  ",end=" ")
    print(link_heading)
    print()
    
    link = links[i]
    print("LINK  :  ",end=" ")
    print(link)
    print()
    
    message = summary_generator(links[i])
    print("TEXT :- ")
    print(message)
    print() 
    print()
    
    choice = input("SHOULD THE ABOVE ARTICLE BE POSTED ON LINKEDIN ? ( Y / N )   :   ")
    print()
    if choice=='Y' or choice=='y':
        post_on_linkedin(message , link_heading , link )
    else:
        print("ALRIGHT .  PLEASE SEE THE NEXT POST .")
        print() 
    
        

GNews.clear()



