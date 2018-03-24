#!/usr/bin/env sh
# DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

mkdir -p /etc/mosquitto/conf.d/
# cd $(pwd)/mosquitto-auth-plug
cp $(pwd)/mosquitto-auth-plug/auth-plug.so /etc/mosquitto/

# cd ..
# rm -fr mosquitto-auth-plug org.eclipse.mosquitto

cp $(pwd)/auth_plugin.conf /etc/mosquitto/conf.d/auth_plugin.conf
