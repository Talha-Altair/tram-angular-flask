import os
import pandas as pd
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')

client = MongoClient(MONGO_URI)

db = client['flood']

ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
CORS(app)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def send_message(message):

    return jsonify({'message': message})


@app.route('/', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':

        file = request.files['file']

        filename = secure_filename(file.filename)

        if file and allowed_file(filename):

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            handle_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return send_message('File uploaded successfully')

        return send_message('File not allowed')

    return send_message('Send a file')


def handle_csv(file_name):

    df = pd.read_csv(file_name)

    df.reset_index(inplace=True)

    df.fillna(0, inplace=True)

    data_dict = df.to_dict("records")

    file_name = file_name.split('/')[-1].split('.')[0]

    coll_name = 'tram-data-' + file_name

    myCollection = db[coll_name]

    myCollection.insert_many(data_dict)

    print(
        f'File {file_name}.csv uploaded successfully to collection {coll_name} in database {db.name}'
    )


if __name__ == '__main__':
    app.run(debug=True)
