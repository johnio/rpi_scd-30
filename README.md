# rpi_scd-30


test sensor: 
python3 test_scd30.py

install redis:
sudo apt-get install redis

install pip requiremnts:
pip3 install requirements.txt

setup config file
/etc/redis/6379.conf:
port              6379
daemonize         yes
save              60 1
bind              127.0.0.1
tcp-keepalive     300
dbfilename        dump.rdb
dir               ./
rdbcompression    yes

run redis:
redis-server /etc/redis/6379.conf

run app:
python3 app.py

access using:
URL:  http://[IP of pi]:8000
