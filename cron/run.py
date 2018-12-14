#!/home/ubuntu/soongsiri/venv/bin/python
import requests

res = requests.get("https://ssu.life/refresh")
print(res.status_code)
