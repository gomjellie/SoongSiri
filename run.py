#!venv/bin/python
from app import app
app.run(port=9091, host='0.0.0.0', debug=True)
