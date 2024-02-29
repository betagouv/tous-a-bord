import os

import sib_api_v3_sdk

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key["api-key"] = os.environ["SEND_IN_BLUE_API_KEY"]

sender_email = "tousabord@beta.gouv.fr"
sender_name = "Tous à bord"


def send_user_creation_email(user_email: str):
    to_email = "tousabord@beta.gouv.fr"
    subject = "Un nouvel utilisateur a été créé"
    text_content = (
        "L'utilisateur "
        + user_email
        + " vient de se créer un compte sur la plateforme. Vous pouvez retrouver la liste des comptes créés à l'adresse https://tous-a-bord.beta.gouv.fr/admin"
    )
    try:
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )
        to = [sib_api_v3_sdk.SendSmtpEmailTo(to_email)]
        sender = sib_api_v3_sdk.SendSmtpEmailSender(
            name=sender_name, email=sender_email
        )
        email = sib_api_v3_sdk.SendSmtpEmail(
            sender=sender, to=to, text_content=text_content, subject=subject
        )
        api_instance.send_transac_email(email)
        return True
    except sib_api_v3_sdk.rest.ApiException as e:
        print("Exception when calling ContactsApi->create_contact: %s", e)
        raise


def send_notification_email(to_email: str, to_name: str):
    subject = "Tarification solidaire des transports en commun !"
    text_content = """
Bonjour,

Vous avez le droit à une tarification solidaire des transports en commun.
Profitez-en !
"""
    try:
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )
        to = [sib_api_v3_sdk.SendSmtpEmailTo(email=to_email, name=to_name)]
        sender = sib_api_v3_sdk.SendSmtpEmailSender(
            name=sender_name, email=sender_email
        )
        email = sib_api_v3_sdk.SendSmtpEmail(
            sender=sender, to=to, text_content=text_content, subject=subject
        )
        api_instance.send_transac_email(email)
        return True
    except sib_api_v3_sdk.rest.ApiException as e:
        print("Exception when calling ContactsApi->create_contact: %s", e)
        raise
