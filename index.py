from flask import Flask, request, render_template, redirect, session, url_for
from app.services.processUsers import processUsers
from flask_bootstrap import Bootstrap
from app.models.user import User
from functools import wraps

app = Flask(__name__)
app.secret_key = b'>\xf9Mg}\x8b\xffo\x9d\x86\xa1\x8f\xe6\x85G\xc4'
Bootstrap(app)

def login_required(f):
    @wraps(f)
    def warp(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            return redirect('/')
    return warp

def mustChange(f):
    @wraps(f)
    def warp(*args,**kwargs):
        if session['user']['mustChangePassword']:
            return redirect("/changePassword")
        else:
            return f(*args,**kwargs)    
    return warp

@app.route('/changePassword',methods=['GET','POST'])
def changePassword():
    if request.method == "POST":
        ans = User().changePassword()
        if ans[1] == 200:
            return redirect(url_for('dashboard'))
        else:
            return ans
    return render_template("changePassword.html")

@app.route('/')
def helloWorld():
    return render_template("index.html")

@app.route('/uploadCSV',methods=['GET','POST'])
def postFile():
    if request.method == "POST":
        if request.files["file"]:      
            processUsers(request.files["file"])       
        return redirect(request.url)
    return render_template("upload.html")

@app.route('/login', methods = ['POST'])
def login():
    ans = User().login()
    if ans[1] == 200:
        return redirect(url_for('dashboard'))
    else:
        return ans

@app.route('/dashboard', methods = ['GET','POST'])
@login_required
@mustChange
def dashboard():
    return render_template('dashboard.html')    


@app.route('/signout', methods = ['GET'])
@login_required
def signout():
    User().signout()
    return redirect('/')

if __name__ == '__main__':
    app.run(port=3000, debug = True)
