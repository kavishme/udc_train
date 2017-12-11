from magpie import Magpie

magpie = Magpie()
magpie.train_word2vec('data/hep-categories', vec_dim=100)
magpie.fit_scaler('data/hep-categories')
labels = ['Gravitation and Cosmology', 'Experiment-HEP', 'Theory-HEP']
magpie.train('data/hep-categories', labels, test_ratio=0.2, epochs=30)
magpie.save_word2vec_model('./model')
magpie.save_scaler('./model', overwrite=True)
magpie.save_model('./model.h5')
