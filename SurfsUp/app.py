
# 1. import Flask
from flask import Flask
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)
# 3. Define what to do when a user hits the index route
@app.route("/")
def hello_world():
    return "hi"


    


if __name__ == "__main__":
    app.run(debug=True)
