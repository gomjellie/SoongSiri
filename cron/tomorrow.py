#!/home/ubuntu/soongsiri/venv/bin/python
import requests

res = requests.get("https://ssu.life/refresh_tomorrow")
print(res.status_code)
