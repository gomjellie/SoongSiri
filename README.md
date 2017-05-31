
# set virtual environment 

$ virtualenv venv -p python3

$ source ./venv/bin/activate

$ pip install -r ./requirements.txt

# to connect to AWS 

$ ssh -i seoul-soongsiri.pem ubuntu@ec2-52-79-131-30.ap-northeast-2.compute.amazonaws.com

# run

$ nohup ./run &


