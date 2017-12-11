from magpie import Magpie
import os

magpie = Magpie()

folder = "output_201711120349"

print("word2vec")
magpie.train_word2vec(folder, vec_dim=160)
print("fit scalar")
magpie.fit_scaler(folder)

labf = open("askubuntu.labels", 'r')
labels = labf.read()
labels = labels.split('\n')

#print(labels[:100])

print("Training")
magpie.train(folder, labels, test_ratio=0.2, epochs=30)
magpie.save_word2vec_model('models')
magpie.save_scaler('models', overwrite=True)
magpie.save_model('model/model.h5')

