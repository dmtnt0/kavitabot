import requests
import json
from urllib.parse import urlparse
# import discord
# from discord.ext import commands
# from discord import app_commands

# KAVITA CLASS & FUNCTIONS
#--------------------------------------------------------------------------#
class KavitaAPI:
    # Authenticate with Kavita
    def auth(url):
        parsed_url = urlparse(url)
        host_address = parsed_url.scheme + "://" + parsed_url.netloc
        api_key = parsed_url.path.split('/')[-1]

        # Authenticate Session
        login_endpoint = "/api/Plugin/authenticate"
        try:
            apikeylogin = requests.post(host_address + login_endpoint + "?apiKey=" + api_key + "&pluginName=pythonScanScript")
            apikeylogin.raise_for_status() # check if the response code indicates an error
            jwt_token = apikeylogin.json()['token']
        except requests.exceptions.RequestException as e:
            print("Error during authentication:", e)
            exit()

        # Set session headers
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json"
        }

        # Return base url and headers
        return host_address,headers

    # Get all users
    def users(url):
        host_address,headers = KavitaAPI.auth(url)
        full_url = host_address + "/api/Users?includePending=true"
        body = {}
        raw = requests.get(full_url, json=body, headers=headers)
        response = raw.json()
        
        return response

    # Send invitation email
    def invite(url,email):
        host_address,headers = KavitaAPI.auth(url)
        full_url = host_address + "/api/Account/invite"
        body = {
            "email": email,
            "roles": [
                "Download",
                "Change Password",
                "Bookmark",
                "Login"
            ],
            "libraries": [
                3
            ],
            "ageRestriction": {
                "ageRating": 0,
                "includeUnknowns": True
            }
        }

        raw = requests.post(full_url, json=body, headers=headers)
        response = raw.json()

        if raw.status_code == 200:
            return response["emailLink"]
        else:
            print(f"\nInvite failed: {response.status_code}")

            
