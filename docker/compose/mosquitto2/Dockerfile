FROM alpine:3.7

MAINTAINER Bopo Wang <ibopo@126.com>

# Build-time metadata as defined at http://label-schema.org
RUN apk update && apk upgrade
RUN apk add mosquitto-dev mosquitto supervisor


RUN mkdir -p /mqtt/config /mqtt/data /mqtt/log
COPY config /mqtt/config
RUN chown -R mosquitto:mosquitto /mqtt
VOLUME ["/mqtt/config", "/mqtt/data", "/mqtt/log"]


EXPOSE 1883 9001

ADD docker-entrypoint.sh /usr/bin/

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["/usr/sbin/mosquitto", "-c", "/mqtt/config/mosquitto.conf"]
