# https://jdm.kr/blog/2
crontab -e

0,30 * * * * /home/ubuntu/soongsiri/cron/today.py >> /home/ubuntu/soongsiri/cron/today.py.log 2>&1
0 0,12 * * * /home/ubuntu/soongsiri/cron/tomorrow.py >> /home/ubuntu/soongsiri/cron/tomorrow.py.log 2>&1

chmod a+x ./run.py 로 .py의 실행권한 줘야함
