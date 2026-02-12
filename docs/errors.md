## Error Codes

### Authorization Errors

* **101** — Client not found  
  The specified client ID is not registered in the system.

* **102** — Token not found  
  The provided token is invalid or does not exist in the system.

* **103** — Invalid client-token pair  
  The combination of client and token does not match any valid authorization credentials.

### File Upload Errors

* **201** — Missing 'file' parameter  
  The required file parameter is not provided during upload.

* **202** — Invalid file type  
  The uploaded file does not match the allowed file types.

* **203** — File size exceeds limit  
  The uploaded file exceeds the maximum allowed size.

### File Retrieval Errors

* **301** — Empty request (missing 'r' parameter)  
  The request does not contain the required 'r' parameter specifying the files to retrieve.

* **302** — Invalid file name format  
  The file name is specified incorrectly or in an unsupported format.

* **303** — File not found  
  The requested file does not exist in the storage.