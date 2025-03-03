import requests

URL = ""
data = ""

PARAMS = {'data': data}

r = requests.get(url = URL, params = PARAMS)
response = r.json()

_ = response['results'][0]['']['']['']
_ = response['results'][0]['']['']['']

formatted_result = data[''][0]['']