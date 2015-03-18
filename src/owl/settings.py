# Owl settings here
DEBUG = True

# List of clients tokens
CLIENTS = {}
CLIENTS['domzamkad'] = '7gJpZdDmQnYNPheQJkruX2WRpxuZQsHC'

# Output data format
FORMAT = 'JSON'

# Storage engine
STORAGE_ENGINE = 'local'
STORAGE_ENGINE_LOCAL_DATA_PATH = '/home/www/vhosts/owl/storage/data'

# Storage image operator
STORAGE_IMAGE_OPERATOR = 'imagemagick'
STORAGE_IMAGE_OPERATOR_CONVERT_PATH = 'convert'
STORAGE_IMAGE_OPERATOR_COMPOSE_PATH = 'composite'
STORAGE_IMAGE_OPERATOR_IDENTIFY_PATH = 'identify'

# Storage vector graphic operator
STORAGE_VECTOR_OPERATOR = 'librsvg'
STORAGE_VECTOR_OPERATOR_CONVERT_PATH = 'rsvg-convert'

# Storage options
STORAGE_WORKERS = 1
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'svg', 'svgz'}

ALLOWED_EXTENSIONS = {
    'binary': ['txt', 'pdf', 'doc'],
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

MAX_FILESIZE = 1024 * 1024 * 10
