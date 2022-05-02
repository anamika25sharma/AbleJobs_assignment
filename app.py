from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from flask_pymongo import PyMongo
from pymongo import *
app = Flask(__name__)

app.config['MONGODB_NAME'] = 'assignment'
app.config['MONGO_URI'] = 'mongodb url'
app.config['SECRET_KEY'] = "anamikasharma"

mongo = PyMongo(app)


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('main'))
    return render_template('home.html')


@app.route('/index')
def main():
    return render_template('home.html')


@app.route('/user/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = mongo.db.user
        login_user = user.find_one({'username': request.form['Uname']})
        if login_user:
            if request.form['password'] == login_user['password']:
                session['username'] = request.form['Uname']
                return redirect(url_for('form'))
            return render_template('login.html')
        return render_template('login.html')
    return render_template('login.html')


@app.route('/user/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = mongo.db.user
        reg_user = user.find_one({'username': request.form['username']})
        if reg_user is None:
            user.insert(
                {'username': request.form['username'], 'email': request.form['email'], 'password': request.form['password']})
            session['username'] = request.form['username']
            return redirect(url_for('form'))
        return redirect(url_for('home'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/opening/form')
def form():
    if 'username' in session:
        return render_template('opening_form.html')
    else:
        return redirect(url_for('login'))


@app.route('/requirement', methods=['POST', 'GET'])
def requirement():
    if 'username' in session and request.method == 'POST':
        company = session['username']
        job = mongo.db.job
        job.insert({'company': company, 'jobRole': request.form['role'], 'jobDescription': request.form[
                    'jdescription'], 'placeOfWork': request.form['place'], 'phone': request.form['phone']})
        return redirect(url_for('form'))
    return redirect(url_for('login'))


@app.route('/user/dashboard', methods=['GET'])
def company_dash():
    if 'username' in session:
        company = session['username']
        job = mongo.db.job
        job_list = job.find({"company": company})
        return render_template('company_dash.html', job_list=job_list)
    return redirect(url_for('login'))


@app.route('/admin/dashboard', methods=['GET'])
def adminDashboard():
    if 'username' in session and session['username'] == "admin":
        jobs = mongo.db.job
        all_list = jobs.find()
        return render_template('admin_dash.html', all_list=all_list)
    return render_template('login.html')


if __name__ == '__main__':
    # app.secret_key = "hello"
    app.run(debug=True)
