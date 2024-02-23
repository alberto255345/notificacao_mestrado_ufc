from google.cloud import secretmanager
import json

def get_json_secret(project_id, secret_name):
    client = secretmanager.SecretsManagerClient()
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_version(request={"name": name})
    print(f"Response: {response}")
    
    decoded_value = response.payload.data.decode("UTF-8")
    return json.loads(decoded_value) if isinstance(decoded_value, str) else None