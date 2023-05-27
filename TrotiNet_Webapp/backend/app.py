import os
import sqlite3
import secrets
import json
from PIL import Image
from flask import Flask, render_template, url_for, redirect, flash, request, jsonify
from forms import RegistrationForm, LoginForm, UpdateAccountForm, UpdatePersonalForm, UpdateProfilePic, UpdatePasswordForm 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_login import UserMixin
from datetime import timedelta, datetime

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.db")

app = Flask(__name__)
app.config['SECRET_KEY'] = '-Ch7jTIxW5coGf4EK2rvc15mweeFZQRPLJZX80tNh8g'
app.config['REMEMBER_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_SAMESITE'] = 'Lax'

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


class User(UserMixin):
    ...


@login_manager.user_loader
def load_user(email):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username,email,image_file,first_name,last_name,birth_date,phone_number FROM users WHERE email = ? ", [email])
        query_result = cursor.fetchone()
        if not query_result:
            return
        user = User()
        user.id = query_result[1]  # Mandatory field
        user.username = query_result[0]
        user.email = query_result[1]
        user.imagefile = query_result[2]
        user.firstname = query_result[3]
        user.lastname = query_result[4]
        user.birthdate = query_result[5]
        user.phonenumber = query_result[6]
    return user


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + file_ext
    picture_path = os.path.join(
        app.root_path, 'static/img/profileImage', picture_fn)

    # get the original width and height of the image
    image = Image.open(form_picture)
    original_width, original_height = image.size

    # calculate the aspect ratio of the image
    aspect_ratio = original_width / original_height

    # set the new height to 512, and calculate the new width based on the aspect ratio
    new_height = 512
    new_width = round(new_height * aspect_ratio)

    # resize the image using the calculated width and height
    resized_image = image.resize((new_width, new_height))

    # create a new blank image with a size of 512x512
    new_image = Image.new("RGB", (512, 512))

    # calculate the coordinates to paste the resized image onto the new image
    x_offset = round((512 - new_width) / 2)
    y_offset = round((512 - new_height) / 2)

    # paste the resized image onto the new image
    new_image.paste(resized_image, (x_offset, y_offset))
    new_image.save(picture_path)

    return picture_fn


def db_store_image(img_name):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        # Remove old image from filesystem
        cursor.execute(
            "SELECT image_file FROM users WHERE username=?", [current_user.username])
        old_img = cursor.fetchone()
        filename = os.path.basename(old_img[0])
        if filename != "default.jpg":
            old_img_path = os.path.join(os.path.dirname(
                os.path.abspath(__file__)), 'static', 'img', 'profileImage', filename)
            try:
                os.remove(old_img_path)
                print(f"Successfully removed {old_img_path}")
            except FileNotFoundError:
                print(f"{old_img_path} doesn't exist.")

        img_path = url_for('static', filename='img/profileImage/' + img_name)
        cursor.execute("UPDATE users SET image_file=? WHERE username=?", [
                       img_path, current_user.username])


def check_profilepic() -> str:
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT image_file FROM users WHERE username=? ", [current_user.username])

        file_path = cursor.fetchone()

        if os.path.exists(str(app.root_path) + str(file_path[0])):
            return file_path[0]
        else:
            return "/static/img/profileImage/default.jpg"


@ app.route("/get_user_id",  methods=['GET'])
@ login_required
def get_user_id():
    return jsonify({'userId' : current_user.username})


@ app.route("/get_user_img_path",  methods=['GET'])
@ login_required
def get_user_img_path():
    return jsonify({'img_path' : check_profilepic()})


@app.route('/get_messages', methods=['GET'])
def get_messages():
    all_messages = []
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT sender,receiver,message,date FROM chat WHERE sender=? AND receiver=? OR sender=? AND receiver=?",
                       [current_user.username, "admin", "admin", current_user.username])
        messages = cursor.fetchall()

        for message in messages:
            all_messages.append({
                "sender": message[0],
                "receiver": message[1],
                "message": message[2],
                "date": message[3]
            })
    return jsonify(messages = all_messages) 


@ app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            with sqlite3.connect(DB) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT username,email FROM users WHERE username = ? OR email = ?", [form.username.data, form.email.data])
                query_result = cursor.fetchone()

                if not query_result:
                    hashed_passsword = bcrypt.generate_password_hash(
                        form.password.data).decode('utf-8')
                    image_file = url_for(
                        'static', filename='img/profileImage/default.jpg')
                    cursor.execute("INSERT INTO users(username, email, password, image_file) VALUES (?,?,?,?)", [
                        form.username.data, form.email.data, hashed_passsword, image_file])
                    flash('Your account has been created {}!'.format(
                        form.username.data), "success")
                    return redirect(url_for('login'))
                else:
                    flash('Username or email already in use', 'warning')
                    return redirect(url_for('register'))

    return render_template('register.html', title='Register', form=form)


@ app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = load_user(form.email.data)
            with sqlite3.connect(DB) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT email,password FROM users WHERE email= ?", [
                    form.email.data])
                query_result = cursor.fetchone()
                if not query_result:
                    flash("User not registered", 'warning')
                    return redirect(url_for('login'))
                if bcrypt.check_password_hash(query_result[1], form.password.data) and form.email.data == query_result[0]:
                    login_user(user, remember=form.remember.data,
                               duration=timedelta(minutes=30), force=False, fresh=True)
                    return redirect(url_for('trip'))
                else:
                    flash(
                        'Login Unsuccessful. Please check email and password!', 'danger')
                    return redirect(url_for('login'))

    return render_template('login.html', title='Login', form=form)


@ app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    Accountform = UpdateAccountForm()
    Personalform = UpdatePersonalForm()
    ProfilePicform = UpdateProfilePic()
    Passwordform = UpdatePasswordForm()

    if request.method == 'POST':
        if Personalform.validate_on_submit():
            with sqlite3.connect(DB) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT first_name,last_name,birth_date,phone_number FROM users WHERE username=?", [current_user.username])
                query_result = cursor.fetchone()
                if Personalform.firstname.data != query_result[0] or Personalform.lastname.data != query_result[1] or str(Personalform.birthdate.data) != str(query_result[2]) or Personalform.phonenumber.data != query_result[3]:
                    cursor.execute("UPDATE users SET first_name= ?, last_name= ?, birth_date = ?, phone_number = ? WHERE username= ?", [
                        Personalform.firstname.data, Personalform.lastname.data, Personalform.birthdate.data, Personalform.phonenumber.data, current_user.username])
                    flash("Your account has been updated !", 'success')
                    return redirect(url_for('account'))
                else:
                    return redirect(url_for('account'))

        if Accountform.validate_on_submit():
            with sqlite3.connect(DB) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT email,username FROM users WHERE email=? OR username=?", [
                    Accountform.email.data, Accountform.username.data])
                UniqueUser = cursor.fetchall()
                if len(UniqueUser) == 1 and (str(Accountform.email.data) != str(UniqueUser[0][0]) or Accountform.username.data != UniqueUser[0][1]):
                    cursor.execute("UPDATE users SET username = ?, email = ? WHERE username= ?", [
                        Accountform.username.data, Accountform.email.data, current_user.username])
                    logout_user()
                    return redirect(url_for('login'))
                else:
                    flash("Username or email already in use!", 'warning')
                    return redirect(url_for('account'))

        if ProfilePicform.validate_on_submit():
            if ProfilePicform.picture.data:
                img = save_picture(ProfilePicform.picture.data)
                db_store_image(img)
                flash("Profile picture updated!", 'success')
                return redirect(url_for('account'))

        if Passwordform.validate_on_submit():
            with sqlite3.connect(DB) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT password FROM users WHERE username=?", [
                               current_user.username])
                query_result = cursor.fetchone()
                if bcrypt.check_password_hash(query_result[0], Passwordform.currentpassword.data):
                    cursor.execute('UPDATE users SET password=? WHERE username=?', [bcrypt.generate_password_hash(
                        Passwordform.newpassword.data).decode('utf-8'), current_user.username])
                    flash("Password has been changed!", 'success')
                    return redirect(url_for('account'))
                else:
                    flash("Current password not matched!", "warning")
     
    img_path = check_profilepic()

    return render_template('account.html', title='Account', personalform=Personalform, accountform=Accountform, picform=ProfilePicform, passwordform=Passwordform, imgPath = img_path)


## THIS IS A DUMMY IMPLEMENTATION OF A CHAT BETWEEN ADMIN AND USER

@ app.route("/chat/admin", methods=['GET', 'POST'])
def chat_admin():
    if request.method == 'POST':
        data = request.get_json()
        message = data.get("message")
        receiver = data.get("receiver")
        dateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(message)
        print(receiver)
        with sqlite3.connect(DB) as conn:
            cursor = conn.cursor()
            if receiver != 'admin':
                cursor.execute(
                    "INSERT INTO chat(sender, receiver, date, message) VALUES(?,?,?,?)",["admin", receiver, dateTime, message])
            return redirect(url_for('chat_admin'))

    js_file = url_for('static', filename='js/admin.js')
    return render_template('admin.html', title='Admin Chat', js_file=js_file)


@ app.route("/chat", methods=['GET', 'POST'])
@login_required
def chat():
    if request.method == 'POST':
        data = request.get_json()
        message = data.get("message")
        sender = data.get("sender")
        dateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with sqlite3.connect(DB) as conn:
            cursor = conn.cursor()
            if sender != 'admin':
                cursor.execute(
                    "INSERT INTO chat(sender, receiver, date, message) VALUES(?,?,?,?)",[sender, "admin", dateTime, message])
            print("massage")
            return redirect(url_for('chat'))

   

    img_path = check_profilepic()

    js_file = url_for('static', filename='js/chat.js')

    return render_template('chat.html', title='Chat', imgPath = img_path, js_file=js_file)

#####################################################################################


@ app.route("/trip/view", methods=['GET', 'POST'])
@login_required
def view():
    js_file = url_for('static', filename='js/view.js')
    return render_template('view.html', title='View', js_file = js_file)


@app.route("/trip/checkout", methods=['GET', 'POST'])
@login_required
def checkout(): 
    return render_template('checkout.html', title=' Checkout')


@ app.route("/trip", methods=['GET', 'POST'])
@login_required
def trip():
    js_file = url_for('static', filename='js/popup.js')
    return render_template('home.html', title='Trip', js_file = js_file)


@ app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('trip'))
    return render_template('start.html', title='Start')

@ app.route("/history", methods=['GET', 'POST'])
@login_required
def history():
    return render_template('history.html', title='History')


@ app.route("/book", methods=['GET', 'POST'])
@login_required
def book(): 
    js_file = url_for('static', filename='js/book.js')
    return render_template('book.html', title='Book Scooter', js_file = js_file)


@ app.route("/book/custom", methods=['GET', 'POST'])
@login_required
def customBook(): 
    js_file = url_for('static', filename='js/custombook.js')
    return render_template('custombook.html', title='Book Scooter', js_file = js_file)


@ app.route("/book/checkout", methods=['GET', 'POST'])
@login_required
def bookCheckout(): 
    return render_template('bookCheckout.html', title='Book Scooter')

@ app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)
