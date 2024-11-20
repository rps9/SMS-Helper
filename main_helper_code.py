import requests
import smtplib
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import os

# Get the weather for a given city
def get_weather(city):
    weather_key = os.getenv("WEATHER_API_KEY")
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_key}"

    weather_response = requests.get(weather_url)
    if weather_response.status_code == 200:
        return weather_response.json()
    else:
        print("Failed to fetch weather data..")
        return None

# Sends message using SMTP
def send_message(message):
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('EMAIL_PASSWORD')
    recipient_email = os.getenv('RECIPIENT_EMAIL')

    # Connect to the notification email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)

    # Send the message
    server.sendmail(sender_email, recipient_email, message)
    server.quit()

def get_clothing_recommendation(feels_like_temp_F):
    """Returns clothing suggestions based on 'feels like' temperature."""
    if feels_like_temp_F < 32:
        return f"It will feel like {feels_like_temp_F}, so wear a heavy coat."
    elif 32 <= feels_like_temp_F < 50:
        return f"It will feel like {feels_like_temp_F}, so wear long sleeves or a sweatshirt."
    elif 50 <= feels_like_temp_F < 65:
        return f"It will feel like {feels_like_temp_F}, so wear a light jacket."
    elif 65 <= feels_like_temp_F < 80:
        return f"It will feel like {feels_like_temp_F}, so wear comfortable, breathable clothing."
    else:
        return f"It will feel like {feels_like_temp_F}, so dress lightly, perhaps shorts and a t-shirt."
    
def main():
    #load_dotenv() # UNCOMMENT FOR TESTING

    # Fetch weather data
    weather_data = get_weather('Boston')
    if not weather_data:
        return

    # Kelvin to Fahrenheit
    high_temp_F = int((weather_data['main']['temp_max'] - 273.15) * 1.8 + 32)
    low_temp_F = int((weather_data['main']['temp_min'] - 273.15) * 1.8 + 32)
    feels_like_F = int((weather_data['main']['feels_like'] - 273.15) * 1.8 + 32)

    # Extract day of the week
    timestamp = weather_data['dt']
    timezone_offset = weather_data['timezone']
    utc_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    local_time = utc_time + timedelta(seconds=timezone_offset)
    day_of_the_week = local_time.strftime('%A')

    # Construct the message
    clothing_recommendation = get_clothing_recommendation(feels_like_F)
    message = (
        f"Good morning, happy {day_of_the_week}!\n\n"
        f"The high today will be {high_temp_F}, and the low will be {low_temp_F}.\n\n"
        f"{clothing_recommendation}"
    )
    

    send_message(message)

if __name__ == "__main__":
    main()
