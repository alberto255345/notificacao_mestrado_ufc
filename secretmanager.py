from google.cloud import secretmanager
import json

def get_json_secret(project_id, secret_name):
    client = secretmanager.SecretManagerServiceClient()
    name = client.secret_version_path(project_id,secret_name,'latest')
    response = client.access_secret_version(name) 
    payload = response.payload.data.decode('UTF-8')
    return json.loads(payload) if isinstance(payload, str) else None