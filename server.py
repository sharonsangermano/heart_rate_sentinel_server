from pymodm import connect, MongoModel, fields
from datetime import datetime
from flask import Flask, jsonify, request
from validate_email import validate_email
import sendgrid
import os
from sendgrid.helpers.mail import *
connect("mongodb://user1:1cooluser@ds155653.mlab.com:55653/ses137_hrss")
app = Flask(__name__)


class User(MongoModel):
    patient_id = fields.IntegerField(primary_key=True)
    attending_email = fields.EmailField()
    user_age = fields.IntegerField()
    heart_rate = fields.ListField()
    rec_time = fields.ListField()


def add_user(pid_arg, email_arg, age_arg):
    u1 = User(pid_arg, email_arg, age_arg, [None], [None])
    u1.save()


def add_hr(pid_arg, hr_arg, time_arg):
    u2 = User.objects.raw({"_id": pid_arg}).first()
    if u2.heart_rate[0] is None:
        u2.heart_rate[0] = hr_arg
        u2.rec_time[0] = time_arg
    else:
        u2.heart_rate.append(hr_arg)
        u2.rec_time.append(time_arg)
    u2.save()


def get_age(pid_arg):
    u3 = User.objects.raw({"_id": pid_arg}).first()
    return u3.user_age


def get_recent_hr(pid_arg):
    u4 = User.objects.raw({"_id": pid_arg}).first()
    return u4.heart_rate[-1]


def get_hrs(pid_arg):
    u5 = User.objects.raw({"_id": pid_arg}).first()
    return u5.heart_rate


def get_avg_hr(hr_list):
    sum_hr = 0
    if len(hr_list) is 0:
        return 'No heart rates recorded'
    else:
        for x in hr_list:
            sum_hr = sum_hr + x
        avg_hr = sum_hr/len(hr_list)
        return avg_hr


def get_int_ave(times_arg, hrs_arg, int_arg):
    int_times, int_hr = [], []
    x = 0
    time_comp = datetime.strptime(int_arg, '%Y-%m-%d %H:%M:%S.%f')
    while x < len(times_arg):
        if times_arg[x] >= time_comp:
            int_times.append(times_arg[x])
            int_hr.append(hrs_arg[x])
        x += 1
    if len(int_hr) is 0:
        return 'No heart rates recorded during that time interval'
    else:
        return get_avg_hr(int_hr)


def is_tachy(age, hr):
    tachy = False
    if age < 1:
        return'Patient is too young to detect tachycardia ' \
              'with this program'
    elif age >= 1 and age <= 2 and hr >= 151:
        tachy = True
    elif age >= 3 and age <= 4 and hr >= 137:
        tachy = True
    elif age >= 5 and age <= 7 and hr >= 133:
        tachy = True
    elif age > 8 and age <= 11 and hr >= 130:
        tachy = True
    elif age >= 12 and age <= 15 and hr >= 119:
        tachy = True
    elif age >= 15 and hr >= 100:
        tachy = True
    if tachy:
        return 'Tachycardic'
    else:
        return 'Non-Tachycardic'


def validate_newp_req(req):
    try:
        int(req["patient_id"])
    except ValueError:
        print('patient_id must be an integer.  Please try again.')
        return False
    try:
        if validate_email(req["attending_email"]) is False:
            raise ValueError
    except ValueError:
        print('attending_email must be a valid email address. '
              'Please try again.')
        return False
    try:
        int(req["user_age"])
    except ValueError:
        print('user_age must be an integer. Please try again.')
        return False
    return True


def validate_hr_req(req):
    try:
        int(req["patient_id"])
    except ValueError:
        print('patient_id must be an integer. Please try again')
        return False
    try:
        int(req["heart_rate"])
    except ValueError:
        print('heart_rate must be an integer. Please try again')
        return False
    return True


def alert_dr(alert_email, pid):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("sharon.sangermano@duke.edu")
    to_email = Email(alert_email)
    subject = "Sending with SendGrid is Fun"
    content = Content("text/plain", "Your patient, with patient_id: " +
                      str(pid) + " has a heart rate registering as "
                                 "tachycardic.")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
    return 'email sent'


@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    r = request.get_json()
    if validate_newp_req(r):
        pid = r["patient_id"]
        a_email = r["attending_email"]
        age = r["user_age"]
        try:
            User.objects.raw({"_id": pid}).first()
            return jsonify('Patient_id is already used.  Please try again'
                           ' with a new id.')
        except:
            add_user(pid, a_email, age)
            return jsonify(pid, a_email, age)


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate():
    r = request.get_json()
    if validate_hr_req(r):
        pid = r["patient_id"]
        hr = r["heart_rate"]
        time = datetime.now()
        try:
            add_hr(pid, hr, time)
            print('added hr')
            return jsonify(pid, hr)
        except:
            return jsonify('Patient with patient_id could not be found.  '
                           'Please try again.')


@app.route("/api/status/<patient_id>", methods=["GET"])
def get_status(patient_id):
    pid = int(patient_id)
    try:
        age = get_age(pid)
        hr = get_recent_hr(pid)
        tachy = is_tachy(age, hr)
        if tachy == 'Tachycardic':
            u6 = User.objects.raw({"_id": pid}).first()
            a_email = u6.attending_email
            alert_dr(a_email, pid)
        return jsonify(tachy)
# RETURN MOST RECENT TIME STAMP
    except:
        return jsonify('Patient with patient_id could not be found.  '
                       'Please try again.')


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def get_hr(patient_id):
    pid = int(patient_id)
    try:
        hr_list = get_hrs(pid)
        return jsonify(hr_list)
    except:
        return jsonify('Patient with patient_id could not be found.  '
                       'Please try again.')


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def get_average(patient_id):
    pid = int(patient_id)
    try:
        hr_list = get_hrs(pid)
        avg_hr = get_avg_hr(hr_list)
        return jsonify(avg_hr)
    except:
        return jsonify('Patient with patient_id could not be found.  '
                       'Please try again.')


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def get_int_average():
    r = request.get_json()
    pid = r["patient_id"]
    interval = r["heart_rate_average_since"]
    try:
        u6 = User.objects.raw({"_id": pid}).first()
        times = u6.rec_time
        hrs = u6.heart_rate
        int_ave = get_int_ave(times, hrs, interval)
        return jsonify(int_ave)
    except:
        return jsonify('Patient with patient_id could not be found.  '
                       'Please try again.')
