import hashlib
import requests
import getpass

def is_common_password(password):
    # Hash the password using SHA-1
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

    # Get the first 5 characters of the SHA-1 hash
    first5_hash = sha1_password[:5]

    # Query the Pwned Passwords API with the first 5 characters
    url = f"https://api.pwnedpasswords.com/range/{first5_hash}"
    response = requests.get(url)

    # Check the returned hashes for a match with the rest of the SHA-1 hash
    hashes = (line.split(':') for line in response.text.splitlines())
    for suffix, count in hashes:
        if sha1_password[5:] == suffix:
            return True  # Password is found in the list of breached passwords

    return False  # Password is not found in the list

# Get user input for password to check (input is hidden)
password = getpass.getpass("Enter your password: ")

# Check the password
if is_common_password(password):
    print("Unsecure: This password has been breached before.")
else:
    print("Secure: This password has not been found in known breaches.")
