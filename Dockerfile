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

RUN echo 'export LC_ALL=C.UTF-8' >> ~/.bashrc
RUN echo 'export LANG=C.UTF-8' >> ~/.bashrc
RUN echo 'export PYENV_ROOT=\"\$HOME\/\.pyenv\"' >> ~/.bashrc
RUN echo 'export PATH=\"\$PYENV_ROOT\/shims\:\$PATH\"' >> ~/.bashrc
RUN echo 'export PATH=\"\$PYENV_ROOT\/bin\:$PATH\"' >> ~/.bashrc
RUN echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bashrc
RUN exec $SHELL

RUN pyenv install miniconda3-4.3.30 -y
RUN pyenv global miniconda3-4.3.30 -y
RUN pip install pipenv -y
RUN pipenv install flask==2.0.1 -y
RUN pipenv --python ~/.pyenv/versions/miniconda3-4.3.30/bin/python -y
# 下面是讓虛擬環境跑起來
RUN pipenv run python



# 安装依赖
# RUN pip install --no-cache-dir -r requirements.txt

# 默认执行爬虫程序
# CMD ["python", "main.py"]