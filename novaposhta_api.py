"""
module for working with API from Nova Poshta
"""

import requests


def check_ttn(api_key, ttns):
    url_nova_poshta = 'https://api.novaposhta.ua/v2.0/json/'

    params = {
        "apiKey": api_key,
        "modelName": "TrackingDocument",
        "calledMethod": "getStatusDocuments"
    }
    numbers_list = list(ttns)
    preload_list = []
    result = []
    counter = 0
    # Nova Poshta's API can return information about 100 TTN at once
    # so we must divide list if it more than 100
    while counter < len(numbers_list):
        if numbers_list[counter]:
            preload_list.append({"DocumentNumber": numbers_list[counter], "Phone": ""})
        if counter % 99 == 0 or counter == len(numbers_list) - 1:
            params["methodProperties"] = {"Documents": preload_list}
            resp = requests.post(url=url_nova_poshta, json=params)
            for item in resp.json()["data"]:
                result.append((item["Number"], item["Status"], item["StatusCode"]))
            preload_list.clear()

        counter += 1

    return result


if __name__ == '__main__':
    print("Module must be imported")
