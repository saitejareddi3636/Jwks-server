from flask import Flask, jsonify, request
import jwt
import time
from keys import generate_key

app = Flask(__name__)

keys = [generate_key()]

@app.route('/jwks', methods=['GET'])
def jwks():
    unexpired_keys = [
        {"kid": key["kid"], "kty": "RSA", "use": "sig", "n": key["public_key"]}
        for key in keys if key["expiry"] > time.time()
    ]
    return jsonify({"keys": unexpired_keys})

@app.route('/auth', methods=['POST'])
def auth():
    expired = request.args.get('expired', False)
    selected_key = keys[0]

    payload = {
        "sub": "test-user",
        "iat": time.time(),
        "exp": time.time() + (3600 if not expired else -3600)
    }

    token = jwt.encode(payload, selected_key["private_key"], algorithm="RS256", headers={"kid": selected_key["kid"]})
    return jsonify({"token": token})

if __name__ == '__main__':
    app.run(port=8080)

