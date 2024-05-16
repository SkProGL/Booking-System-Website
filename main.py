import json

from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
from DatabaseHandler import DatabaseHandler
from validation import validation
from flask_mail import Mail, Message
from datetime import datetime
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# Test users in database
# 'Jardani', 'Jovonov', 'jonathanJ@outlook.com', 'Jardani1', 'thisIsDaisy', '+37125509477'
# 'Liam', 'Morgan', 'liamMorgann@gmail.com', 'liamM1', 'realPass1', '+7125509477'
# admin - 'Alex', 'Jones', 'newAcc1',  'lxyz2Akl','a123personal@gmail.com',


# password encryption
# https://github.com/CoreyMSchafer/code_snippets/blob/master/Python/Flask_Blog/06-Login-Auth/flaskblog/routes.py#L41
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'
app.permanent_session_lifetime = timedelta(days=30)

# setting up automated email service for password recovery
# Corey Schafer
# https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog/10-Password-Reset-Email/flaskblog
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'MAIL'
app.config['MAIL_PASSWORD'] = 'MAIL_PASSWORD'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

bcrypt = Bcrypt(app)
mail = Mail(app)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login', error='Please register/login first!'))

    return wrap


def user_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user-type' in session and 'client' in session['user-type']:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login', error='Please login first!'))

    return wrap


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user-type' in session and 'admin' in session['user-type']:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login', error='Please login first!'))

    return wrap


@app.route("/", methods=['GET', 'POST'])
@app.route("/home/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'username' in session:
            form = request.form.to_dict()
            # print(form)
            if 'separate' in form['type'] and 'Room1' not in form:
                return redirect(url_for('home'))
            # login required decorator was not added
            # to make website navigation more flexible and allow user to look at city options before making any bookings
            if 'user-type' in session and 'admin' in session['user-type']:
                return redirect(url_for('home', error='Admin cannot make bookings!'))
            username = session['username']
            client_id = DatabaseHandler().data_modifier.read('client', f'username="{username}"', 'ClientID')[0][0]
            booking_id = DatabaseHandler().create_booking(datetime.today().strftime('%Y-%m-%d'), form['checkIn'],
                                                          form['checkOut'], 'Pending', 0, 0, client_id)

            rooms = {}
            # booking = json.loads(str(request.args.get('booking')).replace("'", "\""))
            client_id = DatabaseHandler().data_modifier.read('client', f'username="{username}"', 'ClientID')[0][0]
            count = 1

            # check if only one room is booked
            # https://stackoverflow.com/questions/6531482/how-to-check-if-a-string-contains-an-element-from-a-list-in-python
            if form['type'].endswith(('standard', 'double', 'family')):
                rooms = {'Room1': {'type': form['type']}}
                DatabaseHandler().create_room(count, form['type'], 'no', 'no', 'no', 'no', 1, booking_id, client_id)

            else:
                count = 1
                for i in range(1, int(form['count']) + 1):
                    rooms['Room' + str(i)] = {'type': form['Room' + str(i)]}
                    # print(form['Room' + str(i)])
                    DatabaseHandler().create_room(count, str(form['Room' + str(i)]), 'no', 'no', 'no', 'no', 1,
                                                  booking_id, client_id)
                    count += 1

            price = validation().calculate_pricing(username, booking_id)['Total']
            DatabaseHandler().data_modifier.update('booking', {'Cost': price}, 'BookingID = ' + str(booking_id))
            return redirect(url_for('checkout', booking=form, booking_id=booking_id, rooms=rooms, price=price))
        else:
            return redirect(url_for('login', error='Please register/login first!'))

    else:
        cities = DatabaseHandler().data_modifier.read('hotel', column='City')

        return render_template('index.html', title='Home',
                               navigation='nav-booking', message=request.args.get('message'),
                               success=request.args.get('success'),
                               error=request.args.get('error'), cities=cities)


@app.route("/checkout/<booking_id>", methods=['GET', 'POST'])
@user_required
def checkout(booking_id):
    if request.method == 'POST':
        print('request.form.to_dict')
        form = request.form.to_dict()
        for i in form.keys():
            num = i.split('_')[0]
            DatabaseHandler().data_modifier.update('room',
                                                   {'Internet': 'No', 'TV': 'No', 'MiniBar': 'No', 'Breakfast': 'No'},
                                                   f'RoomNumber = "{num}" AND booking_BookingID = "{booking_id}"')
        for i in form.keys():
            num = i.split('_')[0]
            type = i.split('_')[1]
            DatabaseHandler().data_modifier.update('room', {type: 'Yes'},
                                                   f'RoomNumber = "{num}" AND booking_BookingID = "{booking_id}"')
            # Internet, TV, MiniBar, Breakfast,
        DatabaseHandler().data_modifier.update('booking', {'Status': 'Paid'}, 'BookingID = ' + str(booking_id))

        return redirect(url_for('generate_invoice', booking=booking_id, _external=True))
    else:
        rooms = {}
        booking = json.loads(str(request.args.get('booking')).replace("'", "\""))

        if booking['type'].endswith(('standard', 'double', 'family')):
            rooms = {'Room1': {'type': booking['type']}}
        else:
            count = 1
            for i in range(1, int(booking['count']) + 1):
                rooms['Room' + str(i)] = {'type': booking['Room' + str(i)]}
                count += 1

        city = booking['city']
        city = DatabaseHandler().data_modifier.read_as_dict('hotel', f'City="{city}"')[0]['Name']

        price = request.args.get('price')
        return render_template('confirmation-page.html', title='confirmation', hotelName=city, rooms=rooms,
                               price=price)


@app.route("/register/", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        authorized = validation().validate_registration(request.form)
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

        if authorized[0]:
            DatabaseHandler().create_client(name, surname, email, username, hashed_pw, phone)
            session.permanent = True
            session["username"] = username
            session["user-type"] = 'client'
            return redirect(url_for('home', success=f'Successfully registered!'))
        return redirect(url_for('register', error=f'Data did not pass server validation. {authorized[1]}.'))
    else:
        return render_template('register.html', title='Register', navigation='nav-register',
                               message=request.args.get('message'), success=request.args.get('success'),
                               error=request.args.get('error'))


@user_required
@app.route("/generate_invoice/<booking>/", methods=['GET'])
def generate_invoice(booking):
    username = session['username']
    db_client = DatabaseHandler().data_modifier.read_as_dict('client', f'username="{username}"')[0]
    client_id = db_client['ClientID']
    db_booking = \
        DatabaseHandler().data_modifier.read_as_dict('booking',
                                                     f'client_ClientID="{client_id}" AND BookingID="{booking}"')[
            0]
    booking_id = db_booking['BookingID']
    db_rooms = DatabaseHandler().data_modifier.read_as_dict('room', f'booking_BookingID="{booking_id}"')
    # room_id = db_rooms[0]['RoomID']
    hotel_id = db_rooms[0]['hotel_HotelID']
    db_hotel = DatabaseHandler().data_modifier.read_as_dict('hotel', f'HotelID="{hotel_id}"')
    receipt = validation().calculate_pricing(db_client['Username'], booking_id)

    return render_template('invoice.html', title='Invoice', client=db_client, booking=db_booking, rooms=db_rooms,
                           hotel=db_hotel, receipt=receipt)


@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # if 'user' in session:
        #     print(session['username'])
        authorized = validation().validate_login(request.form)
        username = request.form['username']
        if authorized[0] and DatabaseHandler().field_exists(request.form['username'], request.form['user-type']):
            retrieved = DatabaseHandler().data_modifier.read(request.form['user-type'], f'username="{username}"',
                                                             'password')[0][0]
            if bcrypt.check_password_hash(retrieved, request.form['password']):
                session.permanent = True
                session["username"] = request.form['username']
                session["user-type"] = request.form['user-type']
                return redirect(url_for('home', message="Successfully logged in!"))
        return redirect(url_for('login',
                                error="Login failed: Please check whether username or password is correct"))
    else:
        return render_template('login.html', title='Login', navigation='nav-login', message=request.args.get('message'),
                               success=request.args.get('success'), error=request.args.get('error'))


@app.route("/account/", methods=['GET', 'POST'])
@login_required
def account():
    username = session['username']
    client_id = DatabaseHandler().data_modifier.read('client', f'username="{username}"')[0][0]
    if request.method == 'POST':
        form = request.form.to_dict()
        if 'update' in form['action']:
            try:
                booking_id = form['BookingID']
                changes = {'BookingCreationDate': datetime.today().strftime('%Y-%m-%d'),
                           'CheckInDate': form['CheckInDate'], 'CheckOutDate': form['CheckOutDate']}
                DatabaseHandler().data_modifier.update('booking', changes,
                                                       f'BookingID={booking_id} AND client_ClientID="{client_id}"')
                cost = validation().calculate_pricing(username, booking_id)['Total']
                DatabaseHandler().data_modifier.update('booking', {"Cost": cost},
                                                       f'BookingID={booking_id} AND client_ClientID="{client_id}"')
                return redirect(url_for('generate_invoice', booking=booking_id, _external=True))
            except Exception as e:
                return redirect(
                    url_for(f'account', error="Exception, sent data may be corrupted. \n" + str(e)))
        elif 'delete' in form['action']:
            try:
                booking_id = form['BookingID']

                today = datetime.today().strftime('%Y-%m-%d')
                date1 = datetime.strptime(today, '%Y-%m-%d')
                date2 = datetime.strptime(form['CheckInDate'], '%Y-%m-%d')
                difference = (date2 - date1).days
                fee = 0
                if difference > 59:
                    fee = 0
                elif 30 < difference < 60:
                    fee = 0.5
                elif difference < 30:
                    fee = 1
                cost = form['Cost']
                cancellation_fee=int(fee) * float(cost)
                changes = {'Status': 'Cancelled',
                           'CancellationFee': cancellation_fee}
                DatabaseHandler().data_modifier.update('booking', changes,
                                                       f'BookingID={booking_id} AND client_ClientID="{client_id}"')
                return redirect(
                    url_for('account',
                            message=f'Booking cancelled, fee of {fee * 100}% will be deducted from your account - {cancellation_fee}£'))
            except Exception as e:
                return redirect(
                    url_for(f'account', error="Exception, sent data may be corrupted. \n" + str(e)))
    else:
        booking = DatabaseHandler().data_modifier.read('booking',
                                                       f'client_ClientID="{client_id}" AND Status="Pending" OR Status="Paid"')

        bookings_header = DatabaseHandler().data_modifier.features('booking', 'columns')

        return render_template('account.html', title='Account', navigation='nav-account', booking=booking,
                               headers=bookings_header, message=request.args.get('message'),
                               error=request.args.get('error'))


@app.route("/logout/")
@login_required
def logout():
    session.clear()
    return redirect(url_for('login', message='Logged out!'))


@app.route("/about/")
def about():
    # raise ValidationError("Don't do that")
    return render_template('about.html', title='About', navigation='nav-about')


# reset password feature
# https://www.youtube.com/watch?v=vutyTx7IaAI&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=13
@app.route("/reset-password/", methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        # print(request.form)
        email = request.form['email']
        client_id = DatabaseHandler().data_modifier.read('client', f'email="{email}"')[0][0]
        # add Admin handle
        if client_id:
            # sendMessage()
            token = get_reset_token(client_id)
            msg = Message('WH - Password reset', sender="noreply@demo.com", recipients=[str(email)])
            msg.body = f'''To reset WH password, please visit the following link
            {url_for('reset_password_with_token', token=token, _external=True)}
            If you did not make this request please ignore this email'''
            mail.send(msg)
        return redirect(url_for('login', message='Email has been sent!'))
    else:
        return render_template('reset-password.html', title='Password recovery', error=request.args.get('error'))


@app.route("/reset-password/<token>", methods=['GET', 'POST'])
def reset_password_with_token(token):
    if request.method == 'POST':
        if 'password' in request.form:
            password = request.form['password']
            hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
            DatabaseHandler().data_modifier.update('client', {'password': hashed_pw},
                                                   'clientId=' + str(verify_reset_token(token)))

            return redirect(url_for('login', success='Password successfully changed!'))
        return redirect(url_for('home', error='Server could not process data!'))

    if verify_reset_token(token) is None:
        return redirect(url_for('reset_password', error='This is an invalid or expired token'))

    return render_template('reset-password.html', validation=True)


@admin_required
@app.route("/admin/<table_name>", methods=['GET', 'POST'])
def admin(table_name):
    if request.method == 'POST':
        form = request.form.to_dict()
        first_column = DatabaseHandler().data_modifier.features(table_name, 'columns')[0]

        # remove extra information from form dictionary
        # for database update to work
        if form['action'] == 'update':
            try:
                statement = f'{first_column} = {form[str(first_column)]}'
                form.pop('table')
                form.pop('action')
                form.pop(str(first_column))
                DatabaseHandler().data_modifier.update(table_name, form, statement)
                return redirect(url_for(f'admin', table_name=table_name))
            except Exception as e:
                return redirect(
                    url_for(f'admin', table_name=table_name, error="Exception, possibly wrong data type. \n" + str(e)))
        elif form['action'] == 'delete':
            try:
                DatabaseHandler().data_modifier.delete(table_name, f'{first_column} = {form[str(first_column)]}')
                return redirect(url_for(f'admin', table_name=table_name))
            except Exception as e:
                return redirect(
                    url_for(f'admin', table_name=table_name, error="Exception, possibly wrong id. \n" + str(e)))
        elif form['action'] == 'create':
            try:
                form.pop('table')
                form.pop('action')
                form.pop(str(first_column))
                DatabaseHandler().data_modifier.create(table_name, form)
                return redirect(url_for(f'admin', table_name=table_name))
            except Exception as e:
                return redirect(
                    url_for(f'admin', table_name=table_name, error="Exception, possibly wrong data type. \n" + str(e)))


    else:
        db = DatabaseHandler()
        db.get_table_names()
        table = table_name
        clients = db.data_modifier.read(table)
        clients_header = db.data_modifier.features(table, 'columns')

        return render_template('admin.html', title='Admin', navigation='nav-admin', table=clients,
                               headers=clients_header,
                               table_name=table_name, message=request.args.get('message'),
                               error=request.args.get('error'))


@app.route("/enable-js/")
def enable_js():
    return render_template('enable-js.html')


def get_reset_token(client_id):
    s = Serializer(app.config['SECRET_KEY'], 1800)
    return s.dumps({'clientID': client_id}).decode('utf-8')


def verify_reset_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        client_id = s.loads(token)['clientID']
    except:
        return None
    return client_id


if __name__ == "__main__":
    app.run(debug=True)
