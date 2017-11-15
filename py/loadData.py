import json
import userData

# create database:
userData.createDataStructure()

# open json to start the data inserction to database:
# -- starts with functions:
fname = open('json/functions.json')
fjson = fname.read();
info = json.loads(fjson)

functions = list()
for item in info:
    functions.append([item['function'], item['endpoint']])

userData.insertFunctions(functions)

# then the groups:
fname = open('json/groupFunctions.json')
fjson = fname.read();
info = json.loads(fjson)

groups = dict()
for item in info:    
    groups[item['id']] = item['functions']
    
userData.insertGroupFunctions(groups)

# finally the user stack
fname = open('json/userData.json')
fjson = fname.read();
info = json.loads(fjson)
#print('User count:', len(info))
users = dict()
for item in info:
    users[item['user']] = (item['hash'], item['mail'], item['lastPhrase'], item['groups'])
    
userData.insertUser(users)