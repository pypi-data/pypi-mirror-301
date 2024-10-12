import MrLou_AudioCodes
import base64
import random
import string

fqdn = "sbc.lpdne.eu"
username = "api"
password = "woking"


def generate_password(length=25):
    if not (8 <= length <= 40):
        raise ValueError("Password length must be between 8 and 40 characters.")

    # Define valid ASCII characters excluding spaces and backslashes
    valid_chars = string.ascii_letters + string.digits + string.punctuation
    valid_chars = valid_chars.replace('\\', '').replace(' ', '')

    # Generate password of the desired length
    generated_password = ''.join(random.choice(valid_chars) for _ in range(length))

    return generated_password


def create_auth(auth_username: str, auth_password: str) -> str:
    # Concatenate username and password with a colon
    credentials = f"{auth_username}:{auth_password}"

    # Encode the credentials in Base64
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    # Return only the Base64 encoded string without the "Basic " prefix
    return encoded_credentials


auth_header = create_auth(username, password)
MrLou_AudioCodes.acsbc_api.get_status(fqdn, auth_header)


# Generate a 25-character password
new_gpassword = generate_password(25)
print("Generated password:", new_gpassword)


MrLou_AudioCodes.acsbc_api.change_user_password(
    fqdn,
    auth_header,
    "Admin",
    new_gpassword,
    "valid",
    "180"
)
