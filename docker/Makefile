# Makefile six

.PHONY: docs clean start build setup

help:
	@echo "setup    - 安装基本依赖(初始化)"
	@echo "fetch    - 更新版本库最新代码"
	@echo "clean    - 清理编译垃圾数据"
	@echo "build    - 编译所需镜像"
	@echo "start    - 开始项目容器"
	@echo "stop     - 停止项目容器"
	@echo "docs     - 构建在线文档"
	@echo "destry   - 销毁项目容器"
	@echo "restart  - 重启项目容器"

destry:
	docker-compose rm -a -f

clean:
	rm -rf project/app

fetch:
	rm -rf project/app && git clone ssh://git@10.7.7.22:10022/sector3/passport.git project/app

build:
	docker build compose/mosquitto -t mosquitto:alpine
	docker build compose/python -t python:alpine
	docker build . -t django:alpine

docs: 
	cd project/app && mkdocs build && cd -

stop: 
	docker-compose stop

start: 
	docker-compose start

setup:
	docker-compose up -d
	docker-compose run --rm django python3 manage.py migrate
	docker-compose run --rm django python3 manage.py loaddata initdb.json
	docker-compose run --rm django python3 manage.py collectstatic --no-input

restart: 
	docker-compose restart

# DO NOT DELETE
