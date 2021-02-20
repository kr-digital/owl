import os

# Owl settings here
DEBUG = False

# List of clients tokens
CLIENTS = {}
CLIENTS[os.environ['APP_CLIENT']] = os.environ['APP_TOKEN']

# Output data format
FORMAT = 'JSON'

# Storage engine
STORAGE_ENGINE = 'local'
STORAGE_NAMING_STRATEGY = 'uuid'
STORAGE_ENGINE_LOCAL_DATA_PATH = '/var/data'
STORAGE_ENGINE_LOCAL_DATA_PATH_STRATEGY = 'single_dir'
STORAGE_ENGINE_S3_ENDPOINT_URL = 'https://storage.yandexcloud.net'
STORAGE_PROCESS_ORIGINALS_FILTER = 'w1920h1080'

# Storage image operator
STORAGE_IMAGE_OPERATOR = 'imagemagick'
STORAGE_IMAGE_OPERATOR_CONVERT_PATH = 'convert'
STORAGE_IMAGE_OPERATOR_COMPOSE_PATH = 'composite'
STORAGE_IMAGE_OPERATOR_IDENTIFY_PATH = 'identify'

# Storage vector graphic operator
STORAGE_VECTOR_OPERATOR = 'librsvg'
STORAGE_VECTOR_OPERATOR_CONVERT_PATH = 'rsvg-convert'

# Storage options
STORAGE_WORKERS = 2
ALLOWED_EXTENSIONS = {
    'binary': ['txt', 'pdf', 'doc', 'avi', 'mp4', 'csv', 'docx', 'xlsx', 'xls'],
    'raster': ['png', 'jpg', 'jpeg', 'gif'],
    'vector': ['svg', 'svgz']
}

OPTIMIZERS = {
    'jpg': { 'enabled': True, 'options': '-progressive -copy none -optimize'},
    'png': { 'enabled': True, 'options': '-o3 -nc -nb -full -quiet' }
}

WATERMARK = {
    'enabled': False,
    'file': 'watermark.png',
    'position': 'Center'
}

MAX_FILESIZE = 1024 * 1024 * 1024 * 4