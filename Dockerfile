# 現在此份dockerfile尚未完整 怪怪的

FROM ubuntu:20.04
MAINTAINER JamesLin

RUN mkdir -p /opt/crawl
# 設定進入docker的預設工作目錄
WORKDIR /opt/crawl
COPY ./ /opt/crawl

# 系統升級、安裝 python
RUN apt-get update && apt-get install python3.6 -y && apt-get install python3-pip -y
RUN apt install curl git bzip2 -y
RUN curl https://pyenv.run | bash

# 设置环境变量
ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PYENV_ROOT=/root/.pyenv

# 将 Pyenv 相关的路径添加到 PATH 环境变量
ENV PATH=$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

# 安装 Pyenv 并初始化
RUN apt-get update && apt-get install -y git \
    && git clone https://github.com/pyenv/pyenv.git $PYENV_ROOT \
    && echo 'if command -v pyenv 1>/dev/null 2>&1; then eval "$(pyenv init -)"; fi' >> ~/.bashrc


# install package
# RUN pip3 install pipenv==2020.6.2
# genenv


# RUN echo 'export LC_ALL=C.UTF-8' >> ~/.bashrc
# RUN echo 'export LANG=C.UTF-8' >> ~/.bashrc
# RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
# RUN echo 'export PATH="$PYENV_ROOT/shims:$PATH"' >> ~/.bashrc
# RUN echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
# RUN echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bashrc
# RUN exec $SHELL

# RUN echo 'export LC_ALL=C.UTF-8' >> ~/.bashrc
# RUN echo 'export LANG=C.UTF-8' >> ~/.bashrc
# RUN echo 'export PYENV_ROOT=\"\$HOME\/\.pyenv\"' >> ~/.bashrc
# RUN echo 'export PATH=\"\$PYENV_ROOT\/shims\:\$PATH\"' >> ~/.bashrc
# RUN echo 'export PATH=\"\$PYENV_ROOT\/bin\:$PATH\"' >> ~/.bashrc
# RUN echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bashrc
# RUN exec $SHELL

RUN pyenv install miniconda3-4.3.30
RUN pyenv global miniconda3-4.3.30
RUN pip install pipenv
RUN pipenv install flask==2.0.1
RUN pipenv --python ~/.pyenv/versions/miniconda3-4.3.30/bin/python
RUN pip install docker-compose pipenv
RUN pipenv install mysql-connector-python==8.0.28
RUN pipenv install apscheduler
RUN pipenv sync
RUN python genenv.py
# 下面是讓虛擬環境跑起來
# RUN pipenv run python



# 安装依赖
# RUN pip install --no-cache-dir -r requirements.txt

# 默认执行爬虫程序
# CMD ["python", "main.py"]