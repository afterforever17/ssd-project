from flask import render_template, url_for, flash, redirect
from f1shop import app
from f1shop.forms import PilotRegistrationForm, CustomerRegistrationForm, LoginForm
from f1shop.models import User, Post, Item


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
    form = CustomerRegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data =='admin@blog.com' and form.password.data =='password':
            flash(f'You have been logged in!', 'success')
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
