from flask import Flask
from config import AWS_SECRET_KEY

app = Flask(__name__)

@app.route('/')
def home():
    return f"Secret: {AWS_SECRET_KEY}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)