from flask import Flask, render_template, redirect, url_for, request, Response
import cv2 
import numpy as np
import face_recognition
import os 
from datetime import datetime 
import time
import imutils
from web3 import Web3
import pandas as pd
import json
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
with open('contract_abi.json', 'r') as f:
        contract_abi = json.load(f)

# Define contract address and instantiate contract
contract_address = '0xff66466abe9657e2A097EB90Dd611e730235B2A4'
contract = web3.eth.contract(address=contract_address, abi=contract_abi)


def clean_csv():
    import pandas as pd
    df = pd.read_csv("Attendance.csv")
    cols = ["Name", "Time", "Date"]
    df = pd.read_csv("Attendance.csv", names = cols)
    df = df.drop_duplicates(subset=['Name']).reset_index(drop=True)
    df.to_csv('clean.csv', header=False, index=True)


path = "images"
images = []
personName = []
myList = os.listdir(path)
print(myList)
    # Retrieve names from image directories
for root, dirs, files in os.walk(path):
    for cu_img in files:
        current_Img = cv2.imread(os.path.join(root, cu_img))
        images.append(current_Img)
        personName.append(os.path.join(os.path.basename(root)))
print("personName:")
print(personName)

    # Encode images
def faceEncoding(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnow = faceEncoding(images)
print("All encoding complete")

with open("Attendance.csv", "r+") as f:
    f.truncate(0)

def attendance(name):
    i=1
    with open("Attendance.csv", "r+") as f:
        myDataList = f.readline()
        nameList = []
        for line in myDataList:
            entry = line.split(",")
            
            nameList.append(entry[0])
            
        
        if name not in nameList:

            time_now = datetime.now() # capture current time and date 
            tStr = time_now.strftime("%H:%M:%S")
            dStr = time_now.strftime("%D/%m/%Y")
            i=i+1
            f.writelines(f'{name}, {tStr}, {dStr} \n')
            return 0
        
        
    df = pd.read_csv('Attendance.csv')
    df=df.drop_duplicates().reset_index(drop=True)  


def mark_attendance():
    # To access the camera
    cap = cv2.VideoCapture(0)
    t_end = time.time() + 15
    while time.time() < t_end:
    # while True:
        ret, frame  = cap.read()
        frame = imutils.resize(frame, width=600)
        faces = cv2.resize(frame, (0,0), None, fx=0.25, fy=0.25)
        faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

        facesCurrentFrame = face_recognition.face_locations(faces)
        encodesCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame)

        for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnow, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnow, encodeFace)
            print(faceDis)
            matchIndex = np.argmin(faceDis)
            print("matchIndex:")
            print(matchIndex)

            if matches[matchIndex]:
                name = personName[matchIndex].upper()
                print(name)
                dis = str(round(max(faceDis)*100, 2))
                print("dis" + dis)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, dis, (x1 + 6, y1 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                attendance(name)
                break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 
        if cv2.waitKey(1) == 13:
            break
    cap.release()
    clean_csv()

    #add mymodule here
    with open('clean.csv', 'r') as f:
        csv_data = f.readlines()

    # Loop through each row and add it to the contract
    for row in csv_data:
        row = row.strip().split(',')

        # Call the contract function to add the row to the blockchain
        tx_hash = contract.functions.storeCSV(int(row[0])+1, row[1], row[2], row[3]).transact({
            'from': web3.eth.accounts[0],
            'gas': 3000000
        })
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        print('Row added to blockchain:', tx_receipt)

    # Call the contract functions to get data from the blockchain
    csv_count = contract.functions.getCSVCount().call()
    print('CSV count:', csv_count)

    for i in range(csv_count):
        csv_data = contract.functions.getCSV(i).call()
        mark_attendance.returnable_csv = []
        mark_attendance.returnable_csv.append(csv_data)
        print('records in my module', mark_attendance.returnable_csv)


app = Flask(__name__)


app.secret_key = 'abcd'
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'attendance_login'
 
mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('take.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)


@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/take')
def take():
    return render_template('take.html')

@app.route('/video_feed')
def video_feed():
    return render_template('video_feed.html')

@app.route('/video')
def video():
    return Response(mark_attendance(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/table')
def table():
    id=0
    csv_data = []
    for i in range(contract.functions.getCSVCount().call()):
        id, name, time, date = contract.functions.getCSV(i).call()
        csv_data.append({'id': id, 'name': name, 'time': time, 'date': date})
    return render_template('table.html', attendance_records=csv_data)


if __name__ == '__main__':
    app.run(debug=True)