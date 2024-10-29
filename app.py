from flask import Flask, render_template, request, redirect, url_for, flash
from rsa_functions import generate_keys, encrypt_message, decrypt_message, check_prime_number

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

# Global variables to store keys
public_key = None
private_key = None

@app.route('/')
def index():
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
    return render_template('encryption.html', public_key=public_key, private_key=private_key)

@app.route('/decryption')
def decryption():
    return render_template('decryption.html', public_key=public_key, private_key=private_key)

@app.route('/about_me')
def about_me():
    return render_template('about_me.html', public_key=public_key, private_key=private_key)

if __name__ == '__main__':
    app.run(debug=True)
