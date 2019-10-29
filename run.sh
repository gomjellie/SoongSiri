cp ./soongsiri.service /etc/systemd/system/soongsiri.service
cp ./soongsiri.nginx /etc/nginx/sites-available/soongsiri
ln -s /etc/nginx/sites-available/soongsiri /etc/nginx/sites-enabled

systemctl start soongsiri
systemctl enable soongsiri
# systemctl daemon-reload

service nginx start

