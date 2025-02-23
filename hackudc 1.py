from flask import Flask, send_from_directory, abort, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)

# Configuración para los tipos de contenido y servidor
ALLOWED_METHODS = ["GET", "HEAD"]
CONTENT_TYPES = {
    "html": "text/html",
    "txt": "text/plain",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "gif": "image/gif",
}
SERVER_NAME = "AppuServer/1.0"
STATUS_CODES = {
    200: "OK",
    301: "Moved Permanently",
    400: "Bad Request",
    404: "Not Found",
    405: "Method Not Allowed",
    500: "Internal Server Error",
    501: "Not Implemented",
}
VERBOSITY = 0


@app.route('/', methods=['GET', 'HEAD'])
def index():
    """Redirige a index.html."""
    return redirect(url_for('serve_file', filename='index.html'), code=301)


@app.route('/<path:filename>', methods=['GET', 'HEAD'])
def serve_file(filename):
    """Sirve los archivos desde el directorio 'data'."""
    # Verifica si el archivo existe
    file_path = os.path.join('data', filename)
    if not os.path.isfile(file_path):
        abort(404)

    # Obtiene la extensión y tipo MIME
    extension = filename.split('.')[-1]
    mime = CONTENT_TYPES.get(extension, 'application/octet-stream')

    # Si el método es HEAD, solo retorna los encabezados
    if request.method == 'HEAD':
        return '', 200, {'Content-Type': mime, 'Content-Length': str(os.path.getsize(file_path))}

    # Si el método es GET, sirve el archivo
    return send_from_directory('data', filename, mimetype=mime)

@app.route('/Plan_Map')
def home():
    return send_from_directory('data', 'maplan.html')

@app.errorhandler(404)
def not_found(error):
    """Manejo de errores 404."""
    return f"<h1>Error 404</h1><p>{STATUS_CODES[404]}</p>", 404


@app.errorhandler(400)
def bad_request(error):
    """Manejo de errores 400."""
    return f"<h1>Error 400</h1><p>{STATUS_CODES[400]}</p>", 400


if __name__ == '__main__':
    # Ejecuta el servidor en localhost:8000
    app.run(host='127.0.0.1', port=8000)
