import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas
from database.database import insert_data as insert
import training.energy_consumption_main as training
from waitress import serve
import predict.predict as predict

app = Flask(__name__)
CORS(app)  # Omogućava CORS za komunikaciju između frontenda i backenda
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024

@app.route('/api/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('folder')
    if not files:
        return jsonify({"error": "No files have been found"}), 400

    dl = pd.DataFrame()
    dw = pd.DataFrame()

    for file in files:
        if file.filename.endswith('.csv'):
            df = pandas.read_csv(file, engine='python', sep=',')
            df.columns = df.columns.str.lower().str.replace(' ', '_')
            if df.shape[1] == 5:
                df['time_stamp'] = pd.to_datetime(df['time_stamp'])
                df_filtered = df[df['time_stamp'].dt.minute == 0].astype(str)
                dl = pd.concat([dl, df_filtered], ignore_index=True)
            else:
                dw = pd.concat([dw, df], ignore_index=True)

    if not dl.empty:
        insert(dl, 'load_data')
    if not dw.empty:
        insert(dw, 'weather_data')
    if dl.empty and dw.empty:
        return jsonify({"message": "No csv files found"}), 400

    return jsonify({"message": "Chunk uploaded successfully"}), 200


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

    finished = training.mainTraining(layers, neurons_first_layer, neurons_other_layers, epochs, data.get('startDate'), data.get('endDate'))

    if finished:
        return jsonify({
            "message": "Model trainined"
        }), 200
    else:
        return jsonify({
            "message": "Model could not be trained"
        }), 400


@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    start_date = data.get('startDate')
    end_date = data.get('endDate')
    city = data.get('city')
    model_type = data.get('modelType')  # "new" ili "standard"

    # Provera podataka
    if not start_date or not end_date or not city or not model_type:
        return jsonify({"message": "Missing data"}), 400

    # Odabir modela
    if model_type == "new":
        # Poziv novog modela
        predict.test(start_date, end_date, city, model_type)
    elif model_type == "standard":
        # Poziv standardnog modela
        predict.test(start_date, end_date, city, model_type)
    else:
        return jsonify({"message": "Invalid model type"}), 400

    return jsonify({"message": f"Prediction for {city} from {start_date} to {end_date} using {model_type}"})

serve(app, host="0.0.0.0", port=5000, max_request_body_size=1073741824)