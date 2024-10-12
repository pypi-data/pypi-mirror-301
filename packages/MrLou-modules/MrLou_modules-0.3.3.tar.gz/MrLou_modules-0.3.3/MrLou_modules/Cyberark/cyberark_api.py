# cyberark_api.py

import requests

class CyberArkAPI:
    def __init__(self, variables):
        self.variables = variables
        self.full_uri = (f"{self.variables.URI}?"
                         f"AppID={self.variables.AppID}&"
                         f"Safe={self.variables.Safe}&"
                         f"Folder={self.variables.Folder}&"
                         f"Object={self.variables.Object}"
                         )
    def get_credentials(self):
        try:
            response = requests.get(
                self.full_uri,
                cert=(self.variables.client_cert, self.variables.client_key),  # Specify client cert and key
                verify=self.variables.ca_cert
            )

            # Check if the response was successful
            if response.status_code == 200:
                ca_account = response.json()

                # Extract the relevant fields from the response
                #ca_username = ca_account['UserName'].split("\\")[1]
                ca_username = ca_account['UserName']
                ca_password = ca_account['Content']
                ca_password_change_inprocess = ca_account['PasswordChangeInProcess']

                return {
                    "Username": ca_username,
                    "Password": ca_password,
                    "PasswordChangeInProcess": ca_password_change_inprocess
                }

            else:
                # Handle potential errors
                print(f"Failed to retrieve credentials. Status code: {response.status_code}")
                print(response.text)
                return None

        except requests.exceptions.RequestException as e:
            print("Error:", e)
            return None

