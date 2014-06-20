# Owl settings here
DEBUG = True

# List of clients tokens
CLIENTS = {}
CLIENTS['client'] = 'token'

# Output data format
FORMAT = 'JSON'

# Storage engine
STORAGE_ENGINE = 'local'
STORAGE_ENGINE_LOCAL_DATA_PATH = '/path/to/storage/data'

# Storage image operator
STORAGE_IMAGE_OPERATOR = 'imagemagick'
STORAGE_IMAGE_OPERATOR_CONVERT_PATH = '/usr/bin/convert'

# Storage options
STORAGE_WORKERS = 1
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc'}
MAX_FILESIZE = 1024 * 1024 * 10
