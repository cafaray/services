import json
import userData
import hashlib
import getpass

def getCodeUser():
    strUser = input('Which user do you want to auth?: ')
    user = userData.getUser(strUser);
    if user == None: 
        print("The user doesn't exists ...")
    elif user['status'] != 'A':        
        print("The user doesn't have a valid ststus to start a session [" + user['status'] + "]... ")
    else:
        fakeUser = user['user'][:1] + '***' + user['user'][len(user['user'])-1]
        print('Enter the password for', fakeUser, ':')
        phrase = getpass.getpass() 
        if len(phrase)>0:        
            phrase = hashlib.md5(phrase.encode()).hexdigest()
            #print('user:', user['user'], 'phrase to send:', phrase)
            user = userData.auth(user['user'], phrase)
            #print(user)
            if user['status']!='A':
                print("The password isn't active, please complete the activation process ...")
            else:
                return user['code']
        else:
            print('Incorrect value for phrase ...')
    return None

def getUser(strUser):
    data = dict()
    user = userData.getUser(strUser);
    if user == None: 
        data = {'error':'User does not exist'}
    elif user['status']!='A':
        data = {'error':'User is not active yet, first you need to activate it.'}
    else:
        data = {'username': user, 'error': '0'}
    
    js = json.dumps(data, indent=4)   
    return js

def authUser(strUser, strSecret):
    data = dict()
    user = userData.auth(strUser, hashlib.md5(strSecret.encode()).hexdigest())
    if user == None: 
        data = {'error':'Incorrect phrase'}
    #elif user['status']!='A':
    #    data = {'error':'User is not active yet, first you need to activate it.'}
    else:
        data = {'username': user, 'error': '0'}
    
    js = json.dumps(data, indent=4)   
    return js

def do_upload_file(files):
    data = dict()
    archivo = files['the_file']
    try:
        archivo.save('/Users/cofa/py4e/'+archivo.filename)
        fname = open('/Users/cofa/py4e/'+archivo.filename)
        content = fname.read()
        data = {'error':0, 'archivo':archivo.filename, 'data-retrieved':len(content)}        
    except IOError as e:
        data = {'error':e.strerror}
    js = json.dumps(data, indent=4) 
    return js

def do_the_fileupload_form():
    formulario_head = '''<form method = 'post' enctype="multipart/form-data">'''
    file = '''Usuario: <input type='file' name='the_file' /><br />'''
    formulario_end = '''</form>'''   
    boton = '''<input type = 'submit' value = 'Enviar' /> '''
    boton_logoff = '''<p><a href='/logoff'>Exit</a></p>'''
    return formulario_head + file + boton + formulario_end + boton_logoff

def show_the_login_form():
    formulario_head = '''<form method = 'post'>'''
    usuario = '''Usuario: <input type='text' name='username' /><br />'''
    password = '''Password: <input type='password' name='password' /><br />'''
    formulario_end = '''</form>'''   
    boton = '''<input type = 'submit' value = 'Enviar' /> '''
    return formulario_head + usuario + password + boton + formulario_end