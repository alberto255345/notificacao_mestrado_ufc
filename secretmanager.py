from google.cloud import secretmanager
import json

def get_json_secret(project_id, secret_name):
    print(f"Project ID: {project_id}")
    print(f"Secret Name: {secret_name}")
     # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"

    # Get the secret version.
    response = client.get_secret_version(request={"name": name})

    # Print information about the secret version.
    state = response.state.name
    print(f"Got secret version {response.name} with state {state}")
    # [END secretmanager_get_secret_version]
    
    decoded_value = response
    # decoded_value = response.payload.data.decode("UTF-8")
    print(decoded_value)
    return json.loads(decoded_value) if isinstance(decoded_value, str) else None