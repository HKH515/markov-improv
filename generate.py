import markovify
import sys
import os

file_root = "corpora"

class Generator:
    def __init__(self, folder):
        self.models = []
        for f in os.listdir(os.path.join(file_root, folder)):
            file_path = os.path.join(file_root, folder, f)
            with open(file_path) as f_stream:
                data = f_stream.read()
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