from flask import Flask, request, jsonify
from minio import Minio
import uuid
import io
import os

app = Flask(__name__)

minio_client = Minio(
    os.getenv("MINIO_ENDPOINT", "minio:9000"),
    access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
    secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
    secure=False
)

bucket_name = "images"
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)

@app.route('/v1/upload', methods=['POST'])
def upload():
    file_data = request.get_data()
    filename = f"{uuid.uuid4()}.jpg"
    
    minio_client.put_object(
        bucket_name,
        filename,
        io.BytesIO(file_data),
        len(file_data),
        content_type="image/jpeg"
    )
    
    return jsonify({"filename": filename}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
