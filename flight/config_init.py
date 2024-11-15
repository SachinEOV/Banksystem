import base64

# [API_Config]
api_version = [b'3.91']
accessmode = "agency"
accessid = "flyondo embarkingonvoyage"
session =  ""
cache_control = "no-cache"
authmode = "pwd"
api_url = "https://stagingxml.ypsilon.net:11024"
content_type = "application/xml"

# [Authorization]
username = "embarkingonvoyage"
password = "a9684c13b7bd14c6ad1acf3c1f83636b"

# Create the Authorization header value by base64 encoding the username and password
auth_value = f"{username}:{password}"
auth_token = base64.b64encode(auth_value.encode('utf-8')).decode('utf-8')  # Base64 encode and decode to string

# The Authorization header value will now be available as a string
authorization_header = f"Basic {auth_token}"
