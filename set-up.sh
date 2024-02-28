#!/bin/bash

# 这行使得脚本在执行过程中如果遇到任何错误（任何命令返回非零值）就立即退出。这有助于避免错误累积，确保脚本的正确性。
set -e

# COLEARN_WEB_DOMAIN="${COLEARN_WEB_DOMAIN:=unset}"
INSTALL_ROOT="/opt/crawl"

# Check script is run with sudo
# 這裡不能用sudo去安裝，因為會出問題
# if [[ $EUID -ne 0 ]]; then
# 	echo "This script must be run with sudo or as root"
# 	exit 1
# fi

# Check location of install
cd $INSTALL_ROOT
if [ $? -ne 0 ]; then
	echo "$INSTALL_ROOT not found"
	exit 1
fi
echo "Install root will be $INSTALL_ROOT"

# Load .shellEnv file
# wait until all know then do the env file
# if [ -f ".shellEnv" ]; then
# 	set -o allexport
# 	source .shellEnv
# 	set +o allexport
# fi


function install_docker() {

    sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common -y

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

    sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"

    sudo apt-get install docker.io -y

    sudo apt-get install docker-compose-plugin

    echo "Finished"

}

function install_python_env_params () {
    # 獲取當前用戶名
    CURRENT_USER=$(whoami)

    # 獲取當前用戶的主群組
    CURRENT_GROUP=$(id -gn $CURRENT_USER)

    # 將 /opt/crawl 資料夾及其內容的所有者更改為當前用戶和群組
    sudo chown -R $CURRENT_USER:$CURRENT_GROUP /opt/crawl

    sudo apt-get install curl git bzip2 -y

    if find /home -type d -name ".pyenv" | grep -q '.'; then
        echo "警告：無法繼續安裝。請先移除找到的 '.pyenv' 目錄，跑curl https://pyenv.run | bash 去找到目錄"
        exit 1  # 以錯誤代碼退出腳本
    else
        curl https://pyenv.run | bash
    fi

     # 下面沒[]是因為，grep不能當作命令使用，反正[]是命令的意思，grep不能被包起來
    if ! grep -q 'PYENV_ROOT' ~/.bashrc; then
        # 如果 /etc/crontab 中不包含 /opt/colearn/dessert，则执行指令
        sudo echo 'export LC_ALL=C.UTF-8' >> ~/.bashrc
        sudo echo 'export LANG=C.UTF-8' >> ~/.bashrc
        sudo echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
        sudo echo 'export PATH="$PYENV_ROOT/shims:$PATH"' >> ~/.bashrc
        sudo echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
        sudo echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bashrc
        # pyenv install pypy3.8-7.3.10
        # pyenv global pypy3.8-7.3.10
    else
        echo "Already set up!"
    fi
    echo "set up python params finished"
    exec $SHELL
}

function install_python_library () {
    # python version 3.6.3
    # pyenv install miniconda3-4.3.30
    pyenv install miniconda3-4.7.10
    echo 'Finished install miniconda3'
    # pyenv global miniconda3-4.3.30
    pyenv global miniconda3-4.7.10
    echo 'Finished set global miniconda3'
    pip install pipenv
    # pipenv --python 3.8
    echo 'Finished install pipenv'
    pipenv install flask==2.0.1
    echo 'Finished install flask'
    # pipenv --python ~/.pyenv/versions/miniconda3-4.3.30/bin/python
    pipenv --python ~/.pyenv/versions/miniconda3-4.7.10/bin/python
    echo 'Finished binding path'
    pip install docker-compose pipenv
    echo 'Finished install docker compose pipenv'
    pipenv install mysql-connector-python
    echo 'Finished install mysql pipenv'

    # pipenv install line-bot-sdk
    # echo 'Finished install line-bot-sdk'

    # sync這個會去尋找pipfile.lock把相關library都去載好
    pipenv sync
    echo 'Finished All'
}


function create_docker_container () {
    sudo docker compose -f mysql.yml up -d
    echo 'Finished mysql'
    sudo docker compose -f rabbitmq.yml up -d
    echo 'Finished rabbitMQ'
}

function restart_all_docker_container () {
    sudo docker restart crawl_mysql
    sudo docker restart crawl_phpmyadmin
    sudo docker restart crawl_rabbitMQ
    sudo docker restart crawl_flower
}

function start_twse_queue () {
    pipenv run celery -A financialdata.tasks.worker worker --loglevel=info --concurrency=1  --hostname=%h -Q twse
}

function start_tpex_queue () {
    pipenv run celery -A financialdata.tasks.worker worker --loglevel=info --concurrency=1  --hostname=%h -Q tpex
}

function send_test_task () {
    pipenv run python financialdata/producer.py taiwan_stock_price 2021-04-01 2021-04-12
}

function send_ptt_task () {
    pipenv run python financialdata/producer.py ptt_crawl none none
}

function start_ptt_queue () {
    pipenv run celery -A financialdata.tasks.worker worker --loglevel=info --concurrency=1  --hostname=%h -Q pttCrawler
}

function setting_dev_env () {
    python genenv.py
}

function setting_staging_env () {
    VERSION=STAGING python genenv.py
}

function setting_prod_env () {
    VERSION=RELEASE python genenv.py
}

function menu() {
	echo # 空行 增加可讀信
	echo # 空行 增加可讀信
	echo -ne "1) Install Docker
2) Install Python dependencies
3) Install Python Library
4) Create Docker Container services (mysql, rabbitMQ)
5) setting dev env(Need to modified local.ini then run this job)
6) start twse queue (Be the worker to work)
7) start tpex queue (Be the worker to work)
8) Send Stock Task (Will asking worker to work, but if no worker would save this job until woker work)
9) setting staging env(Need to modified local.ini then run this job)
10) setting prod env(Need to modified local.ini then run this job)
11) Send ptt task
12) Start queue of ptt
i) Auto Run Everything (Only 1 ~ 2)
w) restart all docker container
r) reboot
q) quit
Choose what to do: "
	read choice # 把使用者輸入的值存在choice裡面
	echo # 空行 增加可讀信
    # shell 的 case func，就是用) 去當php switch case "1" : 的意思
	case $choice in
		1) install_docker ; menu ;;
		2) install_python_env_params ; menu ;;
        3) install_python_library ; menu ;;
        4) create_docker_container ; menu ;;
        5) setting_dev_env ; menu ;;
        6) start_twse_queue ; menu ;;
        7) start_tpex_queue ; menu ;;
        8) send_test_task ; menu ;;
        9) setting_staging_env ; menu ;;
        10) setting_prod_env ; menu ;;
        11) send_ptt_task ; menu ;;
        12) start_ptt_queue ; menu ;;
		"i") install_docker ; install_python_env_params ; create_docker_container ; menu ;;
		"w") restart_all_docker_container ; menu ;;
		"q") exit 0; ;;
		"r") reboot; ;;
	esac # 关闭 case 语句
}


if [ $# -gt 0 ]; then
	for func in $@; do
		$func;
        # $? 获取上一条命令的退出状态并将其赋给变量 RC
		RC=$?
		if [ $RC -ne 0 ]; then
			echo "$func returned $RC. Exiting."
			exit $RC
		fi
	done
	echo "$@ - completed successfully"
	exit 0
fi


# 因為給予1，如果没有命令行参数传入，脚本进入一个无限循环
while [ 1 ]; do
	menu
done