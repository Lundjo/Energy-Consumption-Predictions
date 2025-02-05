import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas
from database.database import insert_data as insert
import training.energy_consumption_main as training

app = Flask(__name__)
CORS(app)  # Omogućava CORS za komunikaciju između frontenda i backenda
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024

@app.route('/api/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('folder')
    if not files:
        return jsonify({"error": "Nijedan fajl nije pronađen"}), 400

    sent = False
    dl = pd.DataFrame()
    dw = pd.DataFrame()
    saved_files = []

    for file in files:
        if file.filename.endswith('.csv'):
            df = pandas.read_csv(file, engine='python', sep=',')
            df.columns = df.columns.str.lower().str.replace(' ', '_')
            if(df.shape[1] == 5):
                df['time_stamp'] = pd.to_datetime(df['time_stamp'])
                df_filtered = df[df['time_stamp'].dt.minute == 0].astype(str)
                dl = pd.concat([dl, df_filtered], ignore_index=True)
            else:
                dw = pd.concat([dw, df], ignore_index=True)

    if not dl.empty:
        insert(dl, 'load_data')
        sent = True
    if not dw.empty:
        insert(dw, 'weather_data')
        sent = True
    if not sent:
        return jsonify({"error": "Samo CSV fajlovi su dozvoljeni"}), 400

    return jsonify({
        "message": "Fajlovi su uspešno uploadovani",
        "saved_files": saved_files
    }), 200

@app.route('/api/train', methods=['POST'])
def train_model():
    data = request.get_json()

    layers = data.get('layers')
    if layers is None:
        layers = 3

    neurons_first_layer = data.get('neuronsFirstLayer', 17)
    if neurons_first_layer is None:
        neurons_first_layer = 17

    neurons_other_layers = data.get('neuronsOtherLayers', 10)
    if neurons_other_layers is None:
        neurons_other_layers = 10

    epochs = data.get('epochs', 100)
    if epochs is None:
        epochs = 100

    training.mainTraining(layers, neurons_first_layer, neurons_other_layers, epochs)

    return jsonify({
        "message": "Model training started"
    }), 200

if __name__ == '__main__':
    app.run(debug=True)