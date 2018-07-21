#!/usr/bin/python3

import requests as r
import sys

api_key = "KL4rBsAnfXACnSEB1xGOAe30"
api_secret = "zGETG3h:L2WS*aS*jpRW-_&c"

req = {'clientId': api_key, 'clientSecret': api_secret}

api_path = "https://us-central1-sandbox-silverberry.cloudfunctions.net/api/v1/external-apps/"

auth_post = r.post(url = "https://us-central1-sandbox-silverberry.cloudfunctions.net/api/v1/external-apps/authenticate", data = req)

token = auth_post.json()['accessToken\u200b']

headers = {"Authorization": "Bearer " + token}

#adding a new user
user_dict = { 
     
    "firstName": "Liz",
    "lastName": "Wayne",
    "gender": "female",
    "email": "284074@nwytg.net"
    }

user_get = r.get(url = "https://us-central1-sandbox-silverbe\
rry.cloudfunctions.net/api/v1/external-apps/users", headers = headers)

#user_post = r.post(url = api_path + 'users', headers = headers#, data = user_dict)

userId = user_get.json()[0]['userId']

#report_get = r.get(url = api_path + 'users/' + userId + 'repor#ts/' +  

get_shop = r.get(url = api_path + 'shop/products', headers = headers)

prod_ids = []

for i in get_shop.json():
    prod_ids.append(i['productId'])

order_ids = []
for i in prod_ids:
    order_posts = r.post(api_path + 'users/' + userId + '/order', headers= headers, data = {'productId':i})
    order_ids.append(order_posts.json()['orderId'])

print(order_ids)

