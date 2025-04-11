from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)
CSV_FILE = 'users.csv'

# Only run this once to create the file with correct columns
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["username", "email", "gender", "mobile", "password"])
    df.to_csv(CSV_FILE, index=False)


@app.route('/')
def home():
    return redirect(url_for('login'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        gender = request.form['gender'].strip()
        mobile = request.form['mobile'].strip()
        password = request.form['password'].strip()
        confirm_password = request.form['confirm_password'].strip()

        # Password match check
        if password != confirm_password:
            return "Passwords do not match. Please try again."

        # Load existing users
        df = pd.read_csv(CSV_FILE)

        if username in df['username'].values:
            return "Username already exists. Try a different one."

        # Append new user
        new_user = {
            "username": username,
            "email": email,
            "gender": gender,
            "mobile": mobile,
            "password": password
        }

        df = pd.concat([df, pd.DataFrame([new_user])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        return redirect(url_for('login'))

    return render_template('register.html')






@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        df = pd.read_csv(CSV_FILE)

        # Strip all values in CSV to avoid mismatch due to whitespace
        df['username'] = df['username'].astype(str).str.strip()
        df['password'] = df['password'].astype(str).str.strip()

        if ((df['username'] == username) & (df['password'] == password)).any():
            return redirect(url_for('success'))
        else:
            return "Login failed! Incorrect username or password."

    return render_template('login.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
