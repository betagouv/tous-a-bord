import os

import sib_api_v3_sdk

from config import settings

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key["api-key"] = os.environ["BREVO_API_KEY"]
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
    sib_api_v3_sdk.ApiClient(configuration)
)


def send_user_creation_email(user_email: str):
    sender_email = "tousabord@beta.gouv.fr"
    sender_name = "Tous à bord"
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


def send_webhook_notification_email(payload: dict):
    send_transac_email(
        sender_email="tousabord@beta.gouv.fr",
        sender_name="Tous à bord",
        to_email="tousabord@beta.gouv.fr"
        if "tous-a-bord.beta.gouv.fr" in settings.HOST_URL
        else "marie.jeammet@beta.gouv.fr",
        subject="Test webhook Tous à Bord !",
        text_content=str(payload),
    )


def send_transac_email(
    sender_email: str, sender_name: str, to_email: str, subject: str, text_content: str
) -> bool:
    try:
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
        print("Exception when sending transac email: %s", e)
        raise
