from flask import Flask, render_template, request
from generate import Generator
import random
import os

app = Flask(__name__)


model_id_to_name = {"nltk": "NLTK", "markov": "Markov chain"}

file_root = "corpora"
state_size_upperbound = 3


comedian_id_to_name = lambda comedian: " ".join([s.capitalize() for s in comedian.split("_")])

def initialize_comedians():
    dic = {}
    for f in os.listdir(file_root):
        farr = f.split("_")
        farr = [i.capitalize() for i in farr]
        f_cap = " ".join(farr)
        dic[f] = f_cap
    return dic
comedians = initialize_comedians()

generator_cache = {}

def get_gen(comedian, model, state_size):
    if (comedian, model) not in generator_cache:
        gen = Generator(comedian, model, state_size)
        generator_cache[(comedian, model, state_size)] = gen
    gen = generator_cache[(comedian, model, state_size)]
    return gen

def continue_sentence(sentence, comedian, model):
    finished_sentence = None
    i = state_size_upperbound
    while True:
        if i == 0:
            big_gen = get_gen(comedian, model, state_size_upperbound)
            finished_sentence = big_gen.get_jokes(1)[0]
            break
        gen = get_gen(comedian, model, i)
        finished_sentence = gen.finish_sentence(sentence)
        if finished_sentence:
            break
        i -= 1
    return finished_sentence

def get_ensamble_sentences(model, num_sentences):
    comedian_list = list(comedians.keys())
    random.shuffle(comedian_list)
    curr_comedian = random.choice(comedian_list)
    curr_sentence = get_gen(curr_comedian, model, state_size_upperbound).get_jokes(1)[0]
    sentences = [curr_sentence]
    comedian_sequence = [curr_comedian]
    for i in range(num_sentences):
        next_comedian = comedian_list[(comedian_list.index(curr_comedian)+1) % len(comedian_list)]
        next_sentence = continue_sentence(curr_sentence, next_comedian, model)
        curr_comedian = next_comedian
        curr_sentence += next_sentence
        sentences.append(next_sentence)
        comedian_sequence.append(next_comedian)
        
    return zip(comedian_sequence, sentences)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate')
def joke_page(methods = ["GET"]):
    comedian = request.args["comedian"]
    model = request.args["model"]
    gen = get_gen(comedian, model, state_size_upperbound)

    return render_template("generate.html", jokes = gen.get_jokes(5), model_id=model, model=model_id_to_name[model], comedians=comedians, comedian_id=comedian, comedian=comedian_id_to_name(comedian))

@app.route('/generate_landing')
def joke_landing_page():
    return render_template("generate_landing.html", comedians=comedians)

@app.route("/sentencefinisher_landing")
def sentencefinisher_landing():
    return render_template("sentencefinisher_landing.html", comedians=comedians)

@app.route("/sentencefinisher")
def sentencefinisher(methods = ["GET"]):
    comedian = request.args["comedian"]
    model = request.args["model"]
    sentence = request.args["sentence"]
    i = state_size_upperbound
    finished_sentence = continue_sentence(sentence, comedian, model)

    return render_template("sentencefinisher.html", comedians=comedians, model_id=model, model=model_id_to_name[model], comedian=comedian_id_to_name(comedian), comedian_id=comedian, finished_sentence=finished_sentence)

@app.route("/ensemble_landing")
def ensamble_landing():
    return render_template("ensemble_landing.html")

@app.route("/ensemble")
def ensemble(methods = ["GET"]):
    model = "markov"
    num_sentences = int(request.args["num_sentences"])
    ensamble_sentences = get_ensamble_sentences(model, num_sentences)
    return render_template("ensemble.html", ensamble_sentences=ensamble_sentences, comedians=comedians)



#@app.route("/sentencefinisher")
#def sentencefinisher_landing(methods = ["GET"]):
#    return render_template("sentencefinisher_landing.html")

if __name__ == "__main__":
    app.run()