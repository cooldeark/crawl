# Steps to learn this project

The most important file is the 'set-up.sh', when you want to use this file. You need to input:

```bash
sudo chmod +x set-up.sh
```

Then you will have the access permission to run this shell script.

## Discribe set-up.sh file

- Because we'll install python library in instance, so we can't be the super user to run command. Otherwize your pyenv thing would be install on super use root folder.

- start twse/tpex is the queue, this purpose is make your instance be the worker. When the task is comming then your worker would do the jobs. e.g. 10 tasks comming, you have the 2 workers then will separete the 10 tasks and which finished the task fast then would take next task to do.
It will be like Task "1~10", A worker finished 2,3,7,9,10, B worker finished 1,4,5,6,8.

- Send task is call the producer.py to provide the task to broker(rabbitMQ/redis) then broker distribute the task to workers.

- genenv.py file is for generate the .env file, .env file is for each server to connected config file. genenv.py file depend on local.ini file, before you run the setting dev env please modified local.ini.