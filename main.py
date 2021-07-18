# main.py
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello_world():
    return "Hello World from Cloud Run!"

@app.route("/auth_exchange", methods=["POST"])
def auth_exchange_handler():
    data_dict = request.get_json()

    if not data_dict:
        msg = "No payload received"
        middleware.logger.error(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(data_dict, dict):
        msg = "Invalid payload data format"
        middleware.logger.error(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not "code" in data_dict:
        msg = "Missing key 'code'"
        middleware.logger.error(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    try:
        output = auth_helper.new_request_auth_exchange(data_dict)
        return output, 200
    except Exception as err:
        return f"Error: {err}", 500

    ...
    # Chuẩn bị 2 hàm tương tự cho các đường dẫn: /auth_refresh and /auth_info như mô tả trong bài: https://miniapp.tiki.vn/docs/backend-api/platform-api/exchange-auth-token
    ...

if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080
    app.run(host="0.0.0.0", port=PORT, debug=True)
