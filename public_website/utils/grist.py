import requests

base_url = "https://grist.incubateur.net/api/docs/tp4ZSGyfvqHd"


def get_communes():
    response = requests.get(f"{base_url}/tables/Familles_summary_COMMUNE/records")
    return response.json()


def build_csv(commune):
    url = f'{base_url}/download/csv?viewSection=7&tableId=Individus&activeSortSpec=[]&filters=[{{"colRef":23,"filter":"{{\\"included\\":[\\"{commune}\\"]}}"}}]&linkingFilter={{"filters":{{}},"operations":{{}}}}'
    response = requests.get(url)
    return response.text


def build_dataset(commune):
    f_response = requests.get(
        f'{base_url}/tables/Familles/records?filter={{"COMMUNE":["{commune}"]}}'
    )
    f_data = f_response.json()

    i_response = requests.get(
        f'{base_url}/tables/Individus/records?filter={{"COMMUNE_famille_":["{commune}"]}}'
    )
    i_data = i_response.json()

    fs = {fs["id"]: fs["fields"] for fs in f_data["records"]}
    return [
        {"id": i["id"], "fields": {**i["fields"], **fs[i["fields"]["FAMILLE"]]}}
        for i in i_data["records"]
    ]
