import markovify
import sys
import os
import nltk

import re

nltk.download('averaged_perceptron_tagger')

file_root = "corpora"

class GeneratorLoader:
    def __init__(self):
        self.comedians = ["chris_rock", "dave_chappelle", "amy_schumer", "gabriel_iglesias"]
        self.models = ["nltk", "markov"]
        self.generators = {}
        for comedian in self.comedians:
            for model in self.models:
                print("Loading comedian %s with model %s" % (comedian, model))
                self.generators[(comedian, model)] = Generator(comedian, model)
    def __getitem__(self, key):
        return self.generators[key]





class Generator:
    def __init__(self, folder, model="nltk"):
        self.models = []
        for f in os.listdir(os.path.join(file_root, folder)):
            file_path = os.path.join(file_root, folder, f)
            with open(file_path) as f_stream:
                data = f_stream.read()
                if model == "nltk":
                    self.models.append(CustomText(data))
                else:
                    self.models.append(markovify.Text(data))
            self.combo_model = markovify.combine(self.models, [1] * len(self.models))

    def get_jokes(self, num_jokes):
        jokes = []
        for i in range(num_jokes):
            jokes.append(self.combo_model.make_sentence())
        if None in jokes:
            jokes.remove(None)
        return jokes
# Print five randomly-generated sentences

# Print three randomly-generated sentences of no more than 140 characters
#for i in range(100):
#    print(text_model.make_short_sentence(140))

class CustomText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence
    
    """
    Overriden function for throwing away sentences that we dont want.
    TODO find more constraints for the sentences.
    """
    def test_sentence_output(self, words, max_overlap_ratio, max_overlap_total):
        """
        Given a generated list of words, accept or reject it. This one rejects
        sentences that too closely match the original text, namely those that
        contain any identical sequence of words of X length, where X is the
        smaller number of (a) `max_overlap_ratio` (default: 0.7) of the total
        number of words, and (b) `max_overlap_total` (default: 15).
        """
        # Reject large chunks of similarity
        overlap_ratio = int(round(max_overlap_ratio * len(words)))
        overlap_max = min(max_overlap_total, overlap_ratio)
        overlap_over = overlap_max + 1
        gram_count = max((len(words) - overlap_max), 1)
        grams = [ words[i:i+overlap_over] for i in range(gram_count) ]
        for g in grams:
            gram_joined = self.word_join(g)
            #check if begining quote is as many as end quote
            if(gram_joined.count("“") != 
                gram_joined.count("”")% 2):
                return False
            if gram_joined in self.rejoined_text:
                return False
        return True

#gene = Generator("chris_rock")
#print(gene.get_jokes(2))