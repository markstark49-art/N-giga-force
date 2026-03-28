import requests

url = "http://localhost:5000/upload"
files = {'file': open('agents/swarm/evolution_history.md', 'rb')}
r = requests.post(url, files=files)
print(r.text)
