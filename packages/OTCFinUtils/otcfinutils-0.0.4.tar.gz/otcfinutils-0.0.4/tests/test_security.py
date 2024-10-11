from OTCFinUtils.security import get_dataverse_token

url = "https://org873d3f04.crm.dynamics.com/"
token = get_dataverse_token(url)
print(token)