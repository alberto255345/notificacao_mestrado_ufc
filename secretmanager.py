from google.cloud import secretmanager
import json

def get_json_secret(project_id, secret_name):
    print(f"Project ID: {project_id}")
    print(f"Secret Name: {secret_name}")
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    print(f"Name: {name}")
    response = client.access_secret_version(request={"name": name})
    # response = client.access_secret_version(request={"name": version.name})
    print(f"Response: {response}")
    
    decoded_value = response.payload.data.decode("UTF-8")
    return json.loads(decoded_value) if isinstance(decoded_value, str) else None