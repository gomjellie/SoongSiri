
# set virtual environment 

$ virtualenv venv -p python3

$ source ./venv/bin/activate

$ pip install -r ./requirements.txt

# run

$ nohup ./run &

# set mongodb environ

https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-16-04

$ sudo systemctl start mongodb

$ sudo systemctl stop mongodb
