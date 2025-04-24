from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Fishing Logger!"

if __name__ == "__main__":
    app.run(debug=True)
