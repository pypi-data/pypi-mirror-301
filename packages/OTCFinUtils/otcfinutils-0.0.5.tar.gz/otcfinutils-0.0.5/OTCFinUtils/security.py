from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from dotenv import load_dotenv
import msal
from os import getenv


def get_client_credential() -> str:
    """
    Retruns the credential needed to get the token for access to the Dataverse.
    """
    load_dotenv()
    VAULT_URL = getenv("VAULT_URL", "")
    SECRET_NAME = getenv("SECRET_NAME", "")

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=VAULT_URL, credential=credential)
    secret_value = client.get_secret(SECRET_NAME).value
    
    if secret_value is None:
        raise RuntimeError("Could not get client credential.")
    
    return secret_value


def get_dataverse_token(dataverse_url: str) -> str:
    """
    Returns the token needed for working with the Dataverse API
    """
    load_dotenv()
    TOKEN_CLIENT_ID = getenv("TOKEN_CLIENT_ID")
    TOKEN_AUTHORITY = getenv("TOKEN_AUTHORITY")
    TOKEN_CLIENT_CREDENTIAL = get_client_credential()

    permissions = f"{dataverse_url}/.default"
    app = msal.ConfidentialClientApplication(
        client_id=TOKEN_CLIENT_ID,
        client_credential=TOKEN_CLIENT_CREDENTIAL,
        authority=TOKEN_AUTHORITY,
    )
    token = app.acquire_token_for_client(scopes=[permissions])
    
    if not isinstance(token, dict) or "access_token" not in token:
        raise RuntimeError(f"Could not get access token for: {dataverse_url}")
    
    return token["access_token"]

# ----------------------------------------

# NOTE: Not complete

def get_graph_token():
    GRAPH_CLIENT_ID = getenv("GRAPH_CLIENT_ID", "")
    GRAPH_TENANT_ID = getenv("GRAPH_TENANT_ID", "")
    GRAPH_MSAL_AUTHORITY = getenv("GRAPH_MSAL_AUTHORITY", "")
    GRAPH_MSAL_SCOPE = getenv("GRAPH_MSAL_SCOPE", "")
    
    # TODO - Add key vault logic for this secret
    GRAPH_CLIENT_SECRET = getenv("GRAPH_CLIENT_SECRET", "")

    msal_app = msal.ConfidentialClientApplication(
        client_id = GRAPH_CLIENT_ID,
        client_credential = GRAPH_CLIENT_SECRET,
        authority = GRAPH_MSAL_AUTHORITY + GRAPH_TENANT_ID,
    )
    result = msal_app.acquire_token_silent(
        scopes = [GRAPH_MSAL_SCOPE],
        account = None,
    )

    if not result:
        result = msal_app.acquire_token_for_client(scopes=[GRAPH_MSAL_SCOPE])

    if not isinstance(result, dict) or "access_token" not in result:
        raise Exception("No Graph Access Token found")
    
    return result["access_token"]

    