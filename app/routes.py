from app import app
from app.models import User, Log
from app.forms import LoginForm, SignupForm, NewLog
from flask import render_template, Response, session, redirect, url_for, flash

@app.route('/')
@app.route('/index')
def index():
    if not logged_in():
        return redirect('login')
    user = current_user()
    return render_template("index.html", current_user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if logged_in():
        return redirect('index')
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        u = User.get_with_username(username)
        if u and u.verify_password(password):
            session['logged_in'] = True
            session['current_user'] = u._id
            res = redirect(url_for('index'))
            return res
        else:
            flash('Invalid username or password')
            res = redirect(url_for('login'))
            return res
    return render_template("login.html", form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if logged_in():
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User(_username=username, _email=email)
        user.set_password(password)
        user.save()
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session['current_user'] = 0
    return redirect('login')
@app.route('/logs', methods=['GET', 'POST'])
def logs():
    if not logged_in():
        return redirect(url_for('login'))
    user = current_user()
    form = NewLog()
    if form.validate_on_submit():
        type_e = form.activity_type.data
        time = form.time.data
        hr = form.heart_rate.data
        l = Log(activity_type=type_e, time=time, hr=hr, user_id=user._id)
        l.save()
    return render_template('logs.html', form=form, current_user=user)

def logged_in():
    try:
        if session['logged_in']:
            return True
        else:
            try:
                return request.cookies.get('logged_in') == "True"
            except:
                return False
    except:
        return False
def current_user():
    return User.get_with_id(session['current_user'])


