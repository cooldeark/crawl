# 使用官方Python镜像作为基础镜像
FROM python:3.8-slim
MAINTAINER JamesLin

RUN mkdir -p /opt/crawl
# 設定進入docker的預設工作目錄
WORKDIR /opt/crawl
COPY ./ /opt/crawl

RUN apt-get update -y
RUN apt install curl git bzip2 -y
RUN curl https://pyenv.run | bash

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 默认执行爬虫程序
CMD ["python", "main.py"]