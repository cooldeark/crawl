#!/bin/bash

# 这行使得脚本在执行过程中如果遇到任何错误（任何命令返回非零值）就立即退出。这有助于避免错误累积，确保脚本的正确性。
set -e

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