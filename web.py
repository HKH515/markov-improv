from flask import Flask, render_template, request
from generate import Generator


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate')
def joke_page(methods = ["GET"]):
    comedian = request.args["comedian"]
    gen = Generator(comedian)
    return render_template("generate.html", jokes = gen.get_jokes(1), comedian=" ".join([s.capitalize() for s in comedian.split("_")]))

if __name__ == "__main__":
    app.run()