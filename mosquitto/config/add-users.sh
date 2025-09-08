#bin/bash

if [ ! -f /mosquitto/config/passwd ]; then
    touch /mosquitto/config/passwd &&
    mosquitto_passwd -b /mosquitto/config/passwd user senai &&
    mosquitto_passwd -b /mosquitto/config/passwd user2 senai;
fi &&
    chmod 0700 /mosquitto/config/passwd &&
    mosquitto -c /mosquitto/config/mosquitto.conf 