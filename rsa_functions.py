import math

# --- RSA Functions ---
def rsa_encrypt(p, q):
    n = p * q
    return n

def euler_totient(p, q):
    phi_n = (p - 1) * (q - 1)
    return phi_n

def choose_public_e(phi_n):
    possible_e_values = [3, 5, 7, 65537]
    for e in possible_e_values:
        if math.gcd(e, phi_n) == 1:
            return e

def compute_private_d(e, phi_n):
    d = pow(e, -1, phi_n)
    return d

def generate_keys(p, q):
    n = rsa_encrypt(p, q)
    phi_n = euler_totient(p, q)
    e = choose_public_e(phi_n)
    d = compute_private_d(e, phi_n)
    return (n, e), (n, d)

def encrypt(message_int, public_key):
    n, e = public_key
    if message_int >= n:
        raise ValueError("Message too large for the chosen primes. Choose larger primes.")
    ciphertext = pow(message_int, e, n)
    return ciphertext

def encrypt_message(message, public_key):
    encrypted_message = [encrypt(ord(char), public_key) for char in message]
    return encrypted_message

def decrypt(ciphertext, private_key):
    n, d = private_key
    decrypted_message = pow(ciphertext, d, n)
    return decrypted_message

def decrypt_message(encrypted_message, private_key):
    decrypted_message = ''.join(chr(decrypt(char, private_key)) for char in encrypted_message)
    return decrypted_message

def check_prime_number(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# --- CLI Application Functions ---
def generate_rsa_keys():
    try:
        p = int(input("Enter a prime number (p): "))
        if not check_prime_number(p):
            print(f"{p} is not a prime number.")
            return None, None

        q = int(input("Enter another prime number (q): "))
        if not check_prime_number(q):
            print(f"{q} is not a prime number.")
            return None, None
    except ValueError:
        print("Please enter valid integers for p and q.")
        return None, None

    public_key, private_key = generate_keys(p, q)
    print("Keys generated successfully!")
    print(f"Public Key: {public_key}")
    print(f"Private Key: {private_key}")
    return public_key, private_key

def encrypt_message_cli(public_key):
    message = input("Enter the message to encrypt: ")
    ciphertext = encrypt_message(message, public_key)
    print("Encrypted message:", ciphertext)
    return ciphertext

def decrypt_message_cli(ciphertext, private_key):
    decrypted_message = decrypt_message(ciphertext, private_key)
    print("Decrypted message:", decrypted_message)
