#!/bin/bash
# 启动 Uvicorn 服务
pipenv run uvicorn api.main:app --host 0.0.0.0 --port 8888 & apachectl -D FOREGROUND