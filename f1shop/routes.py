import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from f1shop import app, db, bcrypt
from f1shop.forms import PilotRegistrationForm, CustomerRegistrationForm, LoginForm, CustomerUpdateAccountForm, ItemForm
from f1shop.models import User, Post, Item, PilotRequest, ItemRequest
from flask_login import login_user, current_user, logout_user, login_required


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
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/pilot-register", methods=['GET', 'POST'])
def pilotRegister():
    form = PilotRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        pilot_request = PilotRequest(action = 'create',
                                     pilot_name=form.first_name.data + ' ' + form.last_name.data, 
                                     pilot_email = form.email.data, pilot_password = hashed_password, 
                                     pilot_team = form.team.data)
        db.session.add(pilot_request)
        db.session.commit()
        flash(f'Pilot Account requested to be created for {form.first_name.data} {form.last_name.data} as a {form.team.data} member', 'success')
        return redirect(url_for('home'))
    return render_template('pilot_register.html', title='Pilot Register', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    i.save(picture_path)
    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = CustomerUpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        if current_user.role == 'pilot':
            pilot_request = PilotRequest(action = 'edit',
                                         pilot_id = current_user.id,
                                         pilot_name = form.username.data,
                                         pilot_email = form.email.data,
                                         pilot_password = current_user.password,
                                         pilot_team = current_user.team)
            db.session.add(pilot_request)
            flash('Your account update has been requested!', 'success')
        else:
            current_user.username = form.username.data
            current_user.email = form.email.data
            flash('Your account has been updated!', 'success')

        db.session.commit()
        return redirect(url_for('account'))
    elif request.method =='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) 
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/new-item", methods=['GET', 'POST'])
@login_required
def new_item():
    form = ItemForm()
    if form.validate_on_submit():
        picture_file = save_picture(form.picture.data)
        item_request = ItemRequest(action='create', 
                                   item_name = form.item_name.data, 
                                   item_image_file = picture_file, 
                                   item_price = form.price.data, 
                                   owner_id = current_user.id)
        db.session.add(item_request)
        db.session.commit()
        flash('Item request submitted!', 'success')
        return redirect(url_for('new_item'))
    return render_template('new_item.html', form = form, owner_name = current_user.username)



@app.route("/requests", methods=['GET', 'POST'])
@login_required
def requests():
    if current_user.role != 'admin':
        flash('Access Denied', 'danger')
        return redirect(url_for('home'))
    
    pilot_requests = PilotRequest.query.filter_by(status='pending').all()
    item_requests = ItemRequest.query.filter_by(status='pending').all()

    if request.method == 'POST':
        request_id = request.form.get('request_id')
        action = request.form.get('action')
        request_type = request.form.get('request_type')  # Distinguish between pilot and item requests
        if request_type =='pilot':
            pilot_request = PilotRequest.query.get(request_id)
            if pilot_request and action in ['approve', 'reject']:
                if action == 'approve':
                    if pilot_request.action == 'create':
                        new_pilot = User(username = pilot_request.pilot_name, 
                                        email = pilot_request.pilot_email, 
                                        password = pilot_request.pilot_password, 
                                        bank = pilot_request.pilot_bank, 
                                        role = 'pilot', 
                                        team = pilot_request.pilot_team)
                        db.session.add(new_pilot)
                        db.session.commit()
                    elif pilot_request.action == 'edit':
                        pilot = User.query.filter_by(id = pilot_request.pilot_id).first()
                        
                        if pilot:
                            if pilot.username != pilot_request.pilot_name:
                                pilot.username = pilot_request.pilot_name
                            if pilot.email != pilot_request.pilot_email:
                                pilot.email = pilot_request.pilot_email
                            db.session.commit()
                        else:
                            flash('Pilot not found for editing.', 'danger')
                    flash('Request approved!', 'success')
                elif action == 'reject':
                    flash('Request rejected', 'warning')
                
                pilot_request.status = action
                db.session.commit()
        elif request_type == 'item':
            item_request = ItemRequest.query.get(request_id)
            if item_request and action in ['approve', 'reject']:
                if action == 'approve':
                    if item_request.action == 'create':
                        new_item = Item(
                            name=item_request.item_name,
                            price=item_request.item_price,
                            image_file=item_request.item_image_file,
                            owner_id=item_request.owner_id,
                        )
                        db.session.add(new_item)
                    elif item_request.action == 'edit':
                        item = Item.query.filter_by(id = item_request.item_id).first()
                        if item:
                            item.price = item_request.item_price
                            item.image_file = item_request.item_image_file
                        else:
                            flash('Item not found for editing.', 'danger')
                    elif item_request.action == 'delete':
                        item = Item.query.filter_by(id = pilot_request.pilot_id).first()
                        if item:
                            db.session.delete(item)
                        else:
                            flash('Item not found for deletion.', 'danger')
                    flash('Request approved!', 'success')
                elif action == 'reject':
                    flash('Item request rejected.', 'warning')

                item_request.status = action
                db.session.commit()


        return redirect(url_for('requests'))
    
    return render_template('requests.html', title= 'Requests', requests = pilot_requests, item_requests = item_requests)

                

@app.route("/store", methods=['GET'])
def store():
    owner_name = request.args.get('owner_name')  # Get the filter query parameter
    if owner_name:
        # Filter items by owner's username
        items = Item.query.join(User).filter(User.username.ilike(f"%{owner_name}%")).all()
    else:
        # Get all items
        items = Item.query.all()
    
    return render_template('store.html', title='Store', items=items)

@app.route("/buy_item/<int:item_id>", methods=['POST'])
@login_required
def buy_item(item_id):
    item = Item.query.get_or_404(item_id)
    
    if current_user.bank < item.price:
        flash('Insufficient funds to purchase this item.', 'danger')
        return redirect(url_for('store'))
    
    # Deduct item price from user's bank
    current_user.bank -= item.price
    db.session.commit()
    
    flash(f'You have purchased {item.name}!', 'success')
    return redirect(url_for('store'))

