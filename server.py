from pymodm import connect, MongoModel, fields
from datetime import datetime
from flask import Flask, jsonify, request
connect("mongodb://user1:1cooluser@ds155653.mlab.com:55653/ses137bme590")
app = Flask(__name__)


class User(MongoModel):
    patient_id = fields.IntegerField()
    attending_email = fields.EmailField(primary_key=True)
    user_age = fields.IntegerField()
    #hr = fields.ListField(fields=fields.IntegerField())
    hr = fields.ListField()
    #rec_time = fields.ListField(fields=fields.DateTimeField())
    rec_time = fields.ListField()


def add_user(pid_arg, email_arg, age_arg):
    u1 = User(pid_arg, email_arg, age_arg, [None], [None])
    u1.save()


def add_hr(pid_arg, hr_arg, time_arg):
    u2 = User.objects.raw({"patient_id": pid_arg}).first()
    if u2.hr[0] is None:
        u2.hr[0] = hr_arg
        u2.rec_time[0] =time_arg
    else:
        u2.hr.append(hr_arg)
        u2.rec_time.append(time_arg)
    u2.save()


def get_age(pid_arg):
    u3 = User.objects.raw({"patient_id": pid_arg}).first()
    return u3.user_age


def get_recent_hr(pid_arg):
    u4 = User.objects.raw({"patient_id": pid_arg}).first()
    return u4.hr[-1]


def get_hrs(pid_arg):
    u5 = User.objects.raw({"patient_id": pid_arg}).first()
    return u5.hr

def get_avg_hr(pid_arg):
    #u6 = User.objects.raw({"patient_id": pid_arg}).first()
    sum_hr = 0
    cur_hr = get_hrs(pid_arg)
    for x in cur_hr:
        sum_hr = sum_hr + x
    avg_hr = sum_hr/len(cur_hr)
    return avg_hr


# def get_int_ave(pid_arg, int_arg):
#     return "???"
#
#
def is_tachy(age, hr):
    # IF UNDER 1 --> too young throw error/warning
    tachy = False
    if age < 1:
        return'Patient is too young for this program'
    elif age >= 1 and age <= 2 and hr >= 151:
        tachy = True
    elif age >= 2 and age <= 4 and hr >= 137:
        tachy = True
    elif age >= 5 and age <= 7 and hr >= 133:
        tachy = True
    elif age >= 8 and age <= 11 and hr >= 130:
        tachy = True
    elif age >= 12 and age <= 15 and hr >= 119:
        tachy = True
    elif age >= 15 and hr >= 100:
        tachy = True
    if tachy:
        return 'Tachycardic'
    else:
        return 'Non-Tachycardic'



@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    r = request.get_json()
    pid = r["patient_id"]
    email = r["attending_email"]
    age = r["user_age"]
    add_user(pid, email, age)
    print("user added")
    return jsonify(pid, email, age)


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate():
    r = request.get_json()
    pid = r["patient_id"]
    hr = r["hr"]
    time = datetime.now()
    try:
        add_hr(pid, hr, time)
        print('added hr')
        return jsonify(pid, hr)
    except:
        #new_patient(pid, email, age, hr, time)
        print('patient does not exist')
        return jsonify(pid, hr)


@app.route("/api/status/<patient_id>", methods=["GET"])
def get_status(patient_id):
    pid = int(patient_id)
    age = get_age(pid)
    hr = get_recent_hr(pid)
    tachy = is_tachy(age, hr)
    return jsonify(tachy)
# RETURN MOST RECENT TIME STAMP


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def get_hr(patient_id):
    pid = int(patient_id)
    hr_list = get_hrs(pid)
    return jsonify(hr_list)


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def get_average(patient_id):
    pid = int(patient_id)
    avg_hr = get_avg_hr(pid)
    return jsonify(avg_hr)
#
#
# @app.route("/api/heart_rate/interval_average", methods=["POST"])
# def get_int_average():
#     return
