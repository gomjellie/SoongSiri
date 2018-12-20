https://jdm.kr/blog/2 참고해서 아래의 라인을 추가한다

0,30 * * * * /home/ubuntu/soongsiri/cron/today.py >> /home/ubuntu/soongsiri/cron/run.py.log 2>&1
0 0,12 * * * /home/ubuntu/soongsiri/cron/tomorrow.py >> /home/ubuntu/soongsiri/cron/run.py.log 2>&1

chmod a+x ./run.py 로 .py의 실행권한 줘야함
