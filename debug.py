import json

response = json.loads('{"type":"obstacle","middle":"464","left":"2193","right":"467"}')
print(response["middle"])

