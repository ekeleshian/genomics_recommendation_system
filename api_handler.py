#!/usr/bin/python3

import requests as r
import sys
import random, string  
from subprocess import Popen,PIPE, call
import time

name = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(7))
api_key = "KL4rBsAnfXACnSEB1xGOAe30"
api_secret = "zGETG3h:L2WS*aS*jpRW-_&c" 
file = sys.argv[1]
print(name , file)

req = {'clientId': api_key, 'clientSecret': api_secret}

api_path = "https://us-central1-sandbox-silverberry.cloudfunctions.net/api/v1/external-apps/"

auth_post = r.post(url = "https://us-central1-sandbox-silverberry.cloudfunctions.net/api/v1/external-apps/authenticate", data = req)

token = auth_post.json()['accessToken\u200b']

headers = {"Authorization": "Bearer " + token}
email =  name + "@nwytg.net" 
#adding a new user
user_dict = { 
     
    "firstName": name ,
    "lastName": name ,
    "gender": "female",
    "email": email 
    }

user_post = r.post(url = api_path + 'users', headers = headers, data = user_dict)
usrid = user_post.json()['userId']
path = api_path + 'users/' + usrid + '/reports?format=csv' 
print("uploading data")
cmd = 'curl -X POST "https://us-central1-sandbox-silverberry.cloudfunctions.net/api/v1/external-apps/users/' + usrid + '/genotypeFile" -H "accept: application/json" -H "Authorization: Bearer ' + token +  '" -H "Content-Type: multipart/form-data" -F "file=@' + file + ';type=application/x-zip-compressed"' 
process= Popen([cmd],shell=True,stdin=PIPE,stderr=PIPE)
(output, err) = process.communicate()  
p_status = process.wait()
prod_ids = ['10371522118',
'10384517382',
'10384531334',
'10384576966',
'10384586758',
'10707235093',
'10707237461',
'11699507925',
'121891258389',
'223220039701',
'223270961173',
'223272960021']

print("\nsubmtting orders")
order_ids = []
order_posts = r.post(api_path + 'users/' + usrid + '/order', headers= headers, data = {'productId':prod_ids})
orderid = order_posts.json()['orderId']
print("waiting for results")
time.sleep(5)
cmd2 = 'curl -X GET "' + path + '" -H "accept: application/pdf" -H "Authorization: Bearer ' + token + '" > ./completed/' + name + ".csv"
process2 = Popen([cmd2],shell=True,stdin=PIPE,stderr=PIPE)
(output, err) = process2.communicate()  
p_status = process2.wait()
print( output , err)

# data = {'file': open('./0001.male.hispanic.atheist.txt','rb')}

# postgene = r.post(url = api_path + 'users/' + usrid + '/genotypeFile' , files=dict(file=open('./0001.male.hispanic.atheist.txt', 'rb'))  , headers = headers )


# 

# print(cmd)
# process= Popen([cmd],shell=True,stdin=PIPE,stderr=PIPE)
# (output, err) = process.communicate()  
# p_status = process.wait()
# print(err)
# print(output)



# report = r.post(api_path + 'users/' + userId + '/reports' , headers= headers)
# print(report.json())

