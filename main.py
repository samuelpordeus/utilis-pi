import csv
import RPi.GPIO as GPIO
import os
from flask import Flask, url_for, render_template, request, flash, session, redirect
import flask_login

app = Flask(__name__, static_url_path='')
app.secret_key = '08001230800'

# LOGIN

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
users = {'samuelspordeus@gmail.com': {'pw': '123456'}}


class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    user.is_authenticated = request.form['pw'] == users[email]['pw']

    return user


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))
###


pins = {}

GPIO.setmode(GPIO.BOARD)

with open('pins.csv') as csv_file:
    pins_list = csv.reader(csv_file)
    pins_list = list(pins_list)
    for pin in pins_list:
        if pin[2] == 'GPIO.LOW':
            pin[2] = GPIO.LOW
        else:
            pin[2] = GPIO.HIGH
        pins[int(pin[0])] = {'name': pin[1], 'state': pin[2]}

for pin in pins:
    pass
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# VIEWS


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    if request.form['pw'] == users[email]['pw']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('main'))

    return 'Bad login'

@app.route('/powertv')
def powertv():
    os.system("irsend SEND_ONCE samsungTV KEY_POWER")
    return redirect(url_for('main'))

@app.route('/channelup')
def powertv():
    os.system("irsend SEND_ONCE samsungTV KEY_CHANNELUP")
    return redirect(url_for('main'))

@app.route('/volumeup')
def powertv():
    os.system("irsend SEND_ONCE samsungTV KEY_VOLUMELUP")
    return redirect(url_for('main'))

@app.route('/channeldown')
def powertv():
    os.system("irsend SEND_ONCE samsungTV KEY_CHANNELDOWN")
    return redirect(url_for('main'))

@app.route('/volumedown')
def powertv():
    os.system("irsend SEND_ONCE samsungTV KEY_VOLUMEDOWN")
    return redirect(url_for('main'))


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@app.route('/')
@app.route("/index")
@flask_login.login_required
def main():
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
    templateData = {
        'pins': pins
    }
    return render_template('index.html', **templateData)


@app.route("/api/<change_pin>/<action>")
@flask_login.login_required
def action(change_pin, action):
    change_pin = int(change_pin)
    deviceName = pins[change_pin]['name']
    if action == "on":
        GPIO.output(change_pin, GPIO.HIGH)
        print("Turned " + deviceName + " on")
    if action == "off":
        GPIO.output(change_pin, GPIO.LOW)
        print("Turned " + deviceName + " off")

    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)

    templateData = {
        'pins': pins
    }

    return render_template('index.html', **templateData)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
