from boltiot import Bolt
import json
import time
from twilio.rest import Client

# Twilio Credentials
account_sid = 'your_twilio_account_sid'
auth_token = 'your_twilio_auth_token'
twilio_phone_number = 'your_twilio_phone_number'
recipient_phone_number = 'whatsapp:' + 'recipient_phone_number_with_country_code'

client = Client(account_sid, auth_token)
bolt_api_key = "your_bolt_api_key"
device_id = "your_bolt_device_id"

mybolt = Bolt(bolt_api_key, device_id)

def send_whatsapp_message(message):
    message = client.messages.create(
        from_=twilio_phone_number,
        body=message,
        to=recipient_phone_number
    )
    print("WhatsApp message sent with SID:", message.sid)

def convert_to_temperature(sensor_value):
    # Formula for temperature conversion based on the sensor's specifications
    temperature = (sensor_value * 0.48828125) - 50.0
    return temperature

def convert_to_humidity(sensor_value):
    # Formula for humidity conversion based on the sensor's specifications
    humidity = (sensor_value * 0.09765625)
    return humidity

while True:

    response = mybolt.analogRead('A0')
    data = json.loads(response)
    sensor_value = int(data['value'])

    temperature = convert_to_temperature(sensor_value)
    humidity = convert_to_humidity(sensor_value)

    # Send data to Bolt Cloud
    mybolt.serialWrite('Temperature: ' + str(temperature) + '°C, Humidity: ' + str(humidity) + '%')

    # Send data to WhatsApp every hour
    send_whatsapp_message('Temperature: ' + str(temperature) + '°C, Humidity: ' + str(humidity) + '%')

    # Wait for 1 hour before the next iteration
    time.sleep(3600)
