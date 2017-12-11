from magpie import Magpie
import os

folder = "magpie_data"
labf = open(folder+"askubuntu.labels", 'r')
labels = labf.read()
labels = labels.split('\n')
labels = [l for l in labels if len(l)>1 ]

print("loading model")
magpie = Magpie(keras_model=folder+'/model.h5',
		word2vec_model=folder+'/wordvec', 
		scaler=folder+'/scalervec',
		labels=labels)
#print(labels)



                response = jsonify({
                    'categories': que_cats
                })
                response.status_code = 200
                return response

    @app.route('/magcategorize/', methods=['POST'])
    def mag_ask():
        if request.method == "POST":
            question = str(request.data.get('question'))
            if question:

                que_cats = magpie.predict_from_text(question)
                print(que_cats)
                response = jsonify({
                    'categories': que_cats
                })
                response.status_code = 200
    return app
