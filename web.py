from flask import Flask, render_template
from generate import Generator


app = Flask(__name__)

@app.route('/')
def index():
    gen = Generator("chris_rock")
    return render_template("web.html", jokes = gen.get_jokes(1000))

if __name__ == "__main__":
    app.run()