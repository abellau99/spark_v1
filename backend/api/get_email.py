from pymongo import MongoClient
import requests
import csv
import json

api_keys = {
    "primary_key" : "8d1280112ddd4c9cb899968f77d6a84f",
    "secondary_key" : "c7d05d94a9294b36a510c7ef3023df00"
}

def connect_to_mongodb():
    client = MongoClient("mongodb+srv://abellau99:atO9STN5eiNBS9GS@cluster0.tnqx48h.mongodb.net/")
    db = client['charity_commission']
    collection = db['list_of_charities']
    return collection

def fetch_charity_details(collection):
    # Filter criteria to fetch documents where 'latest_income' is greater than 1,000,000
    filter_criteria = {
        "latest_income": {"$gt": 1000000},
        "email": {"$ne": ""},
        "charity_registration_status": "Registered",
        "charity_in_administration": False,
        "charity_insolvent": False
    }
    
    # Initialize an empty list to store charity details
    charity_details_list = []
    
    # Fetch the cursor from MongoDB collection
    cursor = collection.find(filter_criteria).limit(15)
    
    # Iterate through the cursor to extract 'registered_charity_number' and 'linked_charity_number' for each document
    for doc in cursor:
        charity_details = {
            'registered_charity_number': doc['registered_charity_number'],
            'linked_charity_number': doc['linked_charity_number']
        }
        # Append the charity details dictionary to the list
        charity_details_list.append(charity_details)
    
    # Return the list of charity details as a JSON-formatted string
    return charity_details_list

def get_charity_details(charity_id, suffix):
    base_url = "https://api.charitycommission.gov.uk/register/api/allcharitydetails/"
    url = f"{base_url}{charity_id}/{suffix}"
    headers = {
        "Ocp-Apim-Subscription-Key": api_keys.get('primary_key'),
        'Cache-Control': 'no-cache'
    }
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"API call successful for charity ID {charity_id} and suffix {suffix}. Parsing JSON...")
        # Extracting only required fields: name, email, and phone
        charity = response.json()
        charity_detail = {
            'name': charity.get('charity_name', ''),
            'email': charity.get('email', ''),
            'phone': charity.get('phone', ''),
            'latest_income': charity.get('latest_income', ''),
        }
        return charity_detail
    else:
        print(f"Failed to retrieve data for charity ID {charity_id} and suffix {suffix}. Status code: {response.status_code}")
        return None

def main():
    # Connect to MongoDB
    collection = connect_to_mongodb()
    
    # Fetch the first 15 items from the collection
    charity_numbers = fetch_charity_details(collection)
    
    enriched_charity_details = []

    for charity in charity_numbers:
        registered_id = charity['registered_charity_number']
        linked_id = charity['linked_charity_number']
        
        # Make API call using registered_charity_number as charity_id and linked_charity_number as suffix
        enriched_detail = get_charity_details(registered_id, str(linked_id))
        
        # Append the enriched detail to the list if API call is successful
        if enriched_detail:
            enriched_charity_details.append(enriched_detail)
    
    # Serialize the list of enriched charity details into a JSON-formatted string
    enriched_json_data = json.dumps(enriched_charity_details, indent=4)
    
    print("\nEnriched JSON Data:")
    print(enriched_json_data)

if __name__ == "__main__":
    main()
