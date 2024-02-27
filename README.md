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

## Discribe cralwer flow

Run command below will asking worker to work. Let's explain how the flow worked.

```bash
pipenv run python financialdata/producer.py taiwan_stock_price 2021-04-01 2021-04-12
```

- Excuted producer.py, in producer.py will to import financialdata/crawler/taiwan_stock_price.py and running function gen_task_paramter_list which in taiwan_stock_price.py.

- In taiwan_stock_price.py the gen_task_paramter_list func is to return date list.

- When producer.py get the date list will running the import file financialdata/tasks/task.py crawler funcion.

- When task.py excute crawler function will import financialdata/crawler/taiwan_stock_price.py crawler function.

- So the crawl flow would be like : producer.py -> taiwan_stock_price.py gen_task_paramter_list -> task.py crawler -> taiwan_stock_price.py crawler -> producer.py (finished)