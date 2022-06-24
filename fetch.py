import requests
import sys

r = requests.get(sys.argv[1])
data = r.json()

resources = []
for d in data['playlist']:
    r = requests.get('https://www.data.gouv.fr/api/1/datasets/'+d['id'])
    res = r.json()
    for r in res['resources']:
        mydict = {}
        mydict['resource_title'] = r['title']
        mydict['resource_id'] = r['id']
        mydict['dataset_id'] = d['id']
        mydict['dataset_title'] = d['name']
        resources.append(mydict)

print(resources)

for r in resources:
    response = requests.get('https://www.data.gouv.fr/fr/datasets/r/'+r['resource_id'])
    open('./data/'+r['resource_title'], 'wb').write(response.content)