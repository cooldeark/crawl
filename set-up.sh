#!/bin/bash

# 这行使得脚本在执行过程中如果遇到任何错误（任何命令返回非零值）就立即退出。这有助于避免错误累积，确保脚本的正确性。
set -e

COLEARN_WEB_DOMAIN="${COLEARN_WEB_DOMAIN:=unset}"
INSTALL_ROOT="/opt/crawl"

# Check script is run with sudo
if [[ $EUID -ne 0 ]]; then
	echo "This script must be run with sudo or as root"
	exit 1
fi

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

function install_python_dependencies () {
    sudo apt-get install curl git bzip2 -y
    sudo curl https://pyenv.run | bash -y
    sudo echo 'export LC_ALL=C.UTF-8' >> ~/.bashrc
    sudo echo 'export LANG=C.UTF-8' >> ~/.bashrc
    sudo echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    sudo echo 'export PATH="$PYENV_ROOT/shims:$PATH"' >> ~/.bashrc
    sudo echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    sudo echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bashrc
    exec $SHELL

    pyenv install miniconda3-4.3.30 -y
    pyenv global miniconda3-4.3.30 -y
    pip install pipenv -y
    pipenv install flask==2.0.1 -y
    pipenv --python ~/.pyenv/versions/miniconda3-4.3.30/bin/python -y
    pip install docker-compose pipenv
    # sync這個會去尋找pipfile.lock把相關library都去載好
    pipenv sync
}


function create_docker_container () {
    sudo docker compose -f mysql.yml up -d
    sudo docker compose -f rabbitmq.yml up -d
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

function send_task () {
    pipenv run python financialdata/producer.py taiwan_stock_price 2021-04-01 2021-04-12
}

function setting_dev_env () {
    python genenv.py
}

function menu() {
	echo # 空行 增加可讀信
	echo # 空行 增加可讀信
	echo -ne "1) Install Docker
2) Install Python dependencies
3) Create Docker Container services (mysql, rabbitMQ)
4) start twse queue
5) start tpex queue
6) send task
7) setting dev env
i) Auto Run Everything
w) restart all docker container
r) reboot
q) quit
Choose what to do: "
	read choice # 把使用者輸入的值存在choice裡面
	echo # 空行 增加可讀信
    # shell 的 case func，就是用) 去當php switch case "1" : 的意思
	case $choice in
		1) install_docker ; menu ;;
		2) install_python_dependencies ; menu ;;
        3) create_docker_container ; menu ;;
        4) start_twse_queue ; menu ;;
        5) start_tpex_queue ; menu ;;
        6) send_task ; menu ;;
        7) setting_dev_env ; menu ;;
		"i") install_docker ; install_python_dependencies ; create_docker_container ; menu ;;
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