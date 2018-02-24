
# What is Soongsiri?

숭실대학교 식단, 도서관 열람실, 근처 교통정보를 카카오톡으로 제공하는 카카오톡 채팅봇입니다.

식단지원 리스트는 다음과 같습니다:

학식(학생 식당), 교식(교직원 식당), 기식(기숙사), 푸트코트의 학식

식단정보를 보여줄 뿐만아니라 별점을 매겨서 다른 학우의 선택을 도울 수 있습니다.



# 서비스를 이용하는 법

모바일에서 [http://pf.kakao.com/_EMxkxgd](http://pf.kakao.com/_EMxkxgd) 링크를 통해 친구추가 하거나, 플러스친구 검색에서 `숭실대 학식` 을 검색해서 친구추가 합니다.

## install dependencies
```bash
virtualenv venv -p python3

source ./venv/bin/activate

pip install -r ./requirements.txt
```

## set time-zone

```bash
tzselect
```


## set mongodb environ

https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-16-04

```bash
sudo systemctl start mongodb

sudo systemctl stop mongodb
```

## setup

```bash

cp ./soongsiri.service /etc/systemd/system/soongsiri.service
cp ./soongsiri.nginx /etc/nginx/sites-available/soongsiri
ln -s /etc/nginx/sites-available/soongsiri /etc/nginx/sites-enabled

```


## start

```bash

systemctl start soongsiri
systemctl enable soongsiri
# systemctl daemon-reload

service nginx start
```

