from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from rsa_functions import generate_keys, encrypt_message, decrypt_message, check_prime_number
import sqlite3
from datetime import datetime
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

# Global variables to store keys
public_key = None
private_key = None

@app.route('/')
def index():
    log_activity(request.path, 0, request.user_agent.string)
    return render_template('index.html')

@app.route('/generate_keys', methods=['POST'])
def generate_rsa_keys():
    global public_key, private_key

    p = int(request.form['p'])
    q = int(request.form['q'])

    if not (check_prime_number(p) and check_prime_number(q)):
        flash("Both numbers must be prime.", "danger")
        return redirect(url_for('index'))

    public_key, private_key = generate_keys(p, q)
    flash("RSA keys generated successfully!", "success")
    return render_template('encryption.html', public_key=public_key, private_key=private_key)

@app.route('/encrypt_result', methods=['POST'])
def encrypt_result():
    if public_key is None:
        flash("Please generate RSA keys first.", "danger")
        return redirect(url_for('index'))

    message = request.form['message']
    ciphertext = encrypt_message(message, public_key)
    return render_template('encrypt_result.html', message=message, ciphertext=ciphertext)

@app.route('/decrypt_result', methods=['POST'])
def decrypt_result():
    if private_key is None:
        flash("Please generate RSA keys first.", "danger")
        return redirect(url_for('index'))

    encrypted_message = request.form['encrypted_message']
    encrypted_message = list(map(int, encrypted_message.strip('[]').split(',')))
    decrypted_message = decrypt_message(encrypted_message, private_key)
    return render_template('decrypt_result.html', encrypted_message=encrypted_message, decrypted_message=decrypted_message)

@app.route('/encryption')
def encryption():
    log_activity(request.path, 0, request.user_agent.string)
    return render_template('encryption.html', public_key=public_key, private_key=private_key)

@app.route('/decryption')
def decryption():
    log_activity(request.path, 0, request.user_agent.string)
    return render_template('decryption.html', public_key=public_key, private_key=private_key)

@app.route('/about_me')
def about_me():
    log_activity(request.path, 0, request.user_agent.string)
    return render_template('about_me.html', public_key=public_key, private_key=private_key)

def log_activity(page_visited, time_spent, browser_info):
    max_retries = 5  # Number of retries for database access
    retry_delay = 0.1  # Delay between retries (in seconds)

    for attempt in range(max_retries):
        try:
            # Use `with` statement to ensure the connection is properly closed
            with sqlite3.connect('user_activity.db', check_same_thread=False) as conn:
                c = conn.cursor()
                c.execute('''
                    INSERT INTO activity_log (page_visited, time_spent, browser_info, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', (page_visited, time_spent, browser_info, datetime.now()))
                conn.commit()
            break  # Exit loop if insertion is successful
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                print(f"Database is locked. Retry attempt {attempt + 1}...")
                time.sleep(retry_delay)  # Wait before retrying
            else:
                print("Error inserting into database:", e)
                break  # Exit loop if it's a different database error

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route to log user activity
@app.route('/log_activity', methods=['POST'])
def log_user_activity():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'failed', 'message': 'No data received'}), 400
        
        # Extract data
        page_visited = data.get('page')
        time_spent = data.get('time_spent')
        browser_info = request.user_agent.string  # Gets browser details

        # Validate data
        if page_visited is None or time_spent is None:
            return jsonify({'status': 'failed', 'message': 'Missing data fields'}), 400

        # Log activity to the database
        log_activity(page_visited, time_spent, browser_info)
        return jsonify({'status': 'success'})
    except Exception as e:
        print("Error logging activity:", e)  # Error logging
        return jsonify({'status': 'failed', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
