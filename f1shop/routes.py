from flask import render_template, url_for, flash, redirect
from f1shop import app, db, bcrypt
from f1shop.forms import PilotRegistrationForm, CustomerRegistrationForm, LoginForm
from f1shop.models import User, Post, Item
from flask_login import login_user, current_user, logout_user


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title="About")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = CustomerRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/pilot-register", methods=['GET', 'POST'])
def pilotRegister():
    form = PilotRegistrationForm()
    if form.validate_on_submit():
        flash(f'Pilot Account requested to be created for {form.first_name.data} {form.last_name.data} as a {form.team.data} member', 'success')
        return redirect(url_for('home'))
    return render_template('pilot_register.html', title='Pilot Register', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
