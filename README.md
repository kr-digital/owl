# Установка

## Установка через docker

```
    docker run -d --name owl -p 8089:80 -v /path/to/owl_data:/var/data -e "APP_CLIENT=client" -e "APP_TOKEN=secret" gitlab.kr.digital:4567/kr/owl:latest
```

## Установка через docker-compose


Создаём файл `docker-compose.yml`:
```
version: '3.4'

services:
  owl:
    restart: always
    image: gitlab.kr.digital:4567/kr/owl:latest
    ports:
      - "8089:80"
    volumes:
      - /path/to/owl_data:/var/data
    environment:
      - APP_CLIENT=client
      - APP_TOKEN=secret

```

Запуск: `docker-compose up -d`

Останов: `docker-compose stop`

## Нативная установка

### Системные требования

* Linux-сервер (предпочтительно Debian или Ubuntu)
* Nginx >=1.6
* Python >=3.4
* Imagemagick
* Librsvg
  
Оптимизаторы изображений:
* jpegtran
* optipng

### Nginx

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

### Owl

1. Создаем среду, папку под хранилище

		virtualenv domain.name
		cd domain.name
		mkdir storage

2. Активируем среду

		source bin/activate

3. Копируем в папку *storage* содержимое папки *src* репозитория
4. Прописываем верные пути в файле конфигурации *config/uwsgi.ini* и *owl/settings.py*
5. Устанавливаем flask и uwsgi

		pip install flask
		pip install uwsgi
		pip install boto3 #для работы с S3-совместимым хранилищем
		
6. Переходим в папку *storage*
		
		cd ./storage
		
7. Создаём папку *data*

		mkdir data

8. Запускаем сервер

		./scripts/server start