import requests
import json
import urllib3
from requests.auth import HTTPBasicAuth

# 1. Configuration - Update these with your actual Docker credentials
protocol = 'https'
host = '127.0.0.1'  # Since we are running locally
port = 55000
user = 'wazuh-wui'   # Default or your custom user
password = 'YOUR_PASSWORD_HERE' # Update this to your actual password

# Disable SSL warnings for our local self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_wazuh_token():
    login_url = f"{protocol}://{host}:{port}/security/user/authenticate"
    try:
        print(f"[*] Attempting to authenticate with {login_url}...")
        response = requests.get(login_url, auth=HTTPBasicAuth(user, password), verify=False)
        response.raise_for_status()
        token = response.json().get('data', {}).get('token')
        print("[+] Token successfully retrieved!")
        return token
    except Exception as e:
        print(f"[!] Authentication Failed: {e}")
        return None

def test_connection(token):
    if not token: return
    
    headers = {'Authorization': f'Bearer {token}'}
    status_url = f"{protocol}://{host}:{port}/manager/status"
    
    try:
        print("[*] Requesting Manager status...")
        response = requests.get(status_url, headers=headers, verify=False)
        print("\n=== Wazuh Manager Status ===")
        print(json.dumps(response.json(), indent=4))
    except Exception as e:
        print(f"[!] Request Failed: {e}")

if __name__ == "__main__":
    jwt_token = get_wazuh_token()
    test_connection(jwt_token)

