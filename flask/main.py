import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas
from database.database import insert_data as insert

app = Flask(__name__)
CORS(app)  # Omogućava CORS za komunikaciju između frontenda i backenda

@app.route('/api/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('folder')
    if not files:
        return jsonify({"error": "Nijedan fajl nije pronađen"}), 400

    sent = False

    saved_files = []
    for file in files:
        if file.filename.endswith('.csv'):
            df = pandas.read_csv(file, engine='python', sep=',')
            df.columns = df.columns.str.lower().str.replace(' ', '_')
            if(df.shape[1] == 5):
                df['time_stamp'] = pd.to_datetime(df['time_stamp'])
                df_filtered = df[df['time_stamp'].dt.minute == 0].astype(str)
                insert(df_filtered, 'load_data')
            else:
                insert(df, 'weather_data')

            sent = True
    if not sent:
        return jsonify({"error": "Samo CSV fajlovi su dozvoljeni"}), 400

    return jsonify({
        "message": "Fajlovi su uspešno uploadovani",
        "saved_files": saved_files
    }), 200

if __name__ == '__main__':
    app.run(debug=True)