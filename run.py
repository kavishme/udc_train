from flask import request, jsonify
from flask_api import FlaskAPI
from flask_cors import CORS
import operator
from magpie import Magpie
import os

folder = "magpie_model"
labf = open(folder+"/askubuntu.labels", 'r')
labels = labf.read()
labels = labels.split('\n')
labels = [l for l in labels if len(l)>1 ]

print("loading model")
magpie = Magpie(keras_model=folder+'/model.h5',
		word2vec_model=folder+'/wordvec', 
		scaler=folder+'/scalervec',
		labels=labels)
#print(labels)

def create_app():
    app = FlaskAPI(__name__, instance_relative_config=True)

    CORS(app)

    @app.route('/categorize/', methods=['POST'])
    def mag_ask():
        if request.method == "POST":
            #versions = []
            versions = ["16.04", "16.10", "14.04", "14.10", "12.10", "12.04.5", "12.04"]
            question = str(request.data.get('question'))
            if question:

                que_cats = magpie.predict_from_text(question)
                que_cats = sorted(que_cats, key=operator.itemgetter(1), reverse=True)[:5]
                print(que_cats)
                que_cats = [t[0] for t in que_cats if t[1]>0.015 and t[0] not in versions]
                if len(que_cats)>1:
                    response = jsonify({
                        'categories': que_cats
                    })
                    response.status_code = 200
                    return response
            return jsonify({
                    'categories': ['unknown']
                })
    return app

app = create_app()

if __name__ == '__main__':
    app.run(port=5001)



