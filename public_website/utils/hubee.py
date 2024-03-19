import json
import os

import requests
from requests.auth import HTTPBasicAuth


def get_token(scope):
    credentials = HTTPBasicAuth(
        os.getenv(f"{scope}_HUBEE_CLIENT_ID"), os.getenv(f"{scope}_HUBEE_CLIENT_SECRET")
    )
    data = {"grant_type": "client_credentials", "scope": scope}
    headers = {"content-type": "application/json"}
    url = os.getenv("HUBEE_AUTH_TOKEN_URL")
    res = requests.post(url, data=json.dumps(data), headers=headers, auth=credentials)
    return res.json()


def send(company_register, branch_code, filename, token):
    headers = get_headers(token)

    folder_request = build_folder_request(
        company_register, branch_code, filename, token
    )
    url = build_url("/teledossiers/v1/folders")
    print(folder_request)
    folder = requests.post(url, data=json.dumps(folder_request), headers=headers).json()

    print(folder)

    with open(filename, "rb") as f:
        url = build_url(
            "/teledossiers/v1/folders/{}/attachments/{}".format(
                folder["id"], folder["attachments"][0]["id"]
            )
        )
        requests.put(
            url, f.read(), headers=get_headers(token, "application/octet-stream")
        )

    url = build_url("/teledossiers/v1/folders/{}".format(folder["id"]))
    payload = {"globalStatus": "HUBEE_COMPLETED"}
    requests.patch(url, json.dumps(payload), headers=headers)

    return folder


def get_notifications(token):
    headers = get_headers(token)
    url = build_url("/teledossiers/v1/notifications")
    return requests.get(url, headers=headers).json()


def delete_notification(notification_id, token):
    headers = get_headers(token)
    url = build_url("/teledossiers/v1/notifications/{}".format(notification_id))
    return requests.delete(url, headers=headers)


def get_case(case_id, token):
    headers = get_headers(token)
    url = build_url("/teledossiers/v1/cases/{}".format(case_id))
    return requests.get(url, headers=headers).json()


def patch_case(case_id, payload, token):
    headers = get_headers(token)
    url = build_url("/teledossiers/v1/cases/{}".format(case_id))
    return requests.patch(url, json.dumps(payload), headers=headers)


def get_attachment(case_id, attachment_id, token):
    headers = get_headers(token)
    url = build_url(
        "/teledossiers/v1/cases/{}/attachments/{}".format(case_id, attachment_id)
    )
    return requests.get(url, headers=headers)


def build_folder_request(company_register, branch_code, filename, token):
    size = os.path.getsize(filename)
    return {
        "applicant": {"firstName": "firstName", "lastName": "lastName"},
        "attachments": [
            {
                "fileName": "documents.zip",
                "mimeType": "application/zip",
                "recipients": [
                    f'{os.getenv("OSL_EXTERNAL_ID", "DEMO_TAB")}_case',
                ],
                "size": size,
                "type": "documents",
            }
        ],
        "cases": [
            {
                "externalId": f'{os.getenv("OSL_EXTERNAL_ID", "DEMO_TAB")}_case',
                "recipient": {
                    "branchCode": branch_code,
                    "companyRegister": company_register,
                    "type": "SI",
                },
            }
        ],
        "externalId": f'{os.getenv("OSL_EXTERNAL_ID", "DEMO_TAB")}_folder',
        "processCode": os.getenv("OSL_PROCESS_CODE"),
    }


def get_headers(token, content_type="application/json"):
    return {
        "Authorization": "Bearer " + token["access_token"],
        "Content-Type": content_type,
    }


def build_url(ressource):
    return "{}{}".format(os.getenv("HUBEE_BASE_URL"), ressource)
