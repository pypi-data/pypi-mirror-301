import requests
import urllib3
from requests.exceptions import ConnectionError, Timeout, HTTPError

# Suppress only the InsecureRequestWarning from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class HTTPRequest:
    def __init__(self, fqdn, auth):
        self.fqdn = fqdn
        self.auth = auth
        self.headers = {
            'Authorization': f'Basic {self.auth}'
        }

    def _send_request(self, method, url, data=None, files=None):
        url = f"https://{self.fqdn}/{url}"
        try:
            response = requests.request(method, url, headers=self.headers, data=data, files=files, verify=False)
            response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
            return response
        except HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


class GETRequest(HTTPRequest):
    def send(self, url):
        return self._send_request("GET", url)


class POSTRequest(HTTPRequest):
    def send(self, url, payload):
        return self._send_request("POST", url, data=payload)


class PUTRequest(HTTPRequest):
    def send(self, url, payload, files=None):
        return self._send_request("PUT", url, data=payload, files=files)


# Functions to use GET method using class GETRequest(HTTPRequest)


def get_alarms(fqdn, auth):
    url = f'api/v1/alarms/active'
    request = GETRequest(fqdn, auth)
    response = request.send(url)
    # Check if the response is valid and contains JSON
    if response and response.status_code == 200:
        try:
            alarms_data = response.json()
        except ValueError:
            # If JSON decoding fails, handle it gracefully
            print(f"Error decoding JSON from response for {fqdn}. Response content: {response.text}")
            return []  # Returning an empty list if JSON decoding fails
        alarms = alarms_data.get("alarms", [])
        descriptions = [alarm["description"] for alarm in alarms]
        return descriptions
    else:
        # Handle the case where the response is not successful
        print(f"No active alarms for {fqdn}. HTTP status code: {response.status_code}")
        return []  # Return an empty list when there are no alarms or the request fails


def get_status(fqdn, auth):
    url = f'api/v1/status'
    request = GETRequest(fqdn, auth)
    response = request.send(url)
    if response:
        print(f"Status Response: {response.text}")
    return response


def get_tls_contexts_list(fqdn, auth):
    url = f'api/v1/files/tls'
    request = GETRequest(fqdn, auth)
    response = request.send(url)
    if response:
        dict_response = response.json().get("tls", [])
        return dict_response
    return response


def get_device_certificate(fqdn, auth, tls_ctxt_id):
    url = f'api/v1/files/tls/{tls_ctxt_id}/certificate'
    request = GETRequest(fqdn, auth)
    response = request.send(url)
    if response:
        return response.text
    return response

# Functions to use POST method using class POSTRequest(HTTPRequest)


def save_configuration(fqdn, auth):
    url = 'api/v1/actions/saveConfiguration'
    payload = {}
    request = POSTRequest(fqdn, auth)
    response = request.send(url, payload)
    if response:
        print(f"Save Configuration Response: {response.status_code}")
    return response


# Functions to use PUT method using class PUTRequest(HTTPRequest)


def upload_trusted_root_certificates(fqdn, auth, tls_ctxt_id, cert_name, cert_file_path):
    url = f'api/v1/files/tls/{tls_ctxt_id}/trustedRoot'
    payload = {}
    files = [
        ('', (cert_name, open(cert_file_path, 'rb'), 'application/octet-stream'))

    ]
    request = PUTRequest(fqdn, auth)
    response = request.send(url, payload, files)
    if response:
        print(f"Upload Response: {response.text}")
    return response


def upload_key_certificate(fqdn, auth, tls_ctxt_id, cert_name, cert_file_path):
    url = f'api/v1/files/tls/{tls_ctxt_id}/privateKey'
    payload = {}
    files = [
        ('', (cert_name, open(cert_file_path, 'rb'), 'application/octet-stream'))

    ]
    request = PUTRequest(fqdn, auth)
    response = request.send(url, payload, files)
    if response:
        print(f"Upload Response: {response.text}")
    return response


def upload_device_certificate(fqdn, auth, tls_ctxt_id, cert_name, cert_file_path):
    url = f'api/v1/files/tls/{tls_ctxt_id}/certificate'
    payload = {}
    files = [
        ('', (cert_name, open(cert_file_path, 'rb'), 'application/octet-stream'))

    ]
    request = PUTRequest(fqdn, auth)
    response = request.send(url, payload, files)
    if response:
        print(f"Upload Response: {response.text}")
    return response
