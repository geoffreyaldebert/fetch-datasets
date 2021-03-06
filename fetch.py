import requests
import sys
from slugify import slugify
import os
import glob
import boto3

r = requests.get(sys.argv[1])
data = r.json()

folder_name = slugify(data['name'])
isExist = os.path.exists('/home/jovyan/work/repo-git'+'/'+folder_name)
if not isExist:
    os.makedirs('/home/jovyan/work/repo-git/'+folder_name)

f = open("/home/jovyan/work/repo-git/intro.md", "w")

f.write('---\ntitle: "Playlist '+data['name']+'"\nabstract: "Nouvelle playlist"\n---')

f.write('\n\nCe notebook a pour objectif de vous aider à commencer votre analyse autour de votre playlist nouvellement créée. Nous avons téléchargé pour vous vos données et nous les avons stockés dans un répertoire minio accessible depuis cet environnement jupyter')
f.write('\n\nD\'abord les imports')
f.write('\n\n```python\nimport os\nimport pandas as pd\nimport boto3\n```')
f.write('\n\nNous nous connectons ensuite au minio pour pouvoir accéder aux données avec le protocole s3')
f.write('\n\n```python\ns3 = boto3.client("s3",endpoint_url = "https://" + os.getenv("AWS_S3_ENDPOINT"),\n    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),\n    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),\n    aws_session_token = os.getenv("AWS_SESSION_TOKEN"))\n```')

resources = []
for d in data['playlist']:
    for r in d['resources']:
        mydict = {}
        mydict['resource_title'] = r['resource_title']
        mydict['resource_id'] = r['resource_id']
        mydict['dataset_id'] = d['dataset_id']
        mydict['dataset_title'] = d['dataset_title']
        resources.append(mydict)

print(resources)

f.write('\n## Exploration')

cpt = 0
for r in resources:
    cpt = cpt + 1
    response = requests.get('https://www.data.gouv.fr/fr/datasets/r/'+r['resource_id'])
    open('/home/jovyan/work/repo-git/'+folder_name+'/'+r['resource_id'], 'wb').write(response.content)
    f.write('\n\n### Jeu de données ['+r['dataset_title']+'](https://www.data.gouv.fr/fr/datasets/'+r['dataset_id']+')')
    f.write('\n\nResource '+r['resource_title'])
    f.write('\n\n```python\nobj = s3.get_object(Bucket="geoffrey", Key="'+folder_name+'/'+r['resource_id']+'")\ndf'+str(cpt)+' = pd.read_csv(obj["Body"])\n```')
    f.write('\n\n```python\ndf'+str(cpt)+'.head()\n```')

f.write('\n\nA vous de jouer')
