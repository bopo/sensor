#!/usr/bin/env sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# sudo apt-get install mosquitto libssl-dev libmosquitto-dev libcurl4-openssl-dev -y
apk add --no-cache --virtual .build-deps curl-dev openssl-dev gcc g++ automake autoconf make git
apk del .fetch-deps

git clone http://git.eclipse.org/gitroot/mosquitto/org.eclipse.mosquitto.git
git clone https://github.com/jpmens/mosquitto-auth-plug.git

cp $DIR/config.mk mosquitto-auth-plug/config.mk
cd mosquitto-auth-plug

make

cd -

mkdir -p /etc/mosquitto/conf.d/
# cd $(pwd)/mosquitto-auth-plug
cp $(pwd)/mosquitto-auth-plug/auth-plug.so /etc/mosquitto/

# cd ..
# rm -fr mosquitto-auth-plug org.eclipse.mosquitto

cp $(pwd)/auth_plugin.conf /etc/mosquitto/conf.d/auth_plugin.conf
