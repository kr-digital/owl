## API Documentation

### Authorization

Authorization is performed by passing *client* and *token* parameters in the HTTP request header. The set of valid client-token pairs is defined in the *owl/settings.py* configuration file.

### File Upload

**Request:**
* URL: `/api/files`
* Method: `POST`

**Parameters:**
* `file` — file to be uploaded
* `watermark` — optional (1/0), default is 0. Determines whether to apply a watermark

**Response:**
```json
{
    "output_file": "9/6/4.jpeg",
    "result": true
}
```

### File Retrieval

**Request:**
* URL: `/api/files`
* Method: `GET`

**Parameters:**
* `r` — string containing a list of requested files with filters separated by commas
    * Example: `8/0/4.jpeg:w50h70,c/d/test__Kopiya_4.jpeg:w150h150fill|sat60`
    * Filters start after the colon following the file name
    * Different filters are separated by vertical bars
* `force` — optional (1/0), default is 0. Determines whether to clear cached images before creating new ones

**Response:**
```json
{
    "0": {
        "request_filters": "w50h70",
        "request_file": "8/0/4.jpeg",
        "result": false,
        "err_code": 303
    },
    "1": {
        "request_filters": "w150h150fill|sat60",
        "request_file": "c/d/test__Kopiya_4.jpeg",
        "result": true,
        "output_filesize": 8747,
        "output_file": "cache/c/d/test__Kopiya_4.jpeg/w150h150fill|sat60.jpeg"
    }
}
```

### File Deletion

**Request:**
* URL: `/api/files`
* Method: `DELETE`

**Parameters:**
* `r` — string containing a list of files to be deleted separated by commas
    * Example: `9/6/4.jpeg`

**Response:**
```json
{
    "0": {
        "request_file": "9/6/4.jpeg",
        "result": true
    }
}
```