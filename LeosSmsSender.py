import requests

# List of countries with their corresponding country codes
country_codes = {
    "1": ("USA", "+1"),
    "44": ("UK", "+44"),
    "91": ("India", "+91"),
    "61": ("Australia", "+61"),
    "33": ("France", "+33"),
    "49": ("Germany", "+49"),
    "34": ("Spain", "+34"),
    "55": ("Brazil", "+55"),
    "56": ("Chile", "+56"),
    "52": ("Mexico", "+52"),
    # Add more countries and their codes as needed
}

# Function to get remaining SMS quota
def check_quota(api_key):
    url = f"https://textbelt.com/quota/{api_key}"
    try:
        response = requests.get(url)
        quota_data = response.json()
        if quota_data.get('success'):
            return quota_data.get('quotaRemaining', 0)
        else:
            print("Error: Could not retrieve quota data.")
            return 0
    except requests.exceptions.RequestException as e:
        print(f"Error: A network error occurred while checking quota: {e}")
        return 0

# Function to send a text message
def send_sms(api_key, phone_number, message):
    url = "https://textbelt.com/text"
    data = {
        'phone': phone_number,
        'message': message,
        'key': api_key
    }

    try:
        response = requests.post(url, data=data)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: A network error occurred: {e}")
        return None

# Function to get user input and send messages
def send_multiple_texts(api_key):
    # Display a simple message that shows you have texts left (this can be adjusted)
    print("Welcome to Leo's SMS Sender. Please make sure you have enough texts in your plan.")

    # Check remaining quota
    remaining_quota = check_quota(api_key)
    print(f"Remaining texts: {remaining_quota}")

    if remaining_quota == 0:
        print("No texts remaining. Exiting.")
        return

    # Ask which country to send to
    print("\nWhich country to send to:")
    for key, value in country_codes.items():
        print(f"{key}: {value[0]} ({value[1]})")
    
    country_choice = input("Enter the number for the country you want to send to: ")

    # Get the selected country code
    if country_choice in country_codes:
        country_name, country_code = country_codes[country_choice]
        print(f"Selected country: {country_name} with country code {country_code}")
    else:
        print("Invalid choice. Exiting.")
        return

    # Ask for phone number (without country code)
    phone_number = input(f"Enter the phone number (without the country code, e.g. 5555555555 for {country_name}): ")
    full_phone_number = country_code + phone_number  # Combine country code with phone number

    # Ask for the message and how many to send
    message = input("What is the message: ")
    num_messages = int(input("How many messages: "))

    # Check if there are enough remaining texts
    if num_messages > remaining_quota:
        print(f"Insufficient texts. You only have {remaining_quota} texts remaining.")
        num_messages = remaining_quota  # Send as many as possible

    # Send the messages
    for i in range(num_messages):
        print(f"Sending message {i+1}/{num_messages}...")
        response = send_sms(api_key, full_phone_number, message)
        if response and response.get('success'):
            print(f"Message {i+1} sent successfully!")
        else:
            print(f"Failed to send message {i+1}: {response.get('error') if response else 'Unknown error'}")

# Your API key here
api_key = "YOUR API KEY HERE"

# Call the function to start sending messages
send_multiple_texts(api_key)
