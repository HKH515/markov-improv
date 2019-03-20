from flask import Flask, render_template, request
from generate import Generator, GeneratorLoader

app = Flask(__name__)


model_id_to_name = {"nltk": "NLTK", "markov": "Markov chain"}
generator_loader = GeneratorLoader()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate')
def joke_page(methods = ["GET"]):
    comedian = request.args["comedian"]
    model = request.args["model"]
    gen = generator_loader[(comedian, model)]
    return render_template("generate.html", jokes = gen.get_jokes(5), model_id=model, model=model_id_to_name[model], comedian_id=comedian, comedian=" ".join([s.capitalize() for s in comedian.split("_")]))

@app.route('/generate_landing')
def joke_landing_page():
    return render_template("generate_landing.html")

@app.route("/sentencefinisher_landing")
def sentencefinisher_landing():
    return render_template("sentencefinisher_landing.html")

#@app.route("/sentencefinisher")
#def sentencefinisher_landing(methods = ["GET"]):
#    return render_template("sentencefinisher_landing.html")

if __name__ == "__main__":
    app.run()