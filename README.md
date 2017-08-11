
# What is Soongsiri?

숭실대학교 학식(학생 식당), 교식(교직원 식당), 기식(기숙사), 푸트코트의 학식 정보를 카카오톡으로 제공하는 카카오톡 학식 봇입니다.

# 서비스를 이용하는 법

모바일에서 [http://pf.kakao.com/_EMxkxgd](http://pf.kakao.com/_EMxkxgd) 링크를 통해 친구추가 하거나, 플러스친구 검색에서 `숭실대 학식` 을 검색해서 친구추가 합니다.

# branch 관리

http://nvie.com/posts/a-successful-git-branching-model/

http://ohgyun.com/402

master는 http://pf.kakao.com/_EMxkxgd

develop은 http://pf.kakao.com/_nPclxl 같은 아마존 서버에서 포트만 바꿔서 테스트

테스트 충분히 하고 develop -> master

# 서버 설정들(까먹는 나를위해)
## set virtual environment

```bash
virtualenv venv -p python3

source ./venv/bin/activate

pip install -r ./requirements.txt
```
## run
```bash
nohup ./run &
```
## set mongodb environ

https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-16-04
```bash
sudo systemctl start mongodb

sudo systemctl stop mongodb
```

## set time-zone

```bash
tzselect
```
