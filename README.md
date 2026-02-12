# Simple file storage server with image resampling and REST API

## Installation

### Native Installation

#### System Requirements

* Linux server (preferably Debian or Ubuntu)
* Nginx >= 1.6
* Python >= 3.4
* ImageMagick
* librsvg

**Image Optimizers:**
* jpegtran
* optipng

#### Nginx Configuration

The host configuration should look like this:

```nginx
server {
    listen 80;
    server_name domain.name;
    access_log /path/to/domain.name/storage/logs/nginx.access.log;
    error_log /path/to/domain.name/storage/logs/nginx.error.log;

    location ~* ^.+\.(jpg|jpeg|gif|tif|tiff|png|ico|css|zip|tgz|gz|rar|exe|txt|tar|js|xml)$ {
        root /path/to/domain.name/storage/data/client;
        expires 7d;
    }

    location / {
        include uwsgi_params;
        uwsgi_pass unix:///tmp/owl.uwsgi.sock;
        client_max_body_size 100m;
    }
}
```

#### Owl Setup Steps

1. Create environment and storage directory:

```bash
    virtualenv domain.name
    cd domain.name
    mkdir storage
```

2. Activate the environment:

```bash
    source bin/activate
```

3. Copy repository contents from *src* folder to *storage*

4. Update correct paths in *config/uwsgi.ini* and *owl/settings.py*

5. Install required packages:

```bash
    pip install flask
    pip install uwsgi
    pip install boto3  # for S3-compatible storage support
```

6. Navigate to *storage* directory:

```bash
    cd ./storage
```

7. Create *data* directory:

```bash
    mkdir data
```

8. Start the server:

```bash
    ./scripts/server start
```