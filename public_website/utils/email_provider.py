import os
import sib_api_v3_sdk

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key["api-key"] = os.environ["SEND_IN_BLUE_API_KEY"]

def send_user_creation_email(user_email:str):
    sender_email="tousabord@beta.gouv.fr"
    sender_name="Tous à bord"
    to_email="tousabord@beta.gouv.fr"
    subject = "Un nouvel utilisateur a été créé"
    text_content = "L'utilisateur "+user_email+" vient de se créer un compte sur la plateforme."
    try:
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )
        to=[sib_api_v3_sdk.SendSmtpEmailTo(to_email)]
        sender=sib_api_v3_sdk.SendSmtpEmailSender(name=sender_name, email=sender_email)
        email = sib_api_v3_sdk.SendSmtpEmail(sender=sender, to=to, text_content=text_content, subject=subject)
        api_instance.send_transac_email(email)
        return True
    except sib_api_v3_sdk.rest.ApiException as e:
        print("Exception when calling ContactsApi->create_contact: %s", e)
        raise

