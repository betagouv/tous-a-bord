import os
import urllib.parse

import requests


def format_number(number: str):
    return f"0033{number[1:]}"


def send_notification_sms(to_phone_number: str):
    url = "https://europe.ipx.com/restapi/v1/sms/send"
    formattedPhone = format_number(to_phone_number)
    encodedText = urllib.parse.quote_plus(
        """Bonjour,
Vous avez le droit à une tarification solidaire des transports à commun. Profitez-en !"""
    )
    username = os.environ["SMS_SERVICE_USERNAME"]
    password = os.environ["SMS_SERVICE_PASSWORD"]
    params = f"?&originatorTON=1&originatingAddress=TOUS A BORD&destinationAddress={formattedPhone}&messageText={encodedText}&username={username}&password={password}"
    requests.get(f"{url}{params}")
