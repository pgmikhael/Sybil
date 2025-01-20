# Hướng Dẫn Cài Đặt

Python 3.10
Pip version <=24.0

## 1.

```sh
pip install -r requirements.txt
```

## 2. API

To use the API, follow these steps:

1. Open a terminal or command prompt.
2. Navigate to the directory containing the `api.py` file.
3. Run the following command to start the API:

   ```sh
   python api.py
   ```

4. The API will be accessible at `http://localhost:5000`.

### Endpoints

- **POST /api_predict**: Upload images for prediction.

  - **Request**: Multipart form data with files.
  - **Response**: JSON with prediction results and links to overlay images.

- **GET /download/<session_id>/<filename>**: Download overlay image by session ID.

  - **Response**: File download or error message.

- **GET /preview/<session_id>/<filename>**: Preview overlay image in the browser.

  - **Response**: Image preview or error message.

- **GET /download_gif/<session_id>**: Download GIF of overlay images.
  - **Response**: GIF file download or error message.

For more details, refer to the [API documentation](./api.py).
