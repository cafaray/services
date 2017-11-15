from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'index'

@app.route('/hello')
def hello():
    return 'Hello'

@app.route('/hello/<user>')
def hello_user(user):
    if user is None:
        return 'Hello World!'
    else:
        return 'Hello %s' % user

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id
 
if __name__ == '__main__':
    app.run()