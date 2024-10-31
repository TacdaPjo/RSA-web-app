import requests
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from rsa_functions import generate_keys, encrypt_message, decrypt_message, check_prime_number
import sqlite3
from datetime import datetime
import time
import os



app = Flask(__name__)
app.secret_key = 'supersecretkey' 


UPLOAD_FOLDER = 'static/uploads'

# Ensure that the directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
    return render_template('index.html')


@app.route('/encryption')
def encryption():
    return render_template('encryption.html', public_key=public_key, private_key=private_key)

@app.route('/decryption')
def decryption():
    return render_template('decryption.html', public_key=public_key, private_key=private_key)

@app.route('/about_me')
def about_me():
    return render_template('about_me.html', public_key=public_key, private_key=private_key)

@app.route('/')
def home():
    return render_template('index.html')

def convert_image_to_binary(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
    return binary_data

def retrieve_images():
    conn = sqlite3.connect('images.db')
    c = conn.cursor()

    c.execute("SELECT name, species, photo FROM leaderboard")
    records = c.fetchall()

    for record in records:
        name, species, photo_binary = record
        
        # Write the binary data back to an image file
        with open(f"{name}_{species}.jpg", 'wb') as file:
            file.write(photo_binary)

    conn.close()


def save_to_storage(file):
    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    return url_for('static', filename=f'uploads/{filename}', _external=True)

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files or 'name' not in request.form or 'species' not in request.form or 'length' not in request.form:
        return jsonify({'error': 'Missing fields'}), 400

    name = request.form['name']
    length = request.form['length']
    species = request.form['species']
    file = request.files['photo']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    if file:
        # Save the file to storage and get the URL
        photo_url = save_to_storage(file)

        # Insert the data into the database
        conn = sqlite3.connect('images.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO leaderboard (name, length, species, photo_url)
            VALUES (?, ?, ?, ?)
        ''', (name, length, species, photo_url))
        conn.commit()
        conn.close()

        return jsonify({'photo_url': photo_url, 'message': 'Uploaded successfully'})
    else:
        return jsonify({'error': 'Allowed file types are jpg, jpeg, png, gif'}), 400


@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    conn = sqlite3.connect('images.db')
    c = conn.cursor()
    c.execute('''
        SELECT name, length, species, photo_url
        FROM leaderboard
        ORDER BY length ASC
        LIMIT 5
    ''')
    records = c.fetchall()
    conn.close()

    # Convert records to a list of dictionaries
    leaderboard_entries = [
        {
            'name': record[0],
            'length': record[1],
            'species': record[2],
            'photo_url': record[3]
        } for record in records
    ]

    return jsonify(leaderboard_entries)
if __name__ == '__main__':
    app.run(debug=True)
