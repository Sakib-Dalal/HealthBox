from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import csv, os, json
import pandas as pd
import plotly.graph_objs as go
import plotly.utils
import numpy as np
# Import your forms from the forms.py


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

# Create Database
class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Configure Flask-Login's Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

# Create a user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

# Create Table in database
class User(UserMixin, db.Model):
    __tablename__ =  "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    device: Mapped[str] = mapped_column(String(250), nullable=True)
    device_API: Mapped[str] = mapped_column(String(250), nullable=True)

with app.app_context():
    db.create_all()

# Home Page
@app.route('/')
def home():
    # # update record
    # s = db.session.execute(db.select(User).where(User.email == 'sakib@gmail.com')).scalar()
    # s.device = None # update value
    # s.device_API = None
    # print("updated value")
    # db.session.commit()
    return render_template('index.html')

# Login Page
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        # Find user by email entered
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Check stored password hash against entered password hashed.
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('userpage'))

    return render_template('login.html')

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, login instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256', salt_length=8)
        new_user = User(
            email = request.form.get('email'),
            password = hash_and_salted_password
        )
        db.session.add(new_user)
        db.session.commit()
        # Log in and authenticate user after adding details to database.
        login_user(new_user)
        # Can redirect() and get name from the current_user
        return redirect(url_for('userpage'))
    return render_template('register.html')

# About Us Page
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

# Features Page
@app.route('/features')
def features():
    return render_template('features.html')

# Users Main Page
@app.route('/userpage')
@login_required
def userpage():
    # print(current_user.email)
    # print(current_user.device)
    # print(current_user.device_API)
    device_list = str(current_user.device).split(',')
    device_api_list = str(current_user.device_API).split(",")
    device_list_length = len(device_list)
    # Passing the name from the current_user
    return render_template('userpage.html', name=current_user.email, device=device_list, device_API=device_api_list, length=device_list_length)

# add new device page
@app.route('/new_device/<email>')
@login_required
def new_device(email):
    return render_template('new_device.html', email=email)

# delete device 
@app.route('/delete_device/<name>/<device_name>/<device_key>')
@login_required
def delete_device(name, device_name, device_key):
    # delete csv file
    path = f"./data/{device_key}.csv"
    os.remove(path)
    # Update data here
    record_to_be_updated = db.session.execute(db.select(User).where(User.email == name)).scalar()
    devices = str(record_to_be_updated.device)
    devices_api = str(record_to_be_updated.device_API)
    # using split to convert string to list
    device_list = devices.split(",")
    device_api_list = devices_api.split(",")
    print(device_name, device_key)
    # delete device name and device key
    device_list.remove(device_name)
    device_api_list.remove(device_key)
    dl = ",".join(device_list)
    da = ",".join(device_api_list)
    # convert to string
    # update record
    record_to_be_updated.device =  dl  # update value
    record_to_be_updated.device_API = da
    print("delete value")
    db.session.commit()
    flash("Please Re-Login to overwrite changes.")
    return redirect(url_for('login'))

# display created api key
@app.route('/display_API/<email>/<device_name>/<API_key>')
@login_required
def display_api(email, device_name, API_key):
    return render_template("display_api.html", email=email, device_name=device_name, API_key=API_key)

# create new device database page
@app.route('/register_new_device/<name>', methods=['GET', 'POST'])
@login_required
def register_new_device(name):
    if request.method == 'POST':
        email = request.form.get('email')
        device_name = request.form.get('device_name')
        api = f"{email}-{device_name}"

        if name == email:
            # generate api_key
            API_key = str(generate_password_hash(api, method='pbkdf2:sha256', salt_length=8))[-15:]
            # create CSV file
            file_path = f"./data/{API_key}.csv"
            with open(file_path, 'w') as csv_file:
                csv_write = csv.writer(csv_file)
                csv_write.writerow(['Time', 'Blood_Pressure', 'ECG', 'Body_Temperature'])
            print("file created")

            # Update data here
            record_to_be_updated = db.session.execute(db.select(User).where(User.email == name)).scalar()
            # print data
            devices = str(record_to_be_updated.device)
            devices_api = str(record_to_be_updated.device_API)
            # using split to convert sting to list
            device_list = devices.split(",")
            device_api_list = devices_api.split(",")
            # appending new device
            device_list.append(device_name)
            device_api_list.append(API_key)
            dl = ",".join(device_list)
            da =  ",".join(device_api_list)
            # convert to string
            # update record
            record_to_be_updated.device =  dl  # update value
            record_to_be_updated.device_API = da
            print("updated value")
            db.session.commit()
            return render_template("display_api.html", email=email, device_name=device_name, API_key=API_key)
        else:
            flash("You entered incorrect email. Please re-login!")
            return redirect(url_for('login'))
    return render_template('index.html')

# data section here
# create plotly graph
@app.route('/graph/<email>/<device_name>/<device_key>')
@login_required
def graph(email, device_name, device_key):
    # read csv file
    file_path = f"./data/{device_key}.csv"
    db = pd.read_csv(file_path)

    index = db.index.to_list()
    labels = db.columns.to_list()
    values = db.mean().to_list()
    time = db.Time.to_list()
    blood_pressure = db.Blood_Pressure.to_list()
    ecg = db.ECG.to_list()
    body_temperature = db.Body_Temperature.to_list()
    
    BloodPressureGraph = {
        'x': time,
        'y': blood_pressure,
        'type': 'scatter',
        'mode': 'lines+markers',
        'marker': {'color': 'red',
                'size': blood_pressure},  # Set the color here
        'name': 'Sample Data',
    }

    BloodPressureBarGraph = {
        'x': time,
        'y': blood_pressure,
        'type': 'bar',
        'marker': {'color': '#F45050'},
        'name': 'Bar Data'
    }

    BodyTemperatureGraph = {
        'x': time,
        'y': body_temperature,
        'type': 'scatter',
        'mode': 'lines+markers',
        'marker': {'color': 'gray',
                'size': body_temperature},  # Set the color here
        'name': 'Sample Data',
    }

    BodyTemperatureBarGraph = {
        'x': time,
        'y': body_temperature,
        'type': 'bar',
        'marker': {'color': 'gray'},
        'name': 'Bar Data'
    }

    # Create some JSON data for pie chart
    MeanPieChart = {
        'title': "Pie Graph",
        #"textinfo": "percent+label",
        'labels': labels,
        'values': values,
        'hole':0.5,
        'type': 'pie',
        'name': 'Pie Data'
    }

    # 3D graph
    #  # Generate random data
    # np.random.seed(1)
    # N = 70

    fig = go.Figure(data=[go.Mesh3d(
        x=time,
        y=blood_pressure,
        z=body_temperature,
        opacity=0.5,
        color='rgba(255, 0, 0, 0.6)'  # Red color with opacity
    )])

    fig.update_layout(
        scene=dict(
            xaxis=dict(nticks=4, range=[-100, 100]),
            yaxis=dict(nticks=4, range=[None, 100]),
            zaxis=dict(nticks=4, range=[-100, None]),
        ),
        width=1200,
        height=900,
        margin=dict(r=20, l=100, b=100, t=10)
    )

    # Create 3D scatter plot
    # fig = go.Figure(data=[go.Scatter3d(
    #     x=time,
    #     y=blood_pressure,
    #     z=ecg,
    #     mode='markers',
    #     marker=dict(
    #         size=12,
    #         color=blood_pressure,                # set color to an array/list of desired values
    #         colorscale='Viridis',   # choose a colorscale
    #         opacity=0.8
    #     )
    # )])

    # # Update layout
    # fig.update_layout(
    #     scene=dict(
    #         xaxis=dict(title='Time'),
    #         yaxis=dict(title='Blood Pressure'),
    #         zaxis=dict(title='ECG'),
    #     ),
    #     margin=dict(l=0, r=0, b=0, t=0),
    # )

   # Example of 3D Line plot
    # fig = go.Figure(data=[go.Scatter3d(
    #     x=time,
    #     y=blood_pressure,
    #     z=ecg,
    #     mode='lines',
    #     line=dict(
    #         color=body_temperature,
    #         width=4
    #     )
    # )])

    # fig.update_layout(scene=dict(
    #                     xaxis_title='Time',
    #                     yaxis_title='Blood Pressure',
    #                     zaxis_title='ECG'),
    #                 margin=dict(r=0, l=0, b=0, t=0))


    # Convert the figure to JSON
    graph_data = [BloodPressureGraph, BloodPressureBarGraph, BodyTemperatureGraph, BodyTemperatureBarGraph, MeanPieChart, fig]

    # Convert the data to JSON
    graph_json = json.dumps(graph_data, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('graph.html', graph_json=graph_json, email=email, device_name=device_name, device_key=device_key)

# Table page
@app.route('/table/<email>/<device_name>/<device_key>')
@login_required
def table(email, device_name, device_key):
    # read csv file
    file_path = f"./data/{device_key}.csv"
    db = pd.read_csv(file_path)

     # Define table data
    header = dict(values=["Index"]+db.columns.to_list(),
                    align='center',
                    font=dict(color='white', size=14),
                    fill=dict(color='#E72929'))

    cells = dict(values=[db.index.to_list(),
                        db.Time.to_list(),
                        db.Blood_Pressure.to_list(),
                        db.ECG.to_list(),
                        db.Body_Temperature.to_list()],

                align='center',
                font=dict(color='#E72929', size=14),
                fill=dict(color=["#EEEEEE", "#FEF2F4"]))

    table_data = {
        'type': 'table',
        'header': header,
        'cells': cells
    }

    graph_data = [table_data]

    # Convert the data to JSON
    graph_json = json.dumps(graph_data)
    return render_template('table.html', graph_json=graph_json)

# Logout Page
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# API page Here

# HTTP GET Read Record
@app.route('/healthbox/api/<email>/<device_name>/<api>', methods=["GET"])
def api(email, device_name, api):
    # Open csv file here
    file_path = f"./data/{api}.csv"
    fileData = pd.read_csv(file_path)

    # data = {
    #     "DeviceData":{
    #         "id": 1,
    #         "Time": ["12:00"],
    #         "BloodPressure": [120],
    #         "ECG": [200],
    #         "BodyTemperature": [35]
    #     },
    #     "email": "email@gmail.com",
    #     "DeviceName": "Device 1",
    # }

    # data = {
    #     "DeviceData":fileData.to_dict(orient="records"),
    #     "email": email,
    #     "DeviceName": device_name
    # }

    data = {
        "index": fileData.index.tolist(),
        "Blood_Pressure": fileData["Blood_Pressure"].tolist(),
        "Body_Temperature": fileData["Body_Temperature"].tolist(),
        "ECG": fileData["ECG"].tolist(),
        "Time": fileData["Time"].tolist()
    }

    if data:
        return jsonify(data=data)
    else:
        return jsonify(error={"Not Found: Data or API key not found."})

# HTTP POST - create new record
# @app.route()


if __name__ == '__main__':
    app.run(debug=True)
