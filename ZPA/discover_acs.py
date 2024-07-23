import json
import csv
import requests
import getpass
from pprint import pprint
import os

BASE_URL = "https://config.private.zscaler.com"

def get_customer_id():
    return input("Enter the Customer ID retrieved from the ZPA Admin Portal: ")

def authenticate(base_url):
    client_id = input("Enter the Client ID retrieved from the ZPA Admin Portal: ")
    client_secret = getpass.getpass("Enter the Client Secret retrieved from the ZPA Admin Portal: ")

    auth_payload = {
        'client_id': client_id,
        'client_secret': client_secret
    }

    auth_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = requests.post(f"{base_url}/signin", headers=auth_headers, data=auth_payload)
    response.raise_for_status()  # Raise an exception for HTTP errors

    print("Authentication successful... proceeding...")
    auth_response = response.json()
    token = f"{auth_response.get('token_type')} {auth_response.get('access_token')}"
    
    return token

def retrieve_acs(token, base_url, cust_id):
    headers = {
        'Authorization': token
    }

    response = requests.get(f"{base_url}/mgmtconfig/v1/admin/customers/{cust_id}/connector", headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors

    acs = response.json().get('list', [])
    return acs

def parse_and_output(acs):
    scrubbed_acs = [
        {
            "name": ac.get('name'),
            "id": ac.get('id'),
            "os": ac.get('runtimeOS'),
            "description": ac.get('description') if ac.get('description') else "No description",
            "Private IP": ac.get('privateIp')
        }
        for ac in acs
    ]

    while True:
        output = input("Would you like to print (1), export as JSON (2), export as CSV (3), or print & export (4) the results? Enter 'q' to quit.' [1]: \n").strip().lower()
        print()

        if output == "1" or output == "":
            pprint(scrubbed_acs)
            print()

        elif output == "2":
            with open("output.json", 'w') as out:
                json.dump(scrubbed_acs, out, indent=4)
            print(f"File exported to {os.getcwd()}/output.json")
            print()

        elif output == "3":
            with open("output.csv", 'w', newline='') as out:
                writer = csv.DictWriter(out, fieldnames=scrubbed_acs[0].keys())
                writer.writeheader()
                writer.writerows(scrubbed_acs)
            print(f"File exported to {os.getcwd()}/output.csv")
            print()

        elif output == "4":
            pprint(scrubbed_acs)
            print()
            with open("output.json", 'w') as out:
                json.dump(scrubbed_acs, out, indent=4)
            print(f"File exported to {os.getcwd()}/output.json")
            print()
            with open("output.csv", 'w', newline='') as out:
                writer = csv.DictWriter(out, fieldnames=scrubbed_acs[0].keys())
                writer.writeheader()
                writer.writerows(scrubbed_acs)
            print(f"File exported to {os.getcwd()}/output.csv")
            print()

        elif output == "q":
            break

        else:
            print("Invalid input. Please try again.")
            continue

def main():
    base_url = BASE_URL
    cust_id = get_customer_id()
    token = authenticate(base_url)
    acs = retrieve_acs(token, base_url, cust_id)
    parse_and_output(acs)

if __name__ == "__main__":
    main()