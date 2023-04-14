#!/usr/bin/env python3
"""
    Script to make ACI API calls using Signature Based Authentication
    Sample Input:
        apic_ip       : x.x.x.x
        api_path      : /api/node/class/fvTenant.json
        username      : admin
        privatekeyfile: admin.key
"""

import hashlib
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import requests
from pprint import pprint

# Disable certificate validation
requests.packages.urllib3.disable_warnings()

def get_request_signature(method, api_path, privatekeyfile):
    """
    Function to get signature
    """
    # Load the private key from a file
    with open(privatekeyfile, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())

    # Generate the SHA256 digest of some data
    # data = b"GET/api/node/class/fvTenant.json"
    data = (f"{method}{api_path}").encode('utf-8')

    # Sign the digest using the private key
    signature = private_key.sign(data, padding.PKCS1v15(), hashes.SHA256())

    # Encode the signature in Base64 format
    signature_b64 = base64.b64encode(signature).decode('utf-8')
    signature_b64_urlsafe = signature_b64.replace('_', '%2F')

    # Print the signature
    # print(signature_b64_urlsafe)
    return signature_b64_urlsafe


def query_apic(apic_ip, api_path, username, signature_b64_urlsafe):
    """
    Query APIC using Certificate based authentication
    """
    # Set the headers to include in the request
    headers = {
        "Cookie": f"APIC-Certificate-Algorithm=v1.0; APIC-Certificate-DN=uni/userext/user-{username}/usercert-{username}; APIC-Certificate-Fingerprint=fingerprint; APIC-Request-Signature={signature_b64_urlsafe}"
    }

    # Send a GET request with the headers and certificate validation disabled
    response = requests.get(f"https://{apic_ip}{api_path}", headers=headers, verify=False)

    # Print the response content
    print("")
    print(f"Response Status Code: {response.status_code}")
    # print(response.headers)
    print("Response Data: ")
    pprint(response.json())


def main():
    """
    Script main fuction
    """
    apic_ip = input("Enter APIC IP: ")
    api_path = input("Enter API Path: ")
    username = input("Enter Username: ")
    privatekeyfile = input("Enter Private Key filename: ")
    method = "GET"

    # Get signature
    signature_b64_urlsafe = get_request_signature(method, api_path, privatekeyfile)

    # Query APIC
    query_apic(apic_ip, api_path, username, signature_b64_urlsafe)


if __name__ == '__main__':
    main()
