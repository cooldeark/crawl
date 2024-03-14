FROM ubuntu:20.04
MAINTAINER JamesLin

# 系統升級、安裝 python
RUN apt-get update && apt-get install python3.6 -y && apt-get install python3-pip -y
RUN apt install curl git bzip2 -y
RUN curl https://pyenv.run | bash

# 設置環境變量
ENV PYENV_ROOT="/root/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PATH"
ENV PATH="$PYENV_ROOT/shims:$PATH"
ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8
RUN echo 'if command -v pyenv 1>/dev/null 2>&1; then eval "$(pyenv init -)"; fi' >> ~/.bashrc

RUN mkdir -p /opt/crawl
# 設定進入docker的預設工作目錄
COPY ./ /opt/crawl
WORKDIR /opt/crawl

# install package
RUN pip3 install pipenv==2020.6.2
RUN pyenv install miniconda3-4.3.30
RUN pyenv global miniconda3-4.3.30
RUN pip install pipenv
RUN pipenv install flask==2.0.1
RUN pipenv --python ~/.pyenv/versions/miniconda3-4.3.30/bin/python
RUN pip install docker-compose pipenv
RUN pipenv install mysql-connector-python==8.0.28
RUN pipenv install apscheduler
RUN pipenv sync
