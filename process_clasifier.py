from magpie import Magpie
import os

magpie = Magpie()

folder = "data"

print("word2vec")
#magpie.train_word2vec(folder, vec_dim=160)
#magpie.fit_scaler(folder)

magpie.init_word_vectors(folder, vec_dim=100)
magpie.save_word2vec_model('models/wordvec')
print("fit scalar")
magpie.save_scaler('models/scalervec', overwrite=True)

#labf = open("askubuntu.labels", 'r')
#labels = labf.read()
#labels = labels.split('\n')

#print(labels[:100])

#print("Training")
#magpie.train(folder, labels, test_ratio=0.2, epochs=30)
#magpie.save_model('model/model.h5')

