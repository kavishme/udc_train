from magpie import Magpie
import os

folder = "data"
labf = open("askubuntu.labels", 'r')
labels = labf.read()
labels = labels.split('\n')
labels = [l for l in labels if len(l)>1 ]

magpie = Magpie(word2vec_model='models/wordvec', 
		scaler='models/scalervec',
		labels=labels)
print(labels)

print("Training")
magpie.train(folder, labels, test_ratio=0.2, epochs=30)
magpie.save_model('models/model.h5')


