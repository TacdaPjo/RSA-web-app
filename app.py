import requests
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from rsa_functions import generate_keys, encrypt_message, decrypt_message, check_prime_number
import sqlite3
from datetime import datetime
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey' 

IPINFO_API_KEY = "8b6ee932dcdc9c"

public_key = None
private_key = None

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


#Routes goes here!
@app.route('/')
def index():
    client_ip = get_client_ip()
    country = get_country(client_ip)
    log_activity(request.path, 0, request.user_agent.string, request.remote_addr, country)
    return render_template('index.html')


@app.route('/encryption')
def encryption():
    client_ip = get_client_ip()
    country = get_country(client_ip)
    log_activity(request.path, 0, request.user_agent.string, request.remote_addr, country)
    return render_template('encryption.html', public_key=public_key, private_key=private_key)

@app.route('/decryption')
def decryption():
    client_ip = get_client_ip()
    country = get_country(client_ip)
    log_activity(request.path, 0, request.user_agent.string, request.remote_addr, country)
    return render_template('decryption.html', public_key=public_key, private_key=private_key)

@app.route('/about_me')
def about_me():
    client_ip = get_client_ip()
    country = get_country(client_ip)
    log_activity(request.path, 0, request.user_agent.string, request.remote_addr, country)
    return render_template('about_me.html', public_key=public_key, private_key=private_key)

@app.route('/')
def home():
    return render_template('index.html')


#Database stuffs goes here
def get_client_ip():
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.remote_addr



def get_country(ip_address):
    private_ip_prefixes = ("192.168.", "10.", "172.", "127.")

    if ip_address.startswith(private_ip_prefixes):
        print("Detected local IP. Returning 'Local Network'.")
        return "Local Network"  

    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json?token={IPINFO_API_KEY}")
        data = response.json()
        print("API Response:", data)
        return data.get("country", "Unknown")
    
    except requests.RequestException as e:
        print(f"Error fetching country: {e}")
        return "Unknown"

def log_activity(page_visited, time_spent, browser_info, ip_address, country):
    max_retries = 5
    retry_delay = 0.1

    for attempt in range(max_retries):
        try:
            with sqlite3.connect('user_activity.db', check_same_thread=False) as conn:
                c = conn.cursor()
                c.execute('''
                    INSERT INTO activity_log (page_visited, time_spent, browser_info, timestamp, ip_address, country)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (page_visited, time_spent, browser_info, datetime.now(), ip_address, country))
                conn.commit()
            break
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                print(f"Database is locked. Retry attempt {attempt + 1}...")
                time.sleep(retry_delay)
            else:
                print("Error inserting into database:", e)
                break


@app.route('/log_activity', methods=['POST'])
def log_user_activity():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'failed', 'message': 'No data received'}), 400
        
        page_visited = data.get('page')
        time_spent = data.get('time_spent')
        browser_info = request.user_agent.string  
        ip_address = request.remote_addr 
        country = get_country(ip_address)

        if page_visited is None or time_spent is None:
            return jsonify({'status': 'failed', 'message': 'Missing data fields'}), 400

        log_activity(page_visited, time_spent, browser_info, ip_address, country)
        return jsonify({'status': 'success'})
    except Exception as e:
        print("Error logging activity:", e) 
        return jsonify({'status': 'failed', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
