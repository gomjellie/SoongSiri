#!/home/ubuntu/soongsiri/venv/bin/python
import requests

res = requests.get("https://ssu.life/soongsiri/refresh")
print(res.status_code)
