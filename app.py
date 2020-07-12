from flask import Flask
from flask_restful import Api

from resources.predict import PredictFile, PredictText

app = Flask(__name__)

api = Api(app)

api.add_resource(PredictText, '/predict/text')
api.add_resource(PredictFile, '/predict/file')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
