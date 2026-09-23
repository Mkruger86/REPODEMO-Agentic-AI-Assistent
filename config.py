from google.cloud import secretmanager
from agents import set_default_openai_key

PROJECT_ID = "aiagentsinaction"


def configure_openai():
    client = secretmanager.SecretManagerServiceClient()

    secret_name = (
        f"projects/{PROJECT_ID}/secrets/"
        f"OpenAI/versions/1"
    )

    response = client.access_secret_version(
        request={"name": secret_name}
    )

    api_key = response.payload.data.decode("UTF-8")

    set_default_openai_key(api_key)