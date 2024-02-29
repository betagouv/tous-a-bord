import requests

base_url = "https://grist.incubateur.net/api/docs/tp4ZSGyfvqHd/tables"


def get_communes():
    response = requests.get(f"{base_url}/Familles_summary_COMMUNE/records")
    return response.json()


def build_dataset(commune):
    f_response = requests.get(
        f'{base_url}/Familles/records?filter={{"COMMUNE":["{commune}"]}}'
    )
    f_data = f_response.json()

    i_response = requests.get(
        f'{base_url}/Individus/records?filter={{"COMMUNE_famille_":["{commune}"]}}'
    )
    i_data = i_response.json()

    fs = {fs["id"]: fs["fields"] for fs in f_data["records"]}
    return [
        {"id": i["id"], "fields": {**i["fields"], **fs[i["fields"]["FAMILLE"]]}}
        for i in i_data["records"]
    ]
