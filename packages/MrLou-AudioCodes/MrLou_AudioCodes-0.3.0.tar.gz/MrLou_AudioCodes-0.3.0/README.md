# AudioCodes

## Overview
The `AudioCodes` is a collection of Python packages that I keep re-using and thought would be good to share them

## Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request with your changes. Ensure that your code follows the existing style and includes appropriate tests.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Installation

You can install the package from PyPI using pip:

```
pip install MrLou_AudioCodes
```
---

# **User Guide for HTTPRequest Script**

This script simplifies the process of making HTTP `GET`, `POST`, and `PUT` requests to a server with Basic Authentication. It is structured with reusable classes and functions to handle various API endpoints.
This guide provides an overview of the classes, functions, and usage examples for interacting with a server using the `requests` library. The functions facilitate API calls for common tasks such as fetching data, uploading certificates, and saving configurations.

---

## **Classes Overview**

### 1. **`HTTPRequest`**
   - A base class to handle HTTP requests.
   - **Attributes**:
     - `fqdn`: Fully Qualified Domain Name for the server.
     - `auth`: Basic authentication credentials (Base64 encoded).
   - **Methods**:
     - `_send_request(self, method, url, data=None, files=None)`: Sends an HTTP request (GET, POST, PUT) to the server and returns the response.

### 2. **`GETRequest(HTTPRequest)`**
   - Inherits from `HTTPRequest`. Used to send `GET` requests.
   - **Method**:
     - `send(self, url)`: Sends a `GET` request to the specified `url` and returns the response.

### 3. **`POSTRequest(HTTPRequest)`**
   - Inherits from `HTTPRequest`. Used to send `POST` requests.
   - **Method**:
     - `send(self, url, payload)`: Sends a `POST` request to the specified `url` with `payload` and returns the response.

### 4. **`PUTRequest(HTTPRequest)`**
   - Inherits from `HTTPRequest`. Used to send `PUT` requests.
   - **Method**:
     - `send(self, url, payload, files=None)`: Sends a `PUT` request to the specified `url` with `payload` and optional `files`, returns the response.

---

## **Functions Overview**

### **GET Requests**

1. **`get_alarms(fqdn, auth)`**
   - Sends a `GET` request to retrieve active alarms.
   - **Input**: 
     - `fqdn`: Server FQDN.
     - `auth`: Authentication string.
   - **Output**: List of alarm descriptions, or an empty list if no alarms are found.

2. **`get_status(fqdn, auth)`**
   - Sends a `GET` request to retrieve server status.
   - **Input**: 
     - `fqdn`: Server FQDN.
     - `auth`: Authentication string.
   - **Output**: Server status response.

3. **`get_tls_contexts_list(fqdn, auth)`**
   - Sends a `GET` request to retrieve a list of TLS contexts.
   - **Input**: 
     - `fqdn`: Server FQDN.
     - `auth`: Authentication string.
   - **Output**: List of TLS contexts, or the response object.

4. **`get_device_certificate(fqdn, auth, tls_ctxt_id)`**
   - Sends a `GET` request to retrieve the device certificate for the specified TLS context.
   - **Input**: 
     - `fqdn`: Server FQDN.
     - `auth`: Authentication string.
     - `tls_ctxt_id`: TLS context ID.
   - **Output**: Device certificate as a string, or the response object.

5. **`get_ini(fqdn, auth, ini_name, ini_file_path)`**
   - Sends a `GET` request to retrieve the device ini configuration file.
   - **Input**: 
     - `fqdn`: Server FQDN.
     - `auth`: Authentication string.
     - `ini_name`: the file name.
     - `ini_file_path`: the full path.
   - **Output**: Device ini configuration file.

### **POST Requests**

1. **`save_configuration(fqdn, auth)`**
   - Sends a `POST` request to save the server configuration.
   - **Input**:
     - `fqdn`: Server FQDN.
     - `auth`: Authentication string.
   - **Output**: Response status code.

### **PUT Requests**

1. **`upload_trusted_root_certificates(fqdn, auth, tls_ctxt_id, cert_name, cert_file_path)`**
   - Uploads trusted root certificates to the server for the specified TLS context.
   - **Input**:
     - `fqdn`: Server FQDN.
     - `auth`: Authentication string.
     - `tls_ctxt_id`: TLS context ID.
     - `cert_name`: Name of the certificate.
     - `cert_file_path`: File path to the certificate.
   - **Output**: Upload response.

2. **`upload_key_certificate(fqdn, auth, tls_ctxt_id, cert_name, cert_file_path)`**
   - Uploads a private key certificate to the server for the specified TLS context.
   - **Input**:
     - `fqdn`: Server FQDN.
     - `auth`: Authentication string.
     - `tls_ctxt_id`: TLS context ID.
     - `cert_name`: Name of the certificate.
     - `cert_file_path`: File path to the certificate.
   - **Output**: Upload response.

3. **`upload_device_certificate(fqdn, auth, tls_ctxt_id, cert_name, cert_file_path)`**
   - Uploads a device certificate to the server for the specified TLS context.
   - **Input**:
     - `fqdn`: Server FQDN.
     - `auth`: Authentication string.
     - `tls_ctxt_id`: TLS context ID.
     - `cert_name`: Name of the certificate.
     - `cert_file_path`: File path to the certificate.
   - **Output**: Upload response.

4. **`upload_incremental_cli_script(fqdn, auth, cli_name, cli_file_path)`**
   - Uploads an incremental CLI script. 
   - **Input**:
     - `fqdn`: Server FQDN.
     - `auth`: Authentication string.
     - `cli_name`: the name of the cli script file.
     - `cli_file_path`: the location of the cli script file.
   - **Output**: Upload response.

5. **`change_user_config(fqdn, auth, username, password, status, password_age`**
   - Uploads an incremental CLI script. 
   - **Input**:
     - `fqdn`: Server FQDN.
     - `auth`: Authentication string.
     - `username`: the user to change or create a new user.
     - `password`: the new password. The valid value is a string of 8 to 40 ASCII characters, and can't contain the following: Wide characters, Spaces, Backslashes (\)
     - `status`: the status of the user. (New, Valid, Inactivity)
     - `password_age`: Defines the duration (in days) of the validity of the password. ( valid value is 0 to 10000)
   - **Output**: Upload response.

---
## **Example Usage**

### **GET Example: Retrieve Alarms**
```python
alarms = get_alarms('example.com', 'auth_string')
print(alarms)
```

### **POST Example: Save Configuration**
```python
response = save_configuration('example.com', 'auth_string')
print(response.status_code)
```

### **PUT Example: Upload Root Certificate**
```python
response = upload_trusted_root_certificates('example.com', 'auth_string', 'tls_id', 'cert_name', '/path/to/cert.pem')
print(response.text)
```

---

## **Error Handling**

- The script prints HTTP errors (e.g., `HTTPError`, `Timeout`, `ConnectionError`) when requests fail.
- In case of JSON decoding errors or unexpected server responses, it prints appropriate messages and handles failures gracefully.
