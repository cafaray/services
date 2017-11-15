from flask import Flask, request, session, redirect, url_for, escape, render_template, make_response
from functions import *
import os
app = Flask('__name__')

@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error404.html'), 404)
    resp.headers['X-SECRET-KEY'] = b'\x87z\x07r\x8bm\xe58\xa4w\x14\x9f\xee*\xf6;\x1a\x7f\xd2\x81H\xe8\xdb\xcc'
    return resp
    #return render_template('error404.html'), 404

@app.route('/')
def index():
    if 'username' in session:
        print('logged in session as %s' % escape(session['username']))
        return redirect(url_for('upload_image'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #respuesta = do_the_login(request.form['username'], request.form['password'])        
        respuesta = getUser(request.form['username'])
        if 'username' in respuesta:
            session['username'] = request.form['username']
            #resp = make_response(render_template('validLogin.htm'))
            #resp.set_cookie('username', request.form['username'])            
            return redirect(url_for('validLogin'))
            #return resp            
        else:
            return respuesta
    else:
        # for queryparams: searchword = request.args.get('key', '')
        #return show_the_login_form()
        return render_template('login.htm')

@app.route('/validLogin', methods=['POST', 'GET'])
def validLogin():
    if request.method=='GET':
        return render_template('validLogin.htm')
    elif request.method=='POST':
        username = escape(session['username'])
        print('username:',username)  
        user = authUser(username, request.form['usersecret'])
        print(user)
        if 'username' in user:
            print('Autenticado')
            session['username'] = username + '1'
            session['auth'] = '1'
            resp = make_response(redirect(url_for('upload_image')))
            return resp
        else:
            print('No autenticado')
            session['auth'] = '0'
            session.pop('username', None)
            return redirect(url_for('index'))
    
@app.route('/upload', methods=['POST', 'GET'])
def upload_image():    
    if request.method=='POST':
        return do_upload_file(request.files)
    else:
        return do_the_fileupload_form()

@app.route('/logoff', methods=['GET'])
def logoff():
    session.pop('username', None)
    return redirect(url_for('index'))

sk = os.urandom(24)
#print('secret key:', sk)
app.secret_key = sk

if __name__ == '__main__':
    app.run()