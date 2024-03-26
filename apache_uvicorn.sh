#!/bin/bash
# 启动 Uvicorn 服务
sudo pipenv run uvicorn api.main:app --host 0.0.0.0 --port 8888 &

# 启动 Apache 服务
sudo apachectl -D FOREGROUND