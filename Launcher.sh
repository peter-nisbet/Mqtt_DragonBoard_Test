# !/bin/sh
# Launcher.sh
sudo date +%Y%m%d -s "20180721"
sudo mosquitto -c /etc/mosquitto/conf.d/mosquitto.conf &
sudo python /home/linaro/mqtttest.py &

