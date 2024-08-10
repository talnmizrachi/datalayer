import requests
import os
from dotenv import load_dotenv
from global_functions.LoggingGenerator import Logger

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()
load_dotenv()


def get_owner_name(user_id):
	if user_id is None:
		return "Error - Owner is None"
	api_key = os.getenv("HUBSPOT_API_KEY")
	url = f"https://api.hubapi.com/owners/v2/owners/{user_id}"
	headers = {
		'Authorization': f'Bearer {api_key}'
	}

	response = requests.get(url, headers=headers)
	if response.status_code == 200:
		logger.debug(f"Got Response from HubSpot")
		owner_data = response.json()
		owner_name = owner_data.get('firstName', '') + ' ' + owner_data.get('lastName', '')
		return owner_name
	else:
		logger.error(f"Error: Unable to fetch owner data (Status code: {response.status_code})")
		return "Error getting Name from HS"
