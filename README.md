# Установка

## Системные требования

* Linux-сервер (предпочтительно Debian или Ubuntu)
* Nginx >=1.6
* Python >=3.4
* Imagemagick
* Librsvg
  
Оптимизаторы изображений:
* jpegtran
* optipng

## Nginx

Конфигурация хоста должна выглядеть так:

	server {
    	listen	80;
    	server_name	domain.name;
    	access_log	/path/to/domain.name/storage/logs/nginx.access.log;
    	error_log	/path/to/domain.name/storage/logs/nginx.error.log;

    	location ~* ^.+\.(jpg|jpeg|gif|tif|tiff|png|ico|css|zip|tgz|gz|rar|exe|txt|tar|js|xml)$ {
    		root	/path/to/domain.name/storage/data/client;
    		expires	7d;
    	}

    	location / {
    		include uwsgi_params;
    		uwsgi_pass unix:///tmp/owl.uwsgi.sock;
    		client_max_body_size	100m;
    	}
    }

## Owl

1. Полуачаем репозиторий

		git clone git@git.k-r-w.ru:OwlStorage.git


2. Создаем среду, папку под хранилище

		virtualenv domain.name
		cd domain.name
		mkdir storage

3. Активируем среду

		source bin/activate

4. Копируем в папку *storage* содержимое папки *src* репозитория
5. Прописываем верные пути в файле конфигурации *config/uwsgi.ini* и *owl/settings.py*
6. Устанавливаем flask и uwsgi

		pip install flask
		pip install uwsgi
		pip install boto3 #для работы с S3-совместимым хранилищем
		
7. Переходим в папку *storage*
		
		cd ./storage
		
8. Создаём папку *data*

		mkdir data

9. Запускаем сервер

		./scripts/server start