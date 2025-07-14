from flask import Flask, render_template, url_for, redirect, jsonify, Response, abort, session, request, send_file
import sqlite3

from FakeProfile_Detection import FakeProfile_Detection
from Cyberbullying_Detection import Cyberbullying_Detection 

conn = sqlite3.connect('data.db') 


#Use USER Table only when need to add new login users
conn.execute('''CREATE TABLE IF NOT EXISTS user_details
         (ID INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age TEXT,
            gender TEXT NOT NULL,
            password TEXT NOT NULL
         );''')

conn.close()


app = Flask(__name__)


def html_return(msg, redirect_to = "/", delay = 2):
    return f"""
                <html>    
                    <head>      
                        <title>Project Name </title>      
                        <meta http-equiv="refresh" content="{delay};URL='{redirect_to}'" />    
                    </head>    
                    <body> 
                        <h2 style='color:red'> {msg}</h2>
                        <p>This page will refresh automatically.</p> 
                    </body>  
                </html>   
                
                """

@app.route('/signup', methods=['get', 'post'])
def signup(): 
    if request.method == "POST":
        try:
            data = request.json

            print("Data:", data)

            name = data.get('name')
            email = data.get('email')
            age = data.get('age')
            gender = data.get('gender')
            password = data.get('password')

            if not all([name, email, age, gender, password]):
                return jsonify({"error": "All fields are required"}), 400

            # Connect to the database
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()

            # Check if email already exists
            cursor.execute("SELECT * FROM user_details WHERE email = ?", (email,))
            if cursor.fetchone():
                return jsonify({"error": "Email already exists"}), 400

            # Insert user into database
            cursor.execute(
                "INSERT INTO user_details (name, email, age, gender, password) VALUES (?, ?, ?, ?, ?)",
                (name, email, age, gender, password)
            )
            conn.commit()

            return jsonify({"message": "Signup successful"}), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            if conn:
                conn.close()

    else:
        return render_template('signup.html')

@app.route('/login', methods=['get'])      
def redirect_login():
    return redirect(url_for('login_page'))
 
@app.route('/', methods=['get', 'post'])
def login_page():
    global user_details
    if request.method == 'POST':
        try:
            data = request.get_json()

            # Access email and password from the JSON payload
            email = data.get('email')
            password = data.get('password')

            print(email, password)

            # Connect to the database
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()

            # Check if the user exists and password matches
            cursor.execute("SELECT name, password FROM user_details WHERE email = ?", (email,))
            user_data = cursor.fetchone()

            if user_data is None:
                return jsonify({"error": "User not found"}), 404

            user_name, stored_password = user_data

            if password != stored_password:
                return jsonify({"error": "Invalid password"}), 401

            # Query for all user data after successful login
            cursor.execute("SELECT * FROM user_details WHERE email = ?", (email,))
           
            user_details = cursor.fetchone()

            print(user_details)

            # Set session data on successful login
            session['usermail'] = email
            session['name'] = user_name
            session['user_details'] = user_details

            # Pass all user details to the dashboard
            return  jsonify({"message": "success"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            if conn:
                conn.close()

    elif 'usermail' in session.keys():
        # Direct login if user is already in session
        # Query for all user details to send to the dashboard
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_details WHERE email = ?", (session['usermail'],))
        user_details = cursor.fetchone()
        return redirect(url_for('dashboard'))

    else:
        return render_template('login-page.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    print(session['user_details'])
    if "user_details" in session:
        return render_template('dashboard.html', user=session['user_details'], side_focus = 1)
    return redirect('/login')
 
@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

 
@app.route('/fake_profile_detection', methods=['get', 'post'])
def fake_profile_detection():
     
    if "user_details" in session:
        print("Coming Here")
        return render_template('fake_profile_detection.html', user=session['user_details'])
    else:
        return redirect(url_for('login_page'))




@app.route('/fake_profile_detection_result', methods=['get', 'post'])
def fake_profile_detection_result():
    if "user_details" in session:      
        if request.method == 'POST': 

            data = dict(request.form)

   

            prsence_of_profile_pic = data['prsence_of_profile_pic']
            ratio_number_len_of_username = float( data["ratio_number_len_of_username"])
            name_username_matching = data['name_username_matching']
            len_desc = int(data['len_desc'])
            presence_of_extern_url = data['presence_of_extern_url']

            print("Updated Data :", data)

            prediction_result = FakeProfile_Detection(prsence_of_profile_pic,ratio_number_len_of_username,name_username_matching,len_desc,presence_of_extern_url)

            # prediction_result = "Fake"

            print(prediction_result)
 
            return render_template('fake_profile_detection_result.html', user=session['user_details'], prediction_result = prediction_result, side_focus = 2)
    
    return redirect(url_for('login_page'))


# /cyber_bullying_detection
@app.route('/cyber_bullying_detection', methods=['get', 'post'])
def cyber_bullying_detection_ui():
     
    if "user_details" in session:
        print("Coming Here")
        return render_template('cyber_bullying_detection.html', user=session['user_details'])
    else:
        return redirect(url_for('login_page'))
 
@app.route('/cyber_bullying_detection_result', methods=['get', 'post'])
def cyber_bullying_detection_result():
    if "user_details" in session:      
        if request.method == 'POST': 

            data = dict(request.form)

            cyber_bullying_detection_result = Cyberbullying_Detection(data['input_text'])

            cyber_bullying_detection_result = (cyber_bullying_detection_result.replace("_", " ")).title()
 
 
            return render_template('cyber_bullying_detection_result.html', user=session['user_details'], prediction_result = cyber_bullying_detection_result, side_focus = 3, input_text = data['input_text'])
    
    return redirect(url_for('login_page'))

 
 
 
 

 
@app.errorhandler(404)
def nice(_):
    return render_template('error_404.html')

app.secret_key = 'q12q3q4e5g5htrh@werwer15454'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 8080, debug = True)#80)
  