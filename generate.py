import markovify
import sys
import os

folder = sys.argv[1]

file_root = "corpora"


models = []

for f in os.listdir(os.path.join(file_root, folder)):
    file_path = os.path.join(file_root, folder, f)
    with open(file_path) as f_stream:
        data = f_stream.read()
        models.append(markovify.Text(data))


combo_model = markovify.combine(models, [1] * len(models))

# Print five randomly-generated sentences
for i in range(10):
    print(combo_model.make_sentence())

# Print three randomly-generated sentences of no more than 140 characters
#for i in range(100):
#    print(text_model.make_short_sentence(140))