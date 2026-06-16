from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)
SECRET_KEY = "your-secret-key"
users = {"bob": "qwe123"}

@app.route('/v1/user', methods=['POST'])
def register():
    data = request.get_json()
    login = data.get('login')
    password = data.get('password')
    if login in users:
        return jsonify({"error": "User exists"}), 409
    users[login] = password
    return jsonify({"login": login}), 201

@app.route('/v1/token', methods=['POST'])
def token():
    data = request.get_json()
    login = data.get('login')
    password = data.get('password')
    if users.get(login) == password:
        payload = {
            "sub": login,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token, 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/v1/token/validation/', methods=['GET'])
def validate_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return "", 401
    token = auth_header.split(' ')[1]
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return "", 200
    except jwt.InvalidTokenError:
        return "", 401

@app.route('/v1/user', methods=['GET'])
def get_user():
    return jsonify({"user": "bob", "id": 123}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
